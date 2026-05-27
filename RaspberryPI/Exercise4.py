"""
*******************************************************************************************************************
General Information
********************************************************************************************************************
Project:       Exercise
File:          Exercise4.py
Descriptions:   • Thread1generates a random sensor value (temperature).
                • Thread 2 reads the latest sensor value and prints whether the fan
                should be ON or OFF.
                • If the temperature is greater than 30°C: ON
                • Otherwise: OFF

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
import threading 
import random 
import time 
temperature = 0 
lock = threading.Lock() 
def sensor_thread(): 
    global temperature 
    while True: 
        new_temp = random.randint(0, 50) #tao nhien do random 
        with lock: 
            temperature = new_temp 
            print(f"[Sensor] Temperature = {temperature} °C") 
            time.sleep(1) 
def fan_control_thread(): 
    global temperature 
    while True: 
        with lock: 
            if temperature > 30: 
                print("[Fan] Temperature > 30°C --> Fan ON") #tren 30do bat quat 
            else: 
                print("[Fan] Temperature <= 30°C --> Fan OFF") #duoi 30 do tat quat 
                time.sleep(1) 
if __name__ == "__main__": 
    t1 = threading.Thread(target=sensor_thread) 
    t2 = threading.Thread(target=fan_control_thread) 
    t1.start() 
    t2.start() 
    t1.join() 
    t2.join() 
