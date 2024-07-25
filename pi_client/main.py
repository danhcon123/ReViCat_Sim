import subprocess
import time

# Define the full paths to the scripts
script1 = "/home/admin/Desktop/Metadatas_MQTT_Broker_ModbusTCP.py"
script2 = "/home/admin/Desktop/Videodatas_UDP_Receiver.py"

# Start script1 with sudo
process1 = subprocess.Popen(["sudo", "python3", script1])

# Start script2 without sudo
process2 = subprocess.Popen(["python3", script2])

# Keep the main script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Handle cleanup if necessary
    print("Terminating scripts...")
    process1.terminate()
    process2.terminate()
    print("Scripts terminated")
