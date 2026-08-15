import numpy as np


class CFT:
    """
    Continuous Fourier Transform calculator for sampled signals.

    Convention:
        X(f) = ∫ x(t) e^(-j 2πft) dt

        x(t) = ∫ X(f) e^(j 2πft) df
    """

    def __init__(self, t, x):
        self.t = np.asarray(t, dtype=float)
        self.x = np.asarray(x, dtype=complex)

        if self.t.ndim != 1 or self.x.ndim != 1:
            raise ValueError("t and x must be 1-D arrays.")

        if len(self.t) != len(self.x):
            raise ValueError("t and x must have the same length.")

        if len(self.t) < 2:
            raise ValueError("At least two samples are required.")

        self.dt = np.mean(np.diff(self.t))

    # ---------------------------------------------------------
    # Direct CFT
    # ---------------------------------------------------------

    def direct(self, frequencies):
        """
        Compute the CFT directly using numerical integration.

        X(f) = ∫ x(t)e^(-j2πft)dt

        Returns:
            X : complex array
        """

        frequencies = np.asarray(frequencies, dtype=float)

        # Shape:
        # frequencies[:, None] -> (Nf, 1)
        # t[None, :]           -> (1, Nt)
        #
        # Result                 -> (Nf, Nt)
        exponential = np.exp(
            -1j * 2 * np.pi * frequencies[:, None] * self.t[None, :]
        )

        integrand = exponential * self.x[None, :]

        # Integrate along time axis
        return np.trapezoid(integrand, self.t, axis=1)

    # ---------------------------------------------------------
    # Riemann-sum CFT
    # ---------------------------------------------------------

    def riemann(self, frequencies):
        """
        Compute the CFT using a simple Riemann sum.

        X(f) ≈ Σ x(t)e^(-j2πft) Δt
        """

        frequencies = np.asarray(frequencies, dtype=float)

        exponential = np.exp(
            -1j * 2 * np.pi * frequencies[:, None] * self.t[None, :]
        )

        return np.sum(
            self.x[None, :] * exponential,
            axis=1
        ) * self.dt

    # ---------------------------------------------------------
    # Inverse CFT
    # ---------------------------------------------------------

    def inverse(self, frequencies, X):
        """
        Reconstruct x(t) from X(f).

        x(t) = ∫ X(f)e^(j2πft)df
        """

        frequencies = np.asarray(frequencies, dtype=float)
        X = np.asarray(X, dtype=complex)

        if len(frequencies) != len(X):
            raise ValueError("frequencies and X must have the same length.")

        exponential = np.exp(
            1j * 2 * np.pi * self.t[:, None] * frequencies[None, :]
        )

        return np.trapezoid(
            X[None, :] * exponential,
            frequencies,
            axis=1
        )

    # ---------------------------------------------------------
    # FFT approximation
    # ---------------------------------------------------------

    def fft(self):
        """
        Compute the discrete Fourier transform using FFT.

        Returns:
            frequencies
            X
        """

        N = len(self.x)

        X = np.fft.fft(self.x)
        frequencies = np.fft.fftfreq(N, self.dt)

        # Shift zero frequency to center
        X = np.fft.fftshift(X)
        frequencies = np.fft.fftshift(frequencies)

        # Scale to approximate continuous FT
        X *= self.dt

        return frequencies, X

    # ---------------------------------------------------------
    # Magnitude and phase
    # ---------------------------------------------------------

    @staticmethod
    def magnitude(X):
        """Return magnitude spectrum."""

        return np.abs(X)

    @staticmethod
    def phase(X):
        """Return phase spectrum."""

        return np.angle(X)

    # ---------------------------------------------------------
    # MSE
    # ---------------------------------------------------------

    @staticmethod
    def mse(original, reconstructed):
        """
        Mean Squared Error.

        MSE = 1/N Σ |x[n] - x_hat[n]|²
        """

        original = np.asarray(original)
        reconstructed = np.asarray(reconstructed)

        if original.shape != reconstructed.shape:
            raise ValueError(
                "Original and reconstructed signals must have "
                "the same shape."
            )

        return np.mean(np.abs(original - reconstructed) ** 2)

    # ---------------------------------------------------------
    # Relative MSE
    # ---------------------------------------------------------

    @staticmethod
    def relative_mse(original, reconstructed):
        """
        MSE normalized by the energy of the original signal.
        """

        original = np.asarray(original)
        reconstructed = np.asarray(reconstructed)

        error = np.mean(np.abs(original - reconstructed) ** 2)
        energy = np.mean(np.abs(original) ** 2)

        if energy == 0:
            return 0.0

  
