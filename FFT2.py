import numpy as np
import matplotlib.pyplot as plt

def analyze_signal(amplitude, frequency=5, sampling_rate=1000, duration=1):
  """
  Phân tích tín hiệu cos^3.

  Args:
    phương trình 1@.cos^3(10nt) 
    amplitude: Biên độ của tín hiệu.
    frequency: Tần số của tín hiệu (mặc định là 5 Hz).
    sampling_rate: Tần số lấy mẫu (mặc định là 1000 Hz).
    duration: Thời gian tín hiệu (mặc định là 1 giây).

  Returns:
    None
  """

  # Tạo tín hiệu thời gian
  time = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
  signal = amplitude * np.cos(2 * np.pi * frequency * time)**3
  
 # Xác định phương trình
  print(f"Phương trình: {amplitude} * cos^3({10*frequency}*t)")

  # Tính giá trị trung bình
  mean_value = np.mean(signal)
  print("Giá trị trung bình:", mean_value)

  # Tính năng lượng
  energy = np.sum(signal**2) / sampling_rate
  print("Năng lượng:", energy)

  # Tính công suất
  power = energy / duration
  print("Công suất:", power)

  # Tính FFT để tìm phổ biên độ
  fft_result = np.fft.fft(signal)
  freqs = np.fft.fftfreq(len(signal), 1/sampling_rate)
  
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
analyze_signal(amplitude) 