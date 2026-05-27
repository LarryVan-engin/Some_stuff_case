import numpy as np
import matplotlib.pyplot as plt

def analyze_sin_signal(at_value, frequency=1, sampling_rate=1000, duration=1):
  """
  Phân tích tín hiệu 10 - 10sin(@πt).

  Args:
    at_value: Giá trị @.
    frequency: Tần số của tín hiệu (mặc định là 1 Hz).
    sampling_rate: Tần số lấy mẫu (mặc định là 1000 Hz).
    duration: Thời gian tín hiệu (mặc định là 1 giây).

  Returns:
    None
  """

  # Tạo tín hiệu thời gian
  time = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
  sin_signal = 10 - 10 * np.sin(at_value * np.pi * frequency * time)

  # Xác định phương trình
  print(f"Phương trình: 10 - 10sin({at_value}*pi*t)")

  # Tính giá trị trung bình
  mean_value = np.mean(sin_signal)
  print("Giá trị trung bình:", mean_value)

  # Tính năng lượng
  energy = np.sum(sin_signal**2) / sampling_rate
  print("Năng lượng:", energy)

  # Tính công suất
  power = energy / duration
  print("Công suất:", power)

  # Tính FFT để tìm phổ biên độ
  fft_result = np.fft.fft(sin_signal)
  freqs = np.fft.fftfreq(len(sin_signal), 1/sampling_rate)

  # Vẽ đồ thị phổ biên độ
  plt.plot(freqs, np.abs(fft_result))
  plt.xlabel('Tần số (Hz)')
  plt.ylabel('Biên độ')
  plt.title('Phổ biên độ')
  plt.show()

# Nhập giá trị @ từ người dùng
at_value = float(input("Nhập giá trị @: "))
if at_value < 9:
  at_value = at_value + 10
else :
  temp = at_value
  temp = temp/10
  at_value = 10**(temp+1) + at_value

# Gọi hàm phân tích tín hiệu
analyze_sin_signal(at_value)