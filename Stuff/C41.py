import numpy as np
import matplotlib.pyplot as plt

# Định nghĩa các tham số
fc = 1000  # Tần số sóng mang (Hz)
W = 100    # Băng thông tín hiệu băng gốc (Hz)

# Vẽ phổ biên độ của tín hiệu e(t)
f = np.linspace(-2*fc, 2*fc, 1000)
E = np.zeros_like(f)
E[np.abs(f - fc) < W] = 1
E[np.abs(f + fc) < W] = 1

plt.figure(figsize=(10, 4))
plt.plot(f, E)
plt.title('Phổ biên độ của tín hiệu e(t)')
plt.xlabel('Tần số (Hz)')
plt.ylabel('Biên độ')
plt.grid(True)
plt.show()

# Tính băng thông của bộ LPF
bandwidth_LPF = W
print("Băng thông của bộ LPF:", bandwidth_LPF, "Hz")

# Ứng dụng của hệ thống
application = """
Hệ thống điều chế sóng mang được sử dụng rộng rãi trong các hệ thống thông tin, như 
truyền hình, radio và viễn thông. Mục đích của việc điều chế là để truyền tải tín hiệu 
băng gốc thông qua sóng mang, giúp tăng khả năng chống nhiễu và cải thiện hiệu quả sử dụng 
băng tần. Sau khi nhận được tín hiệu, quá trình giải điều chế sẽ khôi phục lại tín hiệu 
gốc từ sóng mang.
"""
print(application)
