import paho.mqtt.client as mqtt
import time
import random
import json

# MQTT configuration
MQTT_BROKER = "192.168.100.74"  # Replace with the IP address of the MQTT broker
# MQTT_BROKER = "127.0.0.1"
MQTT_TOPICS = {
    "speed": "revicat/speed",
    "distance": "revicat/distance",
    "person": "revicat/person"
}

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")

# Set up MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect

# Connect to MQTT broker on port 1883
mqtt_client.connect(MQTT_BROKER, 1883, 60)

# Start MQTT client loop
mqtt_client.loop_start()

class BoundingBoxUpdater:
    def __init__(self):
        self.positions = []
        self.generate_new_positions()

    def generate_new_positions(self):
        self.num_people = random.randint(1, 5)
        self.positions = []
        for _ in range(self.num_people):
            x1 = random.randint(0, 1280)
            y1 = random.randint(0, 720)
            x2 = x1 + random.randint(50, 100)
            y2 = y1 + random.randint(50, 100)
            direction = 'left' if x1 < 640 else 'right'
            self.positions.append([x1, y1, x2, y2, direction])

    def update_positions(self):
        move_step = 20  # Move by 20 pixels
        scale_factor = 1.2  # Increase size by 20%
        new_positions = []

        for pos in self.positions:
            direction = pos[4]
            if direction == 'left':
                pos[0] -= move_step
                pos[2] -= move_step
            else:
                pos[0] += move_step
                pos[2] += move_step

            # Scale the bounding box
            width = (pos[2] - pos[0]) * scale_factor
            height = (pos[3] - pos[1]) * scale_factor
            center_x = (pos[0] + pos[2]) / 2
            center_y = (pos[1] + pos[3]) / 2
            pos[0] = center_x - width / 2
            pos[2] = center_x + width / 2
            pos[1] = center_y - height / 2
            pos[3] = center_y + height / 2

            if 0 <= pos[0] <= 1280 and 0 <= pos[2] <= 1280 and 0 <= pos[1] <= 960 and 0 <= pos[3] <= 960:
                new_positions.append(pos)

        self.positions = new_positions

        # Generate new bounding boxes if all have disappeared
        if not self.positions:
            self.generate_new_positions()

# Instantiate the BoundingBoxUpdater
bbox_updater = BoundingBoxUpdater()

try:
    while True:
        bbox_updater.update_positions()
        persons_coords = [[pos[0], pos[1], pos[2], pos[3]] for pos in bbox_updater.positions]
        
        #Ensure the number of bounding box is exactly 5
        while len(persons_coords) < 5:
            persons_coords.append([0,0,0,0])
        
        speed = random.uniform(0, 200)
        speed = round(speed, 1)
        distance = random.uniform(0, 20)
        distance = round(distance, 1)
        
        data_json = json.dumps(persons_coords)
                
        print(f"Publishing speed: {speed}")
        mqtt_client.publish(MQTT_TOPICS["speed"], speed)

        print(f"Publishing distance: {distance}")
        mqtt_client.publish(MQTT_TOPICS["distance"], distance)

        print(f"Publishing person coordinates: {persons_coords}")
        mqtt_client.publish(MQTT_TOPICS["person"], data_json)

        time.sleep(1)
except KeyboardInterrupt:
    print("Publisher stopped")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
