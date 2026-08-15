import numpy as np
import matplotlib.pyplot as plt
from cft_edge_detector import ContinuousImage, CFT2D, InverseCFT2D


class FourierPropertiesDemo:
    """
    Demonstrates fundamental 2D Continuous Fourier Transform properties
    using simple, easy-to-read Python code.
    """

    @staticmethod
    def plot_subplots(title, images, subtitles):
        """Helper function to plot multiple images side-by-side using Matplotlib subplots."""
        num_images = len(images)
        plt.figure(figsize=(4 * num_images, 4))
        plt.suptitle(title, fontsize=14, fontweight="bold")

        for i in range(num_images):
            plt.subplot(1, num_images, i + 1)
            plt.imshow(images[i], cmap="gray", origin="lower")
            plt.title(subtitles[i])
            plt.axis("off")

        plt.tight_layout()
        plt.show()

    # =========================================================================
    # 1. SPATIAL SHIFT PROPERTY: f(x - x0, y - y0) <---> F(u, v) * exp(-j 2pi (u x0 + v y0))
    # Shifting an image in space only adds a linear phase shift; magnitude stays identical!
    # =========================================================================
    @staticmethod
    def demo_spatial_shift(cft_obj: CFT2D, x0=0.2, y0=0.3):
        # 1. Compute original spectrum
        real, imag = cft_obj.compute_cft()

        # 2. Apply spatial shift theorem directly to the frequency domain
        # F_shifted(u, v) = F(u, v) * exp(-j * 2 * pi * (u*x0 + v*y0))
        shift_real = np.zeros_like(real)
        shift_imag = np.zeros_like(imag)

        for v_idx, v_val in enumerate(cft_obj.v):
            for u_idx, u_val in enumerate(cft_obj.u):
                # Calculate shift phase angle
                angle = -2 * np.pi * (u_val * x0 + v_val * y0)
                cos_angle = np.cos(angle)
                sin_angle = np.sin(angle)

                # Complex multiplication: (R + jI) * (cos + j sin)
                r = real[v_idx, u_idx]
                i = imag[v_idx, u_idx]
                shift_real[v_idx, u_idx] = r * cos_angle - i * sin_angle
                shift_imag[v_idx, u_idx] = r * sin_angle + i * cos_angle

        # 3. Reconstruct shifted image back to spatial domain
        icft = InverseCFT2D(shift_real, shift_imag, cft_obj.u, cft_obj.v, cft_obj.x, cft_obj.y)
        shifted_image = icft.reconstruct()

        # 4. Plot original vs shifted image and magnitude spectrums
        mag_orig = np.log(1 + np.sqrt(real ** 2 + imag ** 2))
        mag_shift = np.log(1 + np.sqrt(shift_real ** 2 + shift_imag ** 2))

        FourierPropertiesDemo.plot_subplots(
            "Spatial Shift Property",
            [cft_obj.I, shifted_image, mag_orig, mag_shift],
            ["Original Image", f"Shifted ({x0}, {y0})", "Original Mag Spectrum", "Shifted Mag Spectrum (Identical!)"]
        )

    # =========================================================================
    # 2. REVERSAL PROPERTY: f(-x, -y) <---> F(-u, -v)
    # Reversing an image in space reverses its frequency spectrum.
    # =========================================================================
    @staticmethod
    def demo_reversal(cft_obj: CFT2D):
        # 1. Reverse the image spatially: f(-x, -y)
        reversed_image = np.flip(cft_obj.I)

        # 2. Compute CFT of original and reversed images
        real_orig, imag_orig = cft_obj.compute_cft()

        # Temporarily swap image inside CFT object to compute reversed image spectrum
        cft_obj.I = reversed_image
        real_rev, imag_rev = cft_obj.compute_cft()
        cft_obj.I = np.flip(reversed_image)  # restore original image

        # 3. Reconstruct reversed image back
        icft = InverseCFT2D(real_rev, imag_rev, cft_obj.u, cft_obj.v, cft_obj.x, cft_obj.y)
        reconstructed_reversed = icft.reconstruct()

        FourierPropertiesDemo.plot_subplots(
            "Spatial Reversal Property",
            [cft_obj.I, reversed_image, reconstructed_reversed],
            ["Original Image f(x,y)", "Reversed Image f(-x,-y)", "Reconstructed f(-x,-y)"]
        )

    # =========================================================================
    # 3. LINEARITY (SUPERPOSITION) PROPERTY: a*f1(x,y) + b*f2(x,y) <---> a*F1(u,v) + b*F2(u,v)
    # The Fourier transform of a weighted sum equals the weighted sum of their transforms.
    # =========================================================================
    @staticmethod
    def demo_linearity(cft_obj1: CFT2D, cft_obj2: CFT2D, a=0.6, b=0.4):
        # Compute individual CFTs
        real1, imag1 = cft_obj1.compute_cft()
        real2, imag2 = cft_obj2.compute_cft()

        # Linear combination in Frequency domain
        combined_real = a * real1 + b * real2
        combined_imag = a * imag1 + b * imag2

        # Reconstruct from combined spectrum
        icft = InverseCFT2D(combined_real, combined_imag, cft_obj1.u, cft_obj1.v, cft_obj1.x, cft_obj1.y)
        combined_reconstructed = icft.reconstruct()

        # Direct spatial combination for comparison
        combined_spatial = a * cft_obj1.I + b * cft_obj2.I

        FourierPropertiesDemo.plot_subplots(
            "Linearity (Superposition) Property",
            [cft_obj1.I, cft_obj2.I, combined_spatial, combined_reconstructed],
            ["Image 1", "Image 2", "Spatial Blend (a*I1 + b*I2)", "Spectrum Blend ICFT(a*F1 + b*F2)"]
        )

    # =========================================================================
    # 4. PARSEVAL'S THEOREM (ENERGY CONSERVATION): Integral |f(x,y)|^2 dx dy = Integral |F(u,v)|^2 du dv
    # Total energy in the spatial domain equals total energy in the frequency domain.
    # =========================================================================
    @staticmethod
    def demo_parseval(cft_obj: CFT2D):
        real, imag = cft_obj.compute_cft()

        # 1. Spatial Domain Energy
        spatial_power = cft_obj.I ** 2
        spatial_energy = np.trapezoid(np.trapezoid(spatial_power, cft_obj.x, axis=1), cft_obj.y, axis=0)

        # 2. Frequency Domain Energy
        freq_power = real ** 2 + imag ** 2
        freq_energy = np.trapezoid(np.trapezoid(freq_power, cft_obj.u, axis=1), cft_obj.v, axis=0)

        print("\n--- Parseval's Energy Conservation ---")
        print(f"Spatial Domain Energy:   {spatial_energy:.6f}")
        print(f"Frequency Domain Energy: {freq_energy:.6f}")
        print(f"Difference:              {abs(spatial_energy - freq_energy):.6e}")


