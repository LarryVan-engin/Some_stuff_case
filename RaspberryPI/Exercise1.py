"""
*******************************************************************************************************************
General Information
********************************************************************************************************************
Project:       Exercise
File:          Exercise1.py
Descriptions:  Light on for 2s, then off for 2s. Stop after 5 times loop.

Author:        VAN DAC PHONG TRUC (Project Leader)
Email:         truc.vanlarrytt@hcmut.edu.vn
Created:       11/11/2025
Last Update:   11/11/2025
Version:       1.0

Python:        3.13.9
Copyright:     (c) 2025 IOE INNOVATION Team
*******************************************************************************************************************
"""

#######################################################################################################################
# Imports
#######################################################################################################################
# Mock library imports
from gpiozero import LED, Device, Button
from gpiozero.pins.mock import MockFactory
import tkinter as tk


Device.pin_factory = MockFactory()

#Create simulate device
led = LED(17)
button = Button(2)


# Create window GUI
root = tk.Tk()
root.title("Simulate GPIO - LED BLINK")
root.geometry("300x250")

# Label led status
led_label = tk.Label(root, text="LED off", font=("Arial", 14), fg="gray")
led_label.pack(pady=20)



# Counter label for loop
count_label = tk.Label(root, text="Count loop: 0 / 5", font=("Arial",12))
count_label.pack(pady=10)

# Label manual
tk.Label(root, text="Automatically LED blink in", font=("Arial", 11)).pack(pady=10)

# Loop count
count_loop = 0
LOOP_MAX = 5
led_state = False

# Update led status
def update_led_state():
    if led.is_lit:
        led_label.config(text="LED on", fg="green")
    else:
        led_label.config(text="LED off", fg="gray")



def toggle_led():
    global count_loop, led_state

    if count_loop >= LOOP_MAX:
        led.off()
        led_label.config(text="FINISHED", fg="red")
        count_label.config(text=f"Complete {LOOP_MAX} cycles")
        print("Stopped after 5 times loop")
        return
    
    if led_state:
        led.off()
        update_led_state()
        led_state= False
        count_loop +=1
        count_label.config(text=f"Cycle: {count_loop}/{LOOP_MAX}")
    else:
        led.on()
        update_led_state()
        led_state = True

    root.after(2000, toggle_led)

toggle_led()

root.mainloop()




