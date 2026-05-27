"""
*******************************************************************************************************************
General Information
********************************************************************************************************************
Project:       Exercise
File:          Exercise2.py
Descriptions:  • Connects abutton and anLEDto GPIOpins.
               • Whenthebuttonispressed, the LED turns ON.
               • Whenthebuttonisreleased, the LED turns OFF.

Author:        VAN DAC PHONG TRUC (Project Leader)
Email:         truc.vanlarrytt@hcmut.edu.vn
Created:       11/11/2-25
Last Update:   11/11/2025
Version:       1.0

Python:        3.13.9
Copyright:     (c) 2025 IOE INNOVATION Team
*******************************************************************************************************************
"""

#######################################################################################################################
# CODE FOR REAL RASPBERRY PI
#######################################################################################################################
# import RPi.GPIO as GPIO
# from time import sleep

# # GPIO pin configuration
# BUTTON_PIN = 17  # GPIO pin for button
# LED_PIN = 18     # GPIO pin for LED

# # Setup GPIO mode
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)

# # Configure pins
# GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Button as input with pull-down resistor
# GPIO.setup(LED_PIN, GPIO.OUT)  # LED as output

# try:
#     print("Button-LED Control Program")
#     print("Press the button to turn LED ON")
#     print("Release the button to turn LED OFF")
#     print("Press CTRL+C to exit")
    
#     while True:
#         # Read button state
#         button_state = GPIO.input(BUTTON_PIN)
        
#         if button_state == GPIO.HIGH:  # Button is pressed
#             GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED ON
#             print("Button pressed - LED ON")
#         else:  # Button is released
#             GPIO.output(LED_PIN, GPIO.LOW)  # Turn LED OFF
#             print("Button released - LED OFF")
        
#         sleep(0.1)  # Small delay to reduce CPU usage

# except KeyboardInterrupt:
#     print("\nProgram terminated by user")

# finally:
#     GPIO.cleanup()  # Clean up GPIO pins
#     print("GPIO cleanup completed")

#######################################################################################################################
# CODE FOR SIMULATE PI
#######################################################################################################################
# Imports
from gpiozero import LED, Button, Device
from gpiozero.pins.mock import MockFactory
import tkinter as tk

# Create mock simulation
Device.pin_factory = MockFactory()

# Get GPIO pin for LED and Button
led = LED(17)
button = Button(2)

# Create label for GUI
# Create window GUI
root = tk.Tk()
root.title("Simulate GPIO - LED BLINK")
root.geometry("300x250")

# Label led status
led_label = tk.Label(root, text="LED off", font=("Arial", 14), fg="gray")
led_label.pack(pady=20)

# Counter label
counter_label = tk.Label(root, text="Press count: 0", font=("Arial",12))
counter_label.pack(pady=10)

# Count button press
press_count = 0
PRESS_MAX = 5
stopped = False

def update_led_state():
    if led.is_lit:
        led_label.config(text="LED on", fg="green")
    else:
        led_label.config(text="LED off", fg="gray")
        button_widget.config(fg='gray')


button_widget = tk.Button(root,text="Press button", width=15, height=2)
button_widget.pack(pady=30)

def on_press():
    global press_count, stopped
    if stopped:
        return

    button.pin.drive_high()
    led.on()
    update_led_state()

def on_release():
    global press_count, stopped

    button.pin.drive_low()
    led.off()
    update_led_state()
    press_count +=1
    counter_label.config(text=f"Press count: {press_count}", font=("Arial", 12))

    # if press_count >= PRESS_MAX:
    #     stopped = True
    #     button_widget.config(text="disable")
    #     led.off()
    #     led_label.config(text="STOPPED", fg="gray")
    #     counter_label.config(text="Limit reached 5 times")
    #     print("Stopped program")


# Get action mouse click
button_widget.bind("<ButtonPress>", lambda e: on_press())
button_widget.bind("<ButtonRelease>", lambda e: on_release())


root.mainloop()