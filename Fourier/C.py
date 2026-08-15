import numpy as np
import matplotlib.pyplot as plt

# =========================================================================
# Signal Generator Class (OOP Framework)
# =========================================================================
class SignalGenerator:
    def __init__(self, t):
        self.t = t

    def square_wave(self, t_grid):
        """Standard square pulse of width 1 centered at 0: rect(t)"""
        return np.where(np.abs(t_grid) <= 0.5, 1.0, 0.0)

    def triangle_wave(self, t_grid):
        """Standard triangle pulse of width 1 centered at 0: tri(t)"""
        return np.maximum(0.0, 1.0 - np.abs(t_grid))

    def original_signal(self, t_grid):
        """x(t) = Square(t) + Triangle(t)"""
        return self.square_wave(t_grid) + self.triangle_wave(t_grid)

    def modified_signal(self, f0, a):
        """
        y(t) = x(a * t) * exp(j * 2 * pi * f0 * t)
        Combines time-scaling (compression by a) and phase-shifting (frequency shift by f0).
        """
        t_scaled = a * self.t
        x_at = self.original_signal(t_scaled)
        phase_shift = np.exp(1j * 2 * np.pi * f0 * self.t)
        return x_at * phase_shift


# =========================================================================
# CFT Analyzer Class
# =========================================================================
class CFTAnalyzer:
    def __init__(self, f):
        self.f = f

    def compute_cft(self, signal, t):
        """
        Computes Continuous Fourier Transform using numerical trapezoidal integration.
        X(f) = integral( x(t) * exp(-j * 2 * pi * f * t) dt )
        """
        X_f = np.zeros(len(self.f), dtype=complex)
        for i, freq in enumerate(self.f):
            integrand = signal * np.exp(-1j * 2 * np.pi * freq * t)
            # Use np.trapz (or np.trapezoid in newer NumPy versions)
            X_f[i] = np.trapz(integrand, t)
        return X_f


# =========================================================================
# Main Execution Flow
# =========================================================================
def main():
    # --- Time Axis Setup ---
    # t in [-5, 5] with 2000 samples
    t = np.linspace(-5, 5, 2000)
    sig_gen = SignalGenerator(t)

    # Signal Parameters
    f0 = 10.0  # Frequency shift unit
    a = 10.0   # Time compression factor

    # Generate signals
    x_t = sig_gen.original_signal(t)
    y_t = sig_gen.modified_signal(f0=f0, a=a)

    # --- Frequency Axis Setup ---
    # f in [-10, 10] with 1000 samples
    f = np.linspace(-10, 10, 1000)
    analyzer = CFTAnalyzer(f)

    # Compute Direct CFTs
    X_f = analyzer.compute_cft(x_t, t)
    Y_f = analyzer.compute_cft(y_t, t)

    # --- Compute Theoretical Spectrum using Property ---
    # Property: Y_prop(f) = (1 / |a|) * X((f - f0) / a)
    # We evaluate the original signal's CFT at shifted/scaled frequencies: f_prop = (f - f0) / a
    f_prop = (f - f0) / a
    analyzer_prop = CFTAnalyzer(f_prop)
    X_scaled_shifted = analyzer_prop.compute_cft(x_t, t)
    
    Y_prop = (1.0 / np.abs(a)) * X_scaled_shifted

    # --- Magnitudes and Phases ---
    mag_Y = np.abs(Y_f)
    mag_prop = np.abs(Y_prop)

    phase_Y = np.angle(Y_f)
    phase_prop = np.angle(Y_prop)

    # --- Error Analysis (MSE) ---
    mse_mag = np.mean((mag_Y - mag_prop) ** 2)
    
    # Wrap phase differences into [-pi, pi] for accurate MSE computation
    phase_diff = (phase_Y - phase_prop + np.pi) % (2 * np.pi) - np.pi
    mse_phase = np.mean(phase_diff ** 2)

    print("==========================================")
    print("           ERROR ANALYSIS METRICS         ")
    print("==========================================")
    print(f"Magnitude MSE (MSEmagnitude) : {mse_mag:.6e}")
    print(f"Phase MSE (MSEphase)         : {mse_phase:.6e}")
    print("==========================================\n")

    # --- Numerical Verification & Plotting ---
    plt.figure(figsize=(12, 8))

    # 1. Magnitude Spectrum Plot
    plt.subplot(2, 1, 1)
    plt.plot(f, mag_Y, 'b-', label='|Y(f)| (Direct CFT)', linewidth=1.5)
    plt.plot(f, mag_prop, 'r--', label='(1/|a|) * |X((f-f0)/a)| (Property)', linewidth=1.5)
    plt.title(f"Magnitude Spectrum Verification (MSE: {mse_mag:.2e})")
    plt.xlabel("Frequency (f)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.legend()

    # 2. Phase Spectrum Plot
    plt.subplot(2, 1, 2)
    plt.plot(f, phase_Y, 'b-', label='∠Y(f) (Direct CFT)', linewidth=1.5)
    plt.plot(f, phase_prop, 'r--', label='∠X((f-f0)/a) (Property)', linewidth=1.5)
    plt.title(f"Phase Spectrum Verification (MSE: {mse_phase:.2e})")
    plt.xlabel("Frequency (f)")
    plt.ylabel("Phase (radians)")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
