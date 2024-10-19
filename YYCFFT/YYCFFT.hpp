#include <cstdint>
#include <complex>
#include <cmath>
#include <numbers>
#include <memory>
#include <stdexcept>

namespace YYCFFT {

	namespace Utils {
		
		template<typename _TyIndex, size_t _N>
		inline constexpr bool IsPow2() {
			size_t N = _N;
			while (!(N & 1u)) {
				N >>= 1u;
			}
			return N == 1u;
		}

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

	template<typename _TyIndex, typename _TyFloat, size_t _N, std::enable_if_t<Utils::ValidateArgs<_TyIndex, _TyFloat, _N>::value, int> = 0>
	class Window {
	private:
		constexpr static _TyIndex N = _N;

	public:
		Window() : m_WindowData(nullptr) {
			// Pre-compute window data
			m_WindowData = std::make_unique<_TyFloat[]>(N);
			for (_TyIndex i = 0u; i < N; ++i) {
				m_WindowData[i] = static_cast<_TyFloat>(0.5) * 
					(static_cast<_TyFloat>(1.0) - std::cos(static_cast<_TyFloat>(2.0) * std::numbers::pi_v<_TyFloat> * static_cast<_TyFloat>(i) / static_cast<_TyFloat>(N - 1u)));
			}
		}

	private:
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
	};

	template<typename _TyIndex, typename _TyFloat, size_t _N, std::enable_if_t<Utils::ValidateArgs<_TyIndex, _TyFloat, _N>::value, int> = 0>
	class FFT {
	private:
		using _TyComplex = std::complex<_TyFloat>;
		constexpr static _TyIndex N = _N;
		constexpr static _TyIndex M = Utils::GetPow2Exponent<_TyIndex, _N>();
		constexpr static _TyIndex c_HalfPoint = _N >> 1u;

	public:
		FFT() : m_WNPCache(nullptr) {
			// Generate WNP cache
			m_WNPCache = std::make_unique<_TyComplex[]>(N);
			for (_TyIndex P = 0u; P < N; ++P) {
				_TyFloat angle = static_cast<_TyFloat>(2) * std::numbers::pi_v<_TyFloat> * static_cast<_TyFloat>(P) / static_cast<_TyFloat>(N);
                // e^(-jx) = cosx - j sinx
				m_WNPCache[P] = std::polar(static_cast<_TyFloat>(1u), angle);
			}
		}

	private:
		std::unique_ptr<_TyComplex[]> m_WNPCache;
	public:
		void Compute(_TyComplex* data) const {
			if (data == nullptr) [[unlikely]] {
				throw std::invalid_argument("nullptr data is not allowed for FFT computing.");
			}

			_TyIndex LH, J, K, B, P;
			LH = J = N >> 1u;

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
				B = 1u << (L - 1u);
				for (J = 0u; J <= B - 1u; ++J) {
					P = J * (1u << (M - L));
					
                    // Use pre-computed cache instead of real-time computing
					for (_TyIndex KK = J; KK <= N - 1; KK += (1u << L)) {
						temp2 = (data[KK + B] * this->m_WNPCache[P]);
						temp = temp2 + data[KK];
						data[KK + B] = data[KK] - temp2;
						data[KK] = temp;
					}
				}
			}
		}
	};

}
