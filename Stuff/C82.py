import numpy as np

# Các tham số
S_x = 0.4  # Công suất tín hiệu
S_R = 20e-9  # Công suất nhiễu (W)
W = 5e6  # Băng thông (Hz)
mu = 1  # Hệ số điều chế
N_0 = 10 * S_R / W  # Công suất nhiễu trên 1 Hz băng thông

# Tính toán tỷ lệ S/N trước giải điều chế
S_N_before = S_x / S_R

# Tính toán tỷ lệ S/N sau giải điều chế
S_N_after = S_N_before * mu**2 / 2

# Chuyển đổi tỷ lệ S/N sang đơn vị dB
S_N_dB = 10 * np.log10(S_N_after)

print(f"Tỷ lệ S/N_D ở đơn vị dB là: {S_N_dB:.2f} dB")
