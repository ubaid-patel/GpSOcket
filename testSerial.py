# receive_gps_sim.py
import serial

port = serial.Serial('COM1', 9600)

while True:
    line = port.readline().decode().strip()
    print("Received:", line)
    # You can now parse and process it as needed
