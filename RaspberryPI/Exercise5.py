"""
*******************************************************************************************************************
General Information
********************************************************************************************************************
Project:       Exercise
File:          Exercise5.py
Descriptions:   • Write a Python program using multiprocessing to calculate factorial of several large numbers in parallel.
                • Exampleinput: [100000, 120000, 150000]
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
import multiprocessing
import sys
sys.set_int_max_str_digits(6000000)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

def compute_factorials(numbers):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(factorial, numbers)
    return results

if __name__ == "__main__":
    numbers = [100000, 120000, 150000]
    

    results = compute_factorials(numbers)
    
    
    for n, result in zip(numbers, results):
        print(f"The factorial of {n} is {result}")
