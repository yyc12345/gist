#include <cstdint>
#include <complex>
#include <vector>
#include <cmath>
#include <numbers>
#include <memory>
#include <stdexcept>
#include <algorithm>

namespace YYCFFT {

	namespace Utils {
		
		// NOTE: May be replaced by std::has_single_bit

		template<typename _TyIndex, size_t _N>
		inline constexpr bool IsPow2() {
			size_t N = _N;
			while (!(N & 1u)) {
				N >>= 1u;
			}
			return N == 1u;
		}
		
		// NOTE: May be replaced by std::bit_floor

		template<typename _TyIndex, size_t _N>
		inline constexpr _TyIndex GetPow2Exponent() {
			_TyIndex ret = 0u;
			size_t N = _N;
			while (N) {
				N >>= 1u;
				++ret;
			}
			return --ret;
		}

		template<typename _TyIndex, typename _TyFloat, size_t _N>
		struct ValidateArgs {
		private:
			static constexpr bool _IsUnsignedInt = std::is_unsigned_v<_TyIndex> && std::is_integral_v<_TyIndex>;
			static constexpr bool _IsFloatPoint = std::is_floating_point_v<_TyFloat>;
			static constexpr bool _IsLegalN = IsPow2<_TyIndex, _N>() && _N >= 2u;
		public:
			static constexpr bool value = _IsUnsignedInt && _IsFloatPoint && _IsLegalN;
		};

	}

	enum class WindowType {
		HanningWindow
	};

	template<typename _TyIndex, typename _TyFloat, size_t _N, std::enable_if_t<Utils::ValidateArgs<_TyIndex, _TyFloat, _N>::value, int> = 0>
	class Window {
	private:
		constexpr static _TyIndex N = _N;

	public:
		Window(WindowType win_type) : m_WindowType(win_type), m_WindowData(nullptr) {
			// Pre-compute window data
			// Allocate window buffer
			m_WindowData = std::make_unique<_TyFloat[]>(N);
			// Assign window data
			switch (win_type) {
				case YYCFFT::WindowType::HanningWindow:
					for (_TyIndex i = 0u; i < N; ++i) {
						m_WindowData[i] = static_cast<_TyFloat>(0.5) *
							(static_cast<_TyFloat>(1.0) - std::cos(static_cast<_TyFloat>(2.0) * std::numbers::pi_v<_TyFloat> *static_cast<_TyFloat>(i) / static_cast<_TyFloat>(N - 1u)));
					}
					break;
				default:
					throw std::invalid_argument("invalid window function type");
			}
		}

	private:
		WindowType m_WindowType;
		std::unique_ptr<_TyFloat[]> m_WindowData;
	public:
		void ApplyWindow(_TyFloat* data) const {
			if (data == nullptr) [[unlikely]] {
				throw std::invalid_argument("nullptr data is not allowed for applying window.");
			}
			for (_TyIndex i = 0u; i < N; ++i) {
				data[i] *= m_WindowData[i];
			}
		}
		const _TyFloat* GetWindowData() const {
			return m_WindowData.get();
		}
	};

	template<typename _TyIndex, typename _TyFloat, size_t _N, std::enable_if_t<Utils::ValidateArgs<_TyIndex, _TyFloat, _N>::value, int> = 0>
	class FFT {
	private:
		using _TyComplex = std::complex<_TyFloat>;
		constexpr static _TyIndex N = _N;
		constexpr static _TyIndex M = Utils::GetPow2Exponent<_TyIndex, _N>();
		constexpr static _TyIndex c_HalfPoint = _N >> 1u;

	public:
		FFT() : m_WNPCache(nullptr), m_EasyComputeCache(N, _TyComplex()) {
			// Generate WNP cache
			m_WNPCache = std::make_unique<_TyComplex[]>(N);
			for (_TyIndex P = 0u; P < N; ++P) {
				_TyFloat angle = static_cast<_TyFloat>(2) * std::numbers::pi_v<_TyFloat> * static_cast<_TyFloat>(P) / static_cast<_TyFloat>(N);
				// e^(-jx) = cosx - j sinx
				m_WNPCache[P] = _TyComplex(
					std::cos(angle),
					-std::sin(angle)
				);
			}

			m_EasyComputeCache = std::vector<_TyComplex>();
		}

