import numpy as np
import matplotlib.pyplot as plt

# Định nghĩa các tín hiệu và thông số
t = np.linspace(0, 1, 1000)  # Thời gian (tính bằng ms)
x_t = 0.8 * np.cos(4 * np.pi * t)  # Tín hiệu cần điều chế
carrier = 10 * np.sin(2 * np.pi * t)  # Sóng mang

# a) Điều chế biên độ (AM)
mu = 0.5  # Chỉ số điều chế
s_t_am = (1 + mu * x_t) * carrier  # Tín hiệu sau điều chế AM

# Vẽ dạng sóng của tín hiệu sau điều chế AM
plt.figure(figsize=(10, 4))
plt.plot(t, s_t_am)
plt.title('Dạng sóng của tín hiệu sau điều chế AM')
plt.xlabel('Thời gian (ms)')
plt.ylabel('Biên độ')
plt.grid(True)
plt.show()

# b) Điều chế hai biên triệt sóng mang (DSB)
s_t_dsb = x_t * carrier  # Tín hiệu sau điều chế DSB
power_dsb = np.mean(s_t_dsb**2)  # Công suất của tín hiệu sau điều chế DSB
print("Công suất của tín hiệu sau điều chế DSB:", power_dsb)

# c) Điều chế biên trên (USSB)
s_t_ussb = x_t * np.cos(2 * np.pi * t) - np.sin(4 * np.pi * t) * np.sin(2 * np.pi * t)
# Biểu thức theo thời gian của tín hiệu sau điều chế USSB
t_2019 = 20.19 / 1000  # Thời điểm 20.19 ms chuyển thành giây
ussb_value = 0.8 * np.cos(4 * np.pi * t_2019) * np.cos(2 * np.pi * t_2019) - np.sin(4 * np.pi * t_2019) * np.sin(2 * np.pi * t_2019)
print("Giá trị của tín hiệu USSB tại t = 20.19 ms:", ussb_value)

# d) Thiết kế sơ đồ nguyên lý điều chế DSB
# Mô tả: Sử dụng các bộ điều chế AM, bộ tạo sóng mang, bộ khuếch đại và bộ cộng để thực hiện điều chế DSB.

print("""
Thiết kế sơ đồ nguyên lý điều chế DSB:
1. Bộ điều chế AM với chỉ số điều chế \(\mu\) và bộ tạo sóng mang nằm trong bộ điều chế.
2. Bộ khuếch đại để tăng biên độ của tín hiệu.
3. Bộ cộng để kết hợp tín hiệu điều chế AM và tín hiệu sóng mang.
""")