# =========================================================================
# QUICK TEST SCRIPT
# =========================================================================
if __name__ == "__main__":
    # Create a simple synthetic square test image (32x32)
    grid = np.linspace(-1, 1, 32)
    X, Y = np.meshgrid(grid, grid)
    square_img = np.where((np.abs(X) < 0.4) & (np.abs(Y) < 0.4), 1.0, 0.0)


    # Wrap inside dummy ContinuousImage container
    class SimpleImage:
        def __init__(self, img_array, spatial_grid):
            self.image = img_array
            self.x = spatial_grid
            self.y = spatial_grid


    img_obj = SimpleImage(square_img, grid)
    cft = CFT2D(img_obj)

    print("Testing CFT Properties...")

    # Run Property Demos
    FourierPropertiesDemo.demo_spatial_shift(cft, x0=0.2, y0=0.1)
    FourierPropertiesDemo.demo_reversal(cft)
    FourierPropertiesDemo.demo_parseval(cft)

    import numpy as np
    import matplotlib.pyplot as plt
    from fs_redrawer import FourierEpicycles
    from svg_utils import load_svg_path


    class EpicyclePropertiesDemo:
        """
        Demonstrates fundamental 1D Complex Fourier Series properties
        using simple, easy-to-read Python code on FourierEpicycles.
        """

        @staticmethod
        def plot_subplots(title, times, signals, subtitles):
            """Helper function to plot multiple 2D shapes (complex signals) side-by-side."""
            num_signals = len(signals)
            plt.figure(figsize=(4 * num_signals, 4))
            plt.suptitle(title, fontsize=14, fontweight="bold")

            for i in range(num_signals):
                plt.subplot(1, num_signals, i + 1)
                sig = signals[i]
                # Plot real vs imaginary parts (X vs Y coordinates)
                plt.plot(sig.real, sig.imag, linewidth=2)
                plt.title(subtitles[i])
                plt.axis("equal")
                plt.grid(True, linestyle="--", alpha=0.5)

            plt.tight_layout()
            plt.show()

        # =========================================================================
        # 1. TIME SHIFT PROPERTY: f(t - t0) <---> c_n * exp(-j * n * omega * t0)
        # Shifting the timing of a path rotates each harmonic coefficient by -n*omega*t0.
        # The geometric shape stays identical, but the starting point moves!
        # =========================================================================
        @staticmethod
        def demo_time_shift(fs_obj: FourierEpicycles, t0=1.0):
            # 1. Calculate original coefficients
            fs_obj.calculate_all_coefficients()

            # 2. Shift coefficients analytically using the property
            shifted_coeffs = {}
            for n, c_n in fs_obj.coeffs.items():
                # Multiply c_n by phase shift: exp(-j * n * omega * t0)
                phase_factor = np.exp(-1j * n * fs_obj.omega * t0)
                shifted_coeffs[n] = c_n * phase_factor

            # 3. Reconstruct original vs shifted signals
            z_orig = fs_obj.approximate(fs_obj.t)

            # Temporarily swap coefficients to approximate shifted signal
            original_coeffs = fs_obj.coeffs
            fs_obj.coeffs = shifted_coeffs
            z_shifted = fs_obj.approximate(fs_obj.t)
            fs_obj.coeffs = original_coeffs  # restore original

            EpicyclePropertiesDemo.plot_subplots(
                "Time Shift Property",
                fs_obj.t,
                [z_orig, z_shifted],
                ["Original Reconstruction", f"Time-Shifted by t0={t0} (Same Shape)"]
            )

        # =========================================================================
        # 2. TIME REVERSAL PROPERTY: f(-t) <---> c_{-n}
        # Reversing time flips the drawing direction and mirrors negative/positive harmonics.
        # =========================================================================
        @staticmethod
        def demo_time_reversal(fs_obj: FourierEpicycles):
            fs_obj.calculate_all_coefficients()

            # Reverse coefficients: new_c_n = old_c_{-n}
            reversed_coeffs = {}
            for n in fs_obj.coeffs.keys():
                reversed_coeffs[n] = fs_obj.coeffs[-n]

            # Reconstruct
            z_orig = fs_obj.approximate(fs_obj.t)

            original_coeffs = fs_obj.coeffs
            fs_obj.coeffs = reversed_coeffs
            z_reversed = fs_obj.approximate(fs_obj.t)
            fs_obj.coeffs = original_coeffs  # restore

            EpicyclePropertiesDemo.plot_subplots(
                "Time Reversal Property",
                fs_obj.t,
                [z_orig, z_reversed],
                ["Original Path f(t)", "Time-Reversed Path f(-t)"]
            )

        # =========================================================================
        # 3. LINEARITY (SUPERPOSITION) PROPERTY: a*f1(t) + b*f2(t) <---> a*c_n^(1) + b*c_n^(2)
        # Scaling or adding paths in space adds their Fourier coefficients linearly.
        # =========================================================================
        @staticmethod
        def demo_linearity(fs_obj1: FourierEpicycles, fs_obj2: FourierEpicycles, a=0.7, b=0.3):
            fs_obj1.calculate_all_coefficients()
            fs_obj2.calculate_all_coefficients()

            # Combine coefficients linearly: c_n_combined = a * c_n1 + b * c_n2
            combined_coeffs = {}
            for n in fs_obj1.coeffs.keys():
                combined_coeffs[n] = a * fs_obj1.coeffs[n] + b * fs_obj2.coeffs[n]

            # Reconstruct from combined coefficients
            original_coeffs = fs_obj1.coeffs
            fs_obj1.coeffs = combined_coeffs
            z_combined_freq = fs_obj1.approximate(fs_obj1.t)
            fs_obj1.coeffs = original_coeffs  # restore

            # Direct spatial combination
            z1 = fs_obj1.approximate(fs_obj1.t)
            z2 = fs_obj2.approximate(fs_obj2.t)
            z_combined_spatial = a * z1 + b * z2

            EpicyclePropertiesDemo.plot_subplots(
                "Linearity (Superposition) Property",
                fs_obj1.t,
                [z1, z2, z_combined_spatial, z_combined_freq],
                ["Shape 1", "Shape 2", "Spatial Blend (a*z1 + b*z2)", "Spectrum Blend ICFT(a*c1 + b*c2)"]
            )

        # =========================================================================
        # 4. PARSEVAL'S THEOREM: (1/T) Integral |f(t)|^2 dt = Sum |c_n|^2
        # The total signal power in time domain equals the sum of powers of all harmonics.
        # =========================================================================
        @staticmethod
        def demo_parseval(fs_obj: FourierEpicycles):
            fs_obj.calculate_all_coefficients()

            # 1. Time-Domain Power: (1/T) * integral_0^T |f(t)|^2 dt
            signal_power = np.abs(fs_obj.signal) ** 2
            time_domain_energy = (1 / fs_obj.T) * np.trapezoid(signal_power, fs_obj.t)

            # 2. Frequency-Domain Power: Sum_{-N}^{N} |c_n|^2
            freq_domain_energy = 0.0
            for c_n in fs_obj.coeffs.values():
                freq_domain_energy += np.abs(c_n) ** 2

            print("\n--- Parseval's Energy Conservation (1D Fourier Series) ---")
            print(f"Time-Domain Average Power:      {time_domain_energy:.6f}")
            print(f"Frequency-Domain Total Power:   {freq_domain_energy:.6f}")
            print(f"Difference (Truncation Error):  {abs(time_domain_energy - freq_domain_energy):.6e}")


    # =========================================================================
    # QUICK TEST SCRIPT
    # =========================================================================
    if __name__ == "__main__":
        # Create a simple synthetic 1D closed signal (a circle + triangle wobble)
        t = np.linspace(0, 2 * np.pi, 1000)
        complex_path = np.exp(1j * t) + 0.3 * np.exp(-2j * t)

        # Instantiate FourierEpicycles object
        fs = FourierEpicycles(t, complex_path, n_harmonics=20)

        print("Testing 1D Fourier Epicycle Properties...")

        # Run Property Demos
        EpicyclePropertiesDemo.demo_time_shift(fs, t0=1.5)
        EpicyclePropertiesDemo.demo_time_reversal(fs)
        EpicyclePropertiesDemo.demo_parseval(fs)