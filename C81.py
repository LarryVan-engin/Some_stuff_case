import numpy as np
import matplotlib.pyplot as plt

# Định nghĩa tín hiệu gốc
t = np.linspace(0, 1, 1000)  # Thời gian (s)
f0 = 30  # Tần số tín hiệu gốc (Hz)
x_t = 2 * np.cos(2 * np.pi * f0 * t)  # Tín hiệu gốc

# Thông số lấy mẫu
fs_ideal = 120  # Tần số lấy mẫu lý tưởng (Hz)
fs_prac = 70    # Tần số lấy mẫu thực tế (Hz)
fs_filter = 50  # Tần số lấy mẫu qua bộ lọc (Hz)

# Hình 6a: Lấy mẫu bằng bộ lấy mẫu lý tưởng
t_ideal = np.arange(0, 1, 1/fs_ideal)
x_s_ideal = 2 * np.cos(2 * np.pi * f0 * t_ideal)

# Hình 6b: Lấy mẫu bằng bộ lấy mẫu thực tế
t_prac = np.arange(0, 1, 1/fs_prac)
x_s_prac = 2 * np.cos(2 * np.pi * f0 * t_prac)

# Hình 6c: Lấy mẫu bằng bộ lấy mẫu lý tưởng và qua hệ thống có đáp ứng xung
t_filter = np.arange(0, 1, 1/fs_filter)
x_s_filter = 2 * np.cos(2 * np.pi * f0 * t_filter)

# Phổ biên độ từ 0 đến 100Hz
frequencies = np.linspace(0, 100, 1000)

# Hàm tính phổ biên độ
def amplitude_spectrum(x_s, fs):
    n = len(x_s)
    f = np.fft.fftfreq(n, d=1/fs)
    X = np.fft.fft(x_s)
    X_amplitude = np.abs(X[:n//2]) * 2 / n
    f_positive = f[:n//2]
    return f_positive, X_amplitude

# Vẽ phổ biên độ cho các trường hợp
plt.figure(figsize=(10, 12))

# Hình 6a
f_ideal, X_ideal = amplitude_spectrum(x_s_ideal, fs_ideal)
plt.subplot(3, 1, 1)
plt.plot(f_ideal, X_ideal)
plt.title('Phổ biên độ của tín hiệu sau lấy mẫu lý tưởng (Hình 6a)')
plt.xlabel('Tần số (Hz)')
plt.ylabel('Biên độ')
plt.grid(True)

# Hình 6b
f_prac, X_prac = amplitude_spectrum(x_s_prac, fs_prac)
plt.subplot(3, 1, 2)
plt.plot(f_prac, X_prac)
plt.title('Phổ biên độ của tín hiệu sau lấy mẫu thực tế (Hình 6b)')
plt.xlabel('Tần số (Hz)')
plt.ylabel('Biên độ')
plt.grid(True)

# Hình 6c
f_filter, X_filter = amplitude_spectrum(x_s_filter, fs_filter)
plt.subplot(3, 1, 3)
plt.plot(f_filter, X_filter)
plt.title('Phổ biên độ của tín hiệu sau lấy mẫu và qua bộ lọc (Hình 6c)')
plt.xlabel('Tần số (Hz)')
plt.ylabel('Biên độ')
plt.grid(True)

plt.tight_layout()
plt.show()
