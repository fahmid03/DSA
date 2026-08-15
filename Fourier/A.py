import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Setup Grids
# ---------------------------------------------------------
# Time grid (long enough window to approximate continuous integral)
t = np.linspace(-5, 5, 2000)

# Frequency grid (Hz)
f = np.linspace(-2, 2, 1000)

# ---------------------------------------------------------
# 1. Define Signals and Derivatives
# ---------------------------------------------------------
x = 0.5 * np.cos(4 * t) + 0.5 * np.sin(6 * t)
y1 = -2 * np.sin(4 * t) + 3 * np.cos(6 * t)
y2 = -8 * np.cos(4 * t) - 18 * np.sin(6 * t)
y3 = 8 * np.sin(4 * t) - 108 * np.cos(6 * t)

# ---------------------------------------------------------
# 2. CFT Function using Trapezoidal Integration
# ---------------------------------------------------------
def compute_cft(signal, t_grid, f_grid):
    X_f = np.zeros(len(f_grid), dtype=complex)
    for i, freq in enumerate(f_grid):
        integrand = signal * np.exp(-1j * 2 * np.pi * freq * t_grid)
        # Using np.trapz (or np.trapezoid for newer NumPy versions)
        X_f[i] = np.trapz(integrand, t_grid)
    return X_f

# Compute X(f)
X_f = compute_cft(x, t, f)

# List of direct derivatives and their names
derivatives = [
    (1, y1, "1st Derivative"),
    (2, y2, "2nd Derivative"),
    (3, y3, "3rd Derivative")
]

# ---------------------------------------------------------
# 3. Compute CFTs, MSE, and Plotting
# ---------------------------------------------------------
plt.figure(figsize=(14, 10))

for k, y_k, title in derivatives:
    # Direct CFT of y_k(t)
    Y_direct = compute_cft(y_k, t, f)
    
    # Property CFT: (j * 2 * pi * f)^k * X(f)
    Y_prop = ((1j * 2 * np.pi * f) ** k) * X_f
    
    # Magnitude & Phase
    mag_direct = np.abs(Y_direct)
    mag_prop = np.abs(Y_prop)
    
    phase_direct = np.angle(Y_direct)
    phase_prop = np.angle(Y_prop)
    
    # MSE Calculation
    mse_mag = np.mean((mag_direct - mag_prop) ** 2)
    mse_phase = np.mean((phase_direct - phase_prop) ** 2)
    
    print(f"=== {title} MSE Analysis ===")
    print(f"Magnitude MSE : {mse_mag:.6e}")
    print(f"Phase MSE     : {mse_phase:.6e}\n")
    
    # Plot Magnitude Comparison
    plt.subplot(3, 2, 2*k - 1)
    plt.plot(f, mag_direct, 'b-', label='|Y_direct(f)|')
    plt.plot(f, mag_prop, 'r--', label='|(j2πf)^k X(f)|')
    plt.title(f"{title} Magnitude Comparison (MSE: {mse_mag:.2e})")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.legend()
    plt.grid(True)
    
    # Plot Phase Comparison
    plt.subplot(3, 2, 2*k)
    plt.plot(f, phase_direct, 'b-', label='Phase Direct')
    plt.plot(f, phase_prop, 'r--', label='Phase Property')
    plt.title(f"{title} Phase Comparison (MSE: {mse_phase:.2e})")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Phase (rad)")
    plt.legend()
    plt.grid(True)

plt.tight_layout()
plt.show()
