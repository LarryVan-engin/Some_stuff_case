"""
*******************************************************************************************************************
General Information
********************************************************************************************************************
Project:       Exercise
File:          Exercise3.py
Descriptions:   Connects to anMQTTbroker(test.mosquitto.org).
                • Publishes the random temperature value (random number from 20–35) to topic
                iot/classroom/temperature every 5 seconds.
                • Subscribes to topic iot/classroom/temperature.
                • Prints out every message it receives from the publisher.
                • Publisher (Sensor Node): Publishes "ON" if temperature > 30, otherwise "OFF"
                to topic iot/classroom/fan.
                • Subscriber (Actuator Node): Subscribes to iot/classroom/fan and controls an
                LED:
                • LEDONifmessage="ON"
                • LEDOFFifmessage="OFF".

Author:        VAN DAC PHONG TRUC (Project Leader)
Email:         truc.vanlarrytt@hcmut.edu.vn
Created:       11/11/2025
Last Update:   12/11/2025
Version:       2.0

Python:        3.13.9
Copyright:     (c) 2025 IOE INNOVATION Team
*******************************************************************************************************************
"""

#######################################################################################################################
# Imports
#######################################################################################################################
import paho.mqtt.client as mqtt
import random
import time
import threading
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# MQTT broker configuration
BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC_TEMPERATURE = "iot/classroom/temperature"
TOPIC_FAN = "iot/classroom/fan"

# For GPIO (uncomment if using actual hardware)
# import RPi.GPIO as GPIO
# LED_PIN = 18
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(LED_PIN, GPIO.OUT)


#######################################################################################################################
# MQTT Node Class
#######################################################################################################################
class MQTTNode:
    def __init__(self, gui):
        self.gui = gui
        self.client = mqtt.Client(client_id="combined_node", clean_session=True)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        # self.client.on_publish = self.on_publish
        self.running = True
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            # Subscribe to both topics
            client.subscribe(TOPIC_TEMPERATURE)
            client.subscribe(TOPIC_FAN)
            print(f"Subscribed to: {TOPIC_TEMPERATURE}, {TOPIC_FAN}\n")
        else:
            print(f"Failed to connect, return code {rc}")
    
    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        print(f"[RECEIVED] Topic: {msg.topic} | Message: {message}")
        
        # # Control LED if message is from fan topic
        # if msg.topic == TOPIC_FAN:
        #     if message == "ON":
        #         print("  >>> LED turned ON")
        #         # GPIO.output(LED_PIN, GPIO.HIGH)
        #     elif message == "OFF":
        #         print("  >>> LED turned OFF")
        #         # GPIO.output(LED_PIN, GPIO.LOW)
    
        if msg.topic == TOPIC_TEMPERATURE:
            self.gui.update_temperature(message)

        elif msg.topic == TOPIC_FAN:
            self.gui.update_fan_status(message)


    def on_publish(self, client, userdata, mid):
        pass  # Silent publishing
    
    def publish_loop(self):
        """Publisher thread - sends temperature and fan control"""
        time.sleep(2)  # Wait for connection
        print("=== Publishing started ===\n")
        
        while self.running:
            try:
                # Generate random temperature
                temperature = random.randint(20, 35)
                
                # Publish temperature
                self.client.publish(TOPIC_TEMPERATURE, str(temperature), qos=0)
                print(f"[PUBLISHED] Temperature: {temperature}°C")
                
                # Determine and publish fan status
                fan_status = "ON" if temperature > 28 else "OFF"
                self.client.publish(TOPIC_FAN, fan_status, qos=0)
                print(f"[PUBLISHED] Fan: {fan_status}\n")
                
                time.sleep(5)

            except Exception as e:
                print(f"Error in publish loop: {e}")
                break
    
    def start(self):
        print(f"Connecting to {BROKER}...")
        self.client.connect(BROKER, PORT, 60)
        self.client.loop_start()

        # Start publishing in background
        pub_thread = threading.Thread(target=self.publish_loop)
        pub_thread.daemon = True
        pub_thread.start()
    

    def stop(self):
        print(f"\nStopping MQTT node...")
        self.running = False
        self.client.loop_stop()
        self.client.disconnect()
        print("Disconnect from broker.")


#######################################################################################################################
# GUI Class
#######################################################################################################################
class IoTGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("IoT MQTT Simulation - Temperature & Fan with Live Chart")
        self.root.geometry("600x600")

        # Title
        tk.Label(root, text="MQTT IoT Node Simulation", font=("Arial", 16, "bold")).pack(pady=10)

        # --- Display Section ---
        info_frame = tk.Frame(root)
        info_frame.pack(pady=10)

        self.temp_label = tk.Label(info_frame, text="Temperature: -- °C", font=("Arial", 12))
        self.temp_label.grid(row=0, column=0, padx=10)

        self.fan_label = tk.Label(info_frame, text="Fan Status: --", font=("Arial", 12))
        self.fan_label.grid(row=0, column=1, padx=10)

        # LED indicator
        self.led_canvas = tk.Canvas(info_frame, width=50, height=50)
        self.led_canvas.grid(row=0, column=2, padx=10)
        self.led_circle = self.led_canvas.create_oval(5, 5, 45, 45, fill="gray")

        # --- Live Chart Section ---
        chart_frame = tk.Frame(root)
        chart_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        self.fig = Figure(figsize=(5.5, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Temperature Trend")
        self.ax.set_xlabel("Samples")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.grid(True)

        self.temp_data = []
        self.line, = self.ax.plot([], [], "r-o")

        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # --- Control Buttons ---
        control_frame = tk.Frame(root, width=10, height=2)
        control_frame.pack(pady=10)

        self.exit_button = ttk.Button(control_frame, text="Exit", command=self.on_exit, width=10)
        self.exit_button.pack()

        # MQTT Node
        self.mqtt_node = MQTTNode(self)
        self.mqtt_node.start()

        # Chart update loop
        self.update_chart_loop()

    # ========== UPDATE GUI ==========
    def update_temperature(self, value):
        """Update temperature display"""
        try:
            temp = float(value)
            self.temp_label.config(text=f"Temperature: {temp:.1f} °C")

            # Append to list
            self.temp_data.append(temp)
            if len(self.temp_data) > 20:
                self.temp_data.pop(0)

            # Refresh chart
            self.update_chart()
        except ValueError:
            pass

    def update_fan_status(self, status):
        """Update fan status + LED indicator"""
        if status == "ON":
            self.fan_label.config(text="Fan Status: ON", fg="green")
            self.led_canvas.itemconfig(self.led_circle, fill="green")
        else:
            self.fan_label.config(text="Fan Status: OFF", fg="gray")
            self.led_canvas.itemconfig(self.led_circle, fill="gray")

    # ========== CHART UPDATE ==========
    def update_chart(self):
        x_data = list(range(len(self.temp_data)))
        self.line.set_data(x_data, self.temp_data)
        self.ax.set_xlim(0, max(20, len(self.temp_data)))
        self.ax.set_ylim(15, 40)
        self.canvas.draw()

    def update_chart_loop(self):
        """Auto refresh chart every 1s"""
        self.update_chart()
        self.root.after(1000, self.update_chart_loop)

    # ========== EXIT ==========
    def on_exit(self):
        """Cleanly exit"""
        self.mqtt_node.stop()
        self.root.destroy()


#######################################################################################################################
# Main
#######################################################################################################################
if __name__ == "__main__":
    root = tk.Tk()
    app = IoTGUI(root)
    root.mainloop()