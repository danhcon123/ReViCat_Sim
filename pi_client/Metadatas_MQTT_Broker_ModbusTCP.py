import json
import paho.mqtt.client as mqtt
from pyModbusTCP.server import DataBank, ModbusServer

# MQTT configuration
MQTT_BROKER = "192.168.100.74"
MQTT_TOPICS = {
    "speed": "revicat/speed",
    "distance": "revicat/distance",
    "person": "revicat/person"
}
x_scale =1024/1280
y_scale = 768/960

# Modbus server configuration
MODBUS_SERVER_IP = "192.168.100.73"
MODBUS_SERVER_PORT = 502

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    for topic in MQTT_TOPICS.values():
        client.subscribe(topic)

def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    process_message(msg.topic, msg.payload.decode())

def process_message(topic, payload):
    if topic == MQTT_TOPICS["speed"]:
        speed = float(payload)
        speed_scaled = int(speed * 10)  # Multiply by 10
        DataBank.set_words(0, [speed_scaled])
        print(f"Updated Speed register with value: {speed_scaled}")
    elif topic == MQTT_TOPICS["distance"]:
        distance = float(payload)
        distance_scaled = int(distance * 10)  # Multiply by 10
        DataBank.set_words(1, [distance_scaled])
        print(f"Updated Distance register with value: {distance_scaled}")
    elif topic == MQTT_TOPICS["person"]:
        coords = json.loads(payload)
        for i, coord in enumerate(coords):
        # Apply scaling
            if coord == [0,0,0,0]:
                scaled_coord = [0,770,0,770]
            else:     
                scaled_coord = [
                    int(coord[0] * x_scale),
                    int(coord[1] * y_scale),
                    int(coord[2] * x_scale),
                    int(coord[3] * y_scale)
                    ]
            base_address = 2 + i * 4
            DataBank.set_words(base_address, [scaled_coord[0]])
            DataBank.set_words(base_address + 1, [scaled_coord[1]])
            DataBank.set_words(base_address + 2, [scaled_coord[2]])
            DataBank.set_words(base_address + 3, [scaled_coord[3]])
            print(f"Updated Bounding Box {i+1} registers with scaled coordinates: {scaled_coord}")

# MQTT client setup
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to MQTT broker
mqtt_client.connect(MQTT_BROKER, 1883, 60)
mqtt_client.loop_start()

# Modbus server setup
modbus_server = ModbusServer(host=MODBUS_SERVER_IP, port=MODBUS_SERVER_PORT, no_block=True)

try:
    print("Starting Modbus server...")
    modbus_server.start()
    while True:
        pass  # Keep the script running
except KeyboardInterrupt:
    print("Subscriber and Modbus server stopped")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    modbus_server.stop()
