#include <YYCFFT.hpp>
#include <initializer_list>
#include <format>
#include <iostream>
#include <limits>
#include <random>
#include <chrono>

namespace YYCFFTTestbench {

	using TIndex = size_t;
	using TFloat = float;
	using TComplex = std::complex<TFloat>;
	template<size_t N>
	using TFFT = YYCFFT::FFT<TIndex, TFloat, N>;

	static void PrintResult(bool ret) {
		if (ret) std::cout << "Test Pass" << std::endl;
		else {
			std::cout << "Test Failed" << std::endl;
			std::abort();
		}
	}
	template<size_t N>
	static bool TestPair(const std::initializer_list<TFloat>& _src, const std::initializer_list<TComplex>& _dst) {
		// Create FFT instance
		TFFT<N> fft;
		// Accept input
		std::vector<TComplex> src(_src.size());
		std::generate(src.begin(), src.end(), [data = _src.begin()]() mutable -> TComplex { return TComplex(*data++); });
		std::vector<TComplex> dst(_dst);
		// Compute FFT
		fft.Compute(src.data());
		// Format result
		//constexpr TFloat tolerance = std::numeric_limits<TFloat>::epsilon();
		constexpr TFloat tolerance = 0.0003f;
		for (TIndex i = 0u; i < src.size(); ++i) {
			if (std::fabs(src[i].real() - dst[i].real()) >= tolerance) return false;
			if (std::fabs(src[i].imag() - dst[i].imag()) >= tolerance) return false;
		}
		return true;
	}
	static void TestAnswer() {

		PrintResult(TestPair<8>(
			{1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f, 7.0f, 8.0f}, 
			{{+3.6000e+01f, +0.0000e+00f}, {-4.0000e+00f, +9.6569e+00f}, {-4.0000e+00f, +4.0000e+00f}, {-4.0000e+00f, +1.6569e+00f}, {-4.0000e+00f, +0.0000e+00f}, {-4.0000e+00f, -1.6569e+00f}, {-4.0000e+00f, -4.0000e+00f}, {-4.0000e+00f, -9.6569e+00f}}
		));
		PrintResult(TestPair<8>(
			{6.0f, 1.0f, 7.0f, 2.0f, 7.0f, 4.0f, 8.0f, 7.0f}, 
			{{+4.2000e+01f, +0.0000e+00f}, {+4.1421e-01f, +6.6569e+00f}, {-2.0000e+00f, +4.0000e+00f}, {-2.4142e+00f, +4.6569e+00f}, {+1.4000e+01f, +0.0000e+00f}, {-2.4142e+00f, -4.6569e+00f}, {-2.0000e+00f, -4.0000e+00f}, {+4.1421e-01f, -6.6569e+00f}}
		));
		PrintResult(TestPair<4>(
			{1.0f, 2.0f, 3.0f, 4.0f}, 
			{{+1.0000e+01f, +0.0000e+00f}, {-2.0000e+00f, +2.0000e+00f}, {-2.0000e+00f, +0.0000e+00f}, {-2.0000e+00f, -2.0000e+00f}}
		));
		PrintResult(TestPair<4>(
			{6.0f, 1.0f, 7.0f ,2.0f}, 
			{{+1.6000e+01f, +0.0000e+00f}, {-1.0000e+00f, +1.0000e+00f}, {+1.0000e+01f, +0.0000e+00f}, {-1.0000e+00f, -1.0000e+00f}}
		));
		PrintResult(TestPair<4>(
			{4.0f, 4.0f, 4.0f ,4.0f}, 
			{{+1.6000e+01f, +0.0000e+00f}, {+0.0000e+00f, +0.0000e+00f}, {+0.0000e+00f, +0.0000e+00f}, {+0.0000e+00f, +0.0000e+00f}}
		));
		PrintResult(TestPair<16>(
			{1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f, 7.0f, 8.0f, 9.0f, 10.0f, 11.0f, 12.0f, 13.0f, 14.0f, 15.0f, 16.0f}, 
			{{+1.3600e+02f, +0.0000e+00f}, {-8.0000e+00f, +4.0219e+01f}, {-8.0000e+00f, +1.9314e+01f}, {-8.0000e+00f, +1.1973e+01f}, {-8.0000e+00f, +8.0000e+00f}, {-8.0000e+00f, +5.3454e+00f}, {-8.0000e+00f, +3.3137e+00f}, {-8.0000e+00f, +1.5913e+00f}, {-8.0000e+00f, +0.0000e+00f}, {-8.0000e+00f, -1.5913e+00f}, {-8.0000e+00f, -3.3137e+00f}, {-8.0000e+00f, -5.3454e+00f}, {-8.0000e+00f, -8.0000e+00f}, {-8.0000e+00f, -1.1973e+01f}, {-8.0000e+00f, -1.9314e+01f}, {-8.0000e+00f, -4.0219e+01f}}
		));

	}

	static void TestSpeed() {

		// Prepare FFT engine
		constexpr TIndex FFTPoint = 1024u;
		TFFT<FFTPoint> fft;

		// Prepare random buffer
		constexpr TIndex RndBufCnt = 10u;
		std::random_device rnd_device;
		std::default_random_engine rnd_engine(rnd_device());
		std::uniform_real_distribution<TFloat> rnd_dist(0.0f, 1.0f);
		std::vector<std::vector<TComplex>> buffer_collection(RndBufCnt);
		for (auto& buf : buffer_collection) {
			buf.resize(FFTPoint);
			std::generate(buf.begin(), buf.end(), [&rnd_engine, &rnd_dist]() mutable -> TComplex { return TComplex(rnd_dist(rnd_engine)); });
		}

		// Do benchmark
		constexpr TIndex TestIterCnt = 1000u;
		auto start_timestamp = std::chrono::high_resolution_clock::now();
		for (auto& buf : buffer_collection) {
			for (TIndex i = 0u; i < TestIterCnt; ++i) {
				fft.Compute(buf.data());
			}
		}
		auto end_timestamp = std::chrono::high_resolution_clock::now();

		// Output result
		std::chrono::duration<double, std::ratio<1, 1>> elpased = end_timestamp - start_timestamp;
		std::cout << "Computing 1024-point float-based FFT " << RndBufCnt * TestIterCnt << " times consume " << elpased.count() << " sec" << std::endl;
		std::cout << "Average time per FFT operation: " << elpased.count() / ((double)RndBufCnt * TestIterCnt) << " sec" << std::endl;
		
	}

}

int main(int argc, char* argv[]) {

	std::cout << "Start testing answer..." << std::endl;
	YYCFFTTestbench::TestAnswer();
	std::cout << "Start testing speed..." << std::endl;
	YYCFFTTestbench::TestSpeed();

}
