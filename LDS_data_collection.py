import serial
import pandas as pd
from datetime import datetime
import math  # Import math library for sqrt

# Setup serial connection
ser = serial.Serial('/dev/tty.usbmodem1401', 9600)  # Set the correct port and baud rate

# Constants
R0 = 15.0  # Reference resistance at 10 Lux in kOhm
Rc = 10.0  # Calibration resistance in kOhm
Vcc = 5.0  # Supply voltage
gamma = 0.5  # Non-linear response factor
u_R = 2.5  # Uncertainty in resistance (kOhm)

# List to store the collected data
data_list = []

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            try:
                if "Distance" in line:
                    parts = line.split(',')
                    distance = float(parts[0].split(':')[1].strip().split(' ')[0])
                    light_level = float(parts[1].split(':')[1].strip().split(' ')[0])

                    # Capture current time
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # Allow manual entry of micrometer-level precision data
                    micro_distance = float(input("Enter the precise micrometer value for this measurement: "))

                    # Calculate total distance with added micro distance
                    total_distance = distance + (micro_distance * 0.000001)

                    # Calculate uncertainty in illuminance
                    V_ADC = 1023 * (light_level * Rc / (Vcc * R0 + light_level * Rc))  # Inverse of voltage divider equation to find ADC value
                    V_LDR = (V_ADC * Vcc) / 1023  # Convert ADC value to voltage
                    R_LDR = (V_LDR * Rc) / (Vcc - V_LDR)  # Calculate LDR resistance
                    u_I = 10 * gamma * (R_LDR / R0)**(gamma - 1) * (u_R / R_LDR)  # Propagation of uncertainty

                    # Append data to list
                    print(f'Timestamp {current_time}, Distance: {total_distance} m, LightLevel: {light_level} Lx, Uncertainty in Illuminance: {u_I} Lux')
                    data_list.append({'Timestamp': current_time, 'Distance': total_distance,
                                      'LightLevel': light_level, 'Uncertainty': u_I})
            except IndexError:
                print("Error parsing line:", line)
except KeyboardInterrupt:
    # Stop collection
    print("Data collection stopped.")
    ser.close()

    # Convert list to DataFrame
    data = pd.DataFrame(data_list)

    # Save DataFrame to CSV
    data.to_csv('LDS_sensor_data.csv', index=False)
    print("Data saved to 'LDS_sensor_data.csv'.")
    print(data.head())  # Optionally print the first few rows of the data
