from gpiozero import LED, Button, Device
from gpiozero.pins.mock import MockFactory
import tkinter as tk

# Kích hoạt chế độ giả lập
Device.pin_factory = MockFactory()

# Tạo các thiết bị ảo
led = LED(17)
button = Button(2)

# Tạo cửa sổ giao diện
root = tk.Tk()
root.title("Giả lập GPIO Zero - LED & Button")
root.geometry("300x250")
root.resizable(False, False)

# Nhãn trạng thái LED
led_label = tk.Label(root, text="LED đang TẮT", font=("Arial", 14), fg="gray")
led_label.pack(pady=20)

# Hàm cập nhật giao diện LED
def update_led_state():
    if led.is_lit:
        led_label.config(text="LED đang BẬT", fg="green")
    else:
        led_label.config(text="LED đang TẮT", fg="gray")

# Hành vi khi nhấn/thả nút ảo
def on_press():
    button.pin.drive_high()
    update_led_state()

def on_release():
    button.pin.drive_low()
    update_led_state()

# Gán hành vi của button ảo cho LED thật (trong giả lập)
button.when_pressed = led.on
button.when_released = led.off

# Nút điều khiển ảo
button_widget = tk.Button(root, text="Nhấn nút", font=("Arial", 14), width=15, height=2)
button_widget.pack(pady=30)

# Gắn sự kiện nhấn và thả chuột
button_widget.bind("<ButtonPress>", lambda e: on_press())
button_widget.bind("<ButtonRelease>", lambda e: on_release())

# Nhãn hướng dẫn
tk.Label(root, text="Nhấn nút để bật/tắt LED ảo", font=("Arial", 11)).pack(pady=10)

root.mainloop()
