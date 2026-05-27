import numpy as np
import matplotlib.pyplot as plt

def analyze_sin_signal(amplitude, frequency=5, sampling_rate=1000, duration=1):
  """
  Phân tích tín hiệu sin(nt).

  Args:
    amplitude: Biên độ của tín hiệu.
    frequency: Tần số của tín hiệu (mặc định là 5 Hz).
    sampling_rate: Tần số lấy mẫu (mặc định là 1000 Hz).
    duration: Thời gian tín hiệu (mặc định là 1 giây).

  Returns:
    None
  """

  # Tạo tín hiệu thời gian
  time = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
  sin_signal = amplitude * np.sin(2 * np.pi * frequency * time)

  # Xác định phương trình
  print(f"Phương trình: {amplitude} * sin({frequency}*t)")

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

# Nhập biên độ từ người dùng
amplitude = float(input("Nhập biên độ: "))
if amplitude < 9:
  amplitude = amplitude + 10
else :
  temp = amplitude
  temp = temp/10
  amplitude = 10**(temp+1) + amplitude

# Gọi hàm phân tích tín hiệu
analyze_sin_signal(amplitude)