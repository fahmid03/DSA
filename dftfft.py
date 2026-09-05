import numpy as np

def next_power_of_two(n):
    """Returns the smallest power of 2 greater than or equal to n."""
    return 1 << (n - 1).bit_length()

def multiply_large_integers(A, B):
    """
    Multiplies two large integers given as LSD-first digit arrays 
    using FFT-based circular convolution and carry propagation.
    """
    if not A or not B or A == [0] or B == [0]:
        return [0]
        
    m = len(A)
    n = len(B)
    
    # Step 1: Determine required length for linear convolution
    conv_len = m + n - 1
    N = next_power_of_two(conv_len)
    
    # Step 2: Zero-pad both arrays to length N
    A_padded = np.pad(A, (0, N - m), 'constant')
    B_padded = np.pad(B, (0, N - n), 'constant')
    
    # Step 3: Transform to frequency domain, multiply, and inverse transform
    FA = np.fft.fft(A_padded)
    FB = np.fft.fft(B_padded)
    C_freq = FA * FB
    C_spatial = np.fft.ifft(C_freq)
    
    # Convert floating-point results back to clean integers (rounding handles precision drift)
    C_raw = np.round(C_spatial.real).astype(np.int64)
    
    # Step 4: Carry Propagation
    carry = 0
    result = []
    for val in C_raw:
        total = val + carry
        result.append(int(total % 10))
        carry = int(total // 10)
        
    while carry > 0:
        result.append(int(carry % 10))
        carry //= 10
        
    # Remove any redundant trailing zero padding, keeping at least [0] if empty
    while len(result) > 1 and result[-1] == 0:
        result.pop()
        
    return result

# --- Testing with the Example Inputs ---
if __name__ == "__main__":
    # Example 1: 123 * 45
    A1 = [3, 2, 1]
    B1 = [5, 4]
    print("Example 1 Result:", multiply_large_integers(A1, B1))  # Expected: [5, 3, 5, 5]
    
    # Example 2: 999 * 99
    A2 = [9, 9, 9]
    B2 = [9, 9]
    print("Example 2 Result:", multiply_large_integers(A2, B2))  # Expected: [1, 0, 9, 8, 9]

#---------------------------------------------------------------------first

import math
import cmath


def fft(a):
    """Computes the Fast Fourier Transform (Cooley-Tukey radix-2 algorithm)."""
    n = len(a)
    if n <= 1:
        return a
    
    # Divide into even and odd parts
    even = fft(a[0::2])
    odd = fft(a[1::2])
    
    # Combine
    half = n // 2
    T = [cmath.exp(-2j * math.pi * k / n) * odd[k] for k in range(half)]
    
    return [even[k] + T[k] for k in range(half)] + [even[k] - T[k] for k in range(half)]


def ifft(a):
    """Computes the Inverse Fast Fourier Transform using the FFT conjugate trick."""
    n = len(a)
    # Conjugate the input
    conjugated = [x.conjugate() for x in a]
    # Apply FFT
    transformed = fft(conjugated)
    # Conjugate again and scale by 1/n
    return [x.conjugate() / n for x in transformed]


def next_power_of_two(n):
    """Returns the smallest power of 2 greater than or equal to n."""
    return 1 << (n - 1).bit_length()


def weighted_polynomial_multiply(P, Q, W):
    """
    Computes the weighted polynomial product R(x) where R[k] = sum(w_i * p_i * q_{k-i})
    using custom FFT/IFFT-based circular convolution.
    """
    # Step 1: Pre-multiply P and W element-wise: P'[i] = p_i * w_i
    P_prime = [p * w for p, w in zip(P, W)]
    
    # Step 2: Determine lengths and required size for linear convolution
    len_p = len(P_prime)
    len_q = len(Q)
    conv_len = len_p + len_q - 1
    N = next_power_of_two(conv_len)
    
    # Step 3: Zero-pad P_prime and Q to size N
    P_padded = P_prime + [0] * (N - len_p)
    Q_padded = Q + [0] * (N - len_q)
    
    # Step 4: Transform to frequency domain, multiply pointwise, and inverse transform
    FP = fft(P_padded)
    FQ = fft(Q_padded)
    R_freq = [FP[i] * FQ[i] for i in range(N)]
    R_spatial = ifft(R_freq)
    
    # Step 5: Extract the relevant coefficients and round to integers
    result = [round(val.real) for val in R_spatial[:conv_len]]
    
    return result
    

if __name__ == "__main__":
    P = [1, 3, 2, 6, 7]
    Q = [4, 1]
    W = [3, 2, 1, 5, 6]
 
    R = weighted_polynomial_multiply(P, Q, W)

    print("Result:", R)

#-------------------------------------------second

import cv2
import numpy as np
import math
import cmath

def fft(a):
    """
    Compute 1D FFT using the Cooley-Tukey radix-2 algorithm.
    """
    n = len(a)
    if n <= 1:
        return list(a)
    
    # Divide into even and odd parts
    even = fft(a[0::2])
    odd = fft(a[1::2])
    
    # Combine
    half = n // 2
    T = [cmath.exp(-2j * math.pi * k / n) * odd[k] for k in range(half)]
    
    return [even[k] + T[k] for k in range(half)] + [even[k] - T[k] for k in range(half)]

def ifft(X):
    """
    Compute 1D inverse FFT using the FFT function via the conjugate trick.
    """
    n = len(X)
    conjugated = [x.conjugate() for x in X]
    transformed = fft(conjugated)
    return [x.conjugate() / n for x in transformed]

def reconstruct_image_using_fft(original_path, shifted_path, output_path):
    original_img = cv2.imread(original_path)
    shifted_img = cv2.imread(shifted_path)

    if original_img is None or shifted_img is None:
        print("Error: Could not load images.")
        return

    if original_img.shape != shifted_img.shape:
        print("Error: Image dimensions do not match.")
        return
    
    # Convert the original and shifted color images to grayscale for shift detection.
    orig_gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    shift_gray = cv2.cvtColor(shifted_img, cv2.COLOR_BGR2GRAY)
    
    height, width = orig_gray.shape
    reconstructed_img = np.zeros_like(shifted_img)

    print("Reconstructing image using manual FFT...")

    # Process each row independently to find shifts and reverse them
    for r in range(height):
        orig_row = [float(val) for val in orig_gray[r]]
        shift_row = [float(val) for val in shift_gray[r]]
        
        # 1. Transform both rows to the frequency domain
        F = fft(orig_row)
        G = fft(shift_row)
        
        # 2. DFT-based cross-correlation: G * conj(F)
        corr_freq = [G[k] * F[k].conjugate() for k in range(width)]
        corr_spatial = ifft(corr_freq)
        
        # 3. Find the shift amount via the maximum peak index
        shift = int(np.argmax([val.real for val in corr_spatial]))
        
        # 4. Reverse the shift for all color channels of the current row
        reconstructed_img[r] = np.roll(shifted_img[r], -shift, axis=0)

    cv2.imwrite(output_path, reconstructed_img)
    print(f"Reconstruction complete. Saved to {output_path}")
    
if __name__ == "__main__":
    reconstruct_image_using_fft("original_image.png", "shifted_image.jpg", "reconstructed_image_fft.jpg")

#-------------------------------------------thirs
