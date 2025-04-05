import eventlet
from virtualPort import runVirtualPort
eventlet.monkey_patch()
import threading
import time
from flask import Flask,render_template
from flask_socketio import SocketIO
import serial




freq = int(input("Enter refresh frequency"))
t = threading.Thread(target=runVirtualPort, args=(freq,))
t.start()
time.sleep(1)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # WebSocket with CORS allowed

@app.route('/')
def index():
    
    return render_template('index.html')

# Background task to read GPS data from serial and emit via WebSocket
def send_gps_data():
    try:
        ser = serial.Serial('COM1', 9600, timeout=1)  # Use correct COM port here
        print("[INFO] Serial port opened:", ser.port)
    except serial.SerialException as e:
        print("[ERROR] Could not open serial port:", e)
        return

    while True:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    socketio.emit('gps_data', line)
                    print("[Transferred]:", line)
                else:
                    print("[WARN] Empty line received.")
            else:
                print("[WAITING] No data yet...")
        except Exception as e:
            print("[ERROR] Exception while reading serial:", e)

        eventlet.sleep(freq)  # Use eventlet's non-blocking sleep

@socketio.on('connect')
def handle_connect():
    print("[CLIENT] Connected")
    socketio.start_background_task(send_gps_data)

if __name__ == '__main__':
    print("[SERVER] Starting Flask WebSocket server on port 5000...")
    socketio.run(app, port=5001)
