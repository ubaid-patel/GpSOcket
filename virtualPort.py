# send_gps_sim.py
import serial
import time
import random

def runVirtualPort(freq):
    # Open the serial port
    port = serial.Serial('COM1', 9600)
    print("Serial port opened:", port.port)

    # Set a base location (e.g., Bangalore)
    base_lat = 12.9716
    base_lon = 77.5946

    while True:
        # Add small random changes to simulate movement
        lat = base_lat + random.uniform(-0.005, 0.005)
        lon = base_lon + random.uniform(-0.005, 0.005)

        # Format the data string
        data = f"[{lat:.6f},{lon:.6f}]\n"

        # Send over serial
        port.write(data.encode())
        print("Sent:", data.strip())

        time.sleep(freq)
