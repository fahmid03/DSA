import numpy as np
import matplotlib.pyplot as plt

# =========================================================================
# Part 1: SignalGenerator Class (OOP Framework)
# =========================================================================
class SignalGenerator:
    def __init__(self, t):
        self.t = t

    def gaussian(self, a):
        """Generates Gaussian signal: x(t) = exp(-a * t^2)"""
        return np.exp(-a * (self.t ** 2))

    def shift(self, signal_func, t0, *args, **kwargs):
        """
        Implements time shift y(t) = x(t - t0) using OOP framework 
        without manually shifting array elements.
        """
        t_shifted = self.t - t0
        # Re-evaluate the signal function at the shifted time grid
        return np.exp(-kwargs.get('a', 1) * (t_shifted ** 2)) if signal_func == 'gaussian' else None


# =========================================================================
# Continuous Fourier Transform Analyzer Class
# =========================================================================
class CFTAnalyzer:
    def __init__(self, f):
        self.f = f

    def compute_cft(self, signal, t):
        """
        Computes Continuous Fourier Transform using numerical integration.
        X(f) = integral(x(t) * exp(-j * 2 * pi * f * t) dt)
        """
        X_f = np.zeros(len(self.f), dtype=complex)
        for i, freq in enumerate(self.f):
            integrand = signal * np.exp(-1j * 2 * np.pi * freq * t)
            # Numerical integration via np.trapz (or np.trapezoid)
            X_f[i] = np.trapz(integrand, t)
        return X_f


# =========================================================================
# Main Execution Flow (Parts 2 - 6)
# =========================================================================
def main():
    # --- Part 2: Constructing Original Signal ---
    # Time axis: t in [-5, 5] with 2000 samples
    t = np.linspace(-5, 5, 2000)
    sig_gen = SignalGenerator(t)
    
    a = 1.0
    x_t = sig_gen.gaussian(a)  # x(t) = exp(-t^2)

    # --- Part 3: Time-Shifting the Signal ---
    t0 = 1.0
    y_t = sig_gen.shift('gaussian', t0, a=a)  # y(t) = x(t - 1)

    # --- Part 4 & 5: Frequency Setup & Continuous Fourier Transform ---
    # Frequency axis: f in [-10, 10] with 1000 samples
    f = np.linspace(-10, 10, 1000)
    analyzer = CFTAnalyzer(f)

    # Compute CFTs
    X_f = analyzer.compute_cft(x_t, t)
    Y_f = analyzer.compute_cft(y_t, t)

    # Magnitude Spectra
    mag_X = np.abs(X_f)
    mag_Y = np.abs(Y_f)

    # Phase Spectra
    phase_X = np.angle(X_f)
    phase_Y = np.angle(Y_f)

    # --- Part 6: Numerical Verification & Error Analysis ---
    # (a) MSE of Magnitude: MSE = (1/N) * sum(|X(f)| - |Y(f)|)^2
    mse_mag = np.mean((mag_X - mag_Y) ** 2)

    # (b) Predicted Phase according to property: angle(Y) = angle(X) - 2*pi*f*t0
    predicted_phase_Y = phase_X - (2 * np.pi * f * t0)
    
    # Wrap phase predicted difference into [-pi, pi] for fair comparison against np.angle()
    phase_diff = (phase_Y - predicted_phase_Y + np.pi) % (2 * np.pi) - np.pi
    mse_phase = np.mean(phase_diff ** 2)

    print("==========================================")
    print("           ERROR ANALYSIS METRICS         ")
    print("==========================================")
    print(f"Magnitude MSE (MSE_mag) : {mse_mag:.6e}")
    print(f"Phase MSE (MSE_phase)    : {mse_phase:.6e}")
    print("==========================================\n")

    # --- Plotting Results ---
    plt.figure(figsize=(12, 8))

    # 1. Magnitude Spectra
    plt.subplot(2, 1, 1)
    plt.plot(f, mag_X, 'b-', label='|X(f)| (Original)', linewidth=1.5)
    plt.plot(f, mag_Y, 'r--', label='|Y(f)| (Shifted)', linewidth=1.5)
    plt.title(f"Magnitude Spectra Comparison (MSE: {mse_mag:.2e})")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.legend()

    # 2. Phase Spectra
    plt.subplot(2, 1, 2)
    plt.plot(f, phase_Y, 'b-', label='Measured ∠Y(f)', linewidth=1.5)
    plt.plot(f, predicted_phase_Y, 'r--', label='Predicted: ∠X(f) - 2πf t₀', linewidth=1.5)
    plt.title(f"Phase Spectra Verification (MSE: {mse_phase:.2e})")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Phase (radians)")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