	private:
		std::unique_ptr<_TyComplex[]> m_WNPCache;
	public:
		void Compute(_TyComplex* data) const {
			if (data == nullptr) [[unlikely]] {
				throw std::invalid_argument("nullptr data is not allowed for FFT computing.");
			}

			_TyIndex LH, J, K, B, P;
			LH = J = c_HalfPoint;

			// Construct butterfly structure
			for (_TyIndex I = 1u; I <= N - 2u; ++I) {
				if (I < J) std::swap(data[I], data[J]);

				K = LH;
				while (J >= K) {
					J -= K;
					K >>= 1u;
				}
				J += K;
			}

			// Calculate butterfly
			_TyComplex temp, temp2;
			for (_TyIndex L = 1u; L <= M; ++L) {
				B = static_cast<_TyIndex>(1u) << (L - 1u);
				for (J = 0u; J <= B - 1u; ++J) {
					P = J * (static_cast<_TyIndex>(1u) << (M - L));

					// Use pre-computed cache instead of real-time computing
					for (_TyIndex KK = J; KK <= N - 1u; KK += (static_cast<_TyIndex>(1u) << L)) {
						temp2 = (data[KK + B] * this->m_WNPCache[P]);
						temp = temp2 + data[KK];
						data[KK + B] = data[KK] - temp2;
						data[KK] = temp;
					}
				}
			}
		}

	private:
		mutable std::vector<_TyComplex> m_EasyComputeCache;
	public:
		/**
		 * @brief Get the maximum frequency by given sample rate.
		 * @param[in] sample_rate 
		 * The sample rate of input stream.
		 * Unit is Hz or SPS (sample point per second).
		 * @return 
		 * The last data in computed FFT drequency data represented frequency.
		 * Unit is Hz.
		*/
		_TyFloat GetMaxFreq(_TyFloat sample_rate) {
			// Following sample priniciple
			return sample_rate / static_cast<_TyFloat>(2.0);
		}
		/**
		 * @brief
		 * The convenient FFT compute function.
		 * For 
		 * @param[in] time_scope
		 * The length of this data must be N.
		 * For the time order of data, the first data should be the oldest data and the last data should be the newest data.
		 * @param[out] freq_scope
		 * The length of this data must be N / 2.
		 * The first data is 0Hz and the frequency of last data is decided by sample rate which can be computed by GetMaxFreq function in this class.
		 * @param[in] window
		 * The window instance applied to data.
		*/
		void EasyCompute(const _TyFloat* time_scope, _TyFloat* freq_scope, const Window<_TyIndex, _TyFloat, _N>& window) const {
			if (time_scope == nullptr || freq_scope == nullptr) [[unlikely]] {
				throw std::invalid_argument("nullptr data is not allowed for easy FFT computing.");
			}

			// First, we copy time scope data into cache with reversed order.
			// because FFT order the first item should be the latest data.
			// At the same time we multiple it with window function.
			std::generate(
				m_EasyComputeCache.begin(),
				m_EasyComputeCache.end(),
				[data = &(time_scope[N]), win_data = window.GetWindowData()]() mutable -> _TyComplex {
					return _TyComplex(*(data--) * *(win_data++), static_cast<_TyFloat>(0));
				}
			);

			// Do FFT compute
			this->Compute(m_EasyComputeCache.data());

			// Compute amplitude
			for (_TyIndex i = 0u; i < c_HalfPoint; ++i) {
				freq_scope[i] = static_cast<_TyFloat>(10.0) * std::log10(std::abs(m_EasyComputeCache[i + c_HalfPoint]));
			}
		}
	};


	using FFT4F = FFT<size_t, float, 4u>;
	using FFT8F = FFT<size_t, float, 8u>;
	using FFT16F = FFT<size_t, float, 16u>;
	using FFT32F = FFT<size_t, float, 32u>;
	using FFT64F = FFT<size_t, float, 64u>;
	using FFT128F = FFT<size_t, float, 128u>;
	using FFT256F = FFT<size_t, float, 256u>;
	using FFT512F = FFT<size_t, float, 512u>;
	using FFT1024F = FFT<size_t, float, 1024u>;
	using FFT2048F = FFT<size_t, float, 2048u>;
	
	using FFT4 = FFT<size_t, double, 4u>;
	using FFT8 = FFT<size_t, double, 8u>;
	using FFT16 = FFT<size_t, double, 16u>;
	using FFT32 = FFT<size_t, double, 32u>;
	using FFT64 = FFT<size_t, double, 64u>;
	using FFT128 = FFT<size_t, double, 128u>;
	using FFT256 = FFT<size_t, double, 256u>;
	using FFT512 = FFT<size_t, double, 512u>;
	using FFT1024 = FFT<size_t, double, 1024u>;
	using FFT2048 = FFT<size_t, double, 2048u>;

}
