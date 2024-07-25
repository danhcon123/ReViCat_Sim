from picamera2 import Picamera2
import cv2
import socket
import numpy as np

# Set up UDP socket
UDP_IP = "192.168.100.73"  # Replace with the IP address of your computer
UDP_PORT = 5004
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Create Picamera2 instance
picam2 = Picamera2()

# Configure the camera
config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
picam2.configure(config)

# Start the camera
picam2.start()

print("Starting video stream... Press 'q' to quit.")

# Initialize VideoWriter for H.264 encoding
fourcc = cv2.VideoWriter_fourcc(*'H264')
pipeline = 'appsrc ! videoconvert ! video/x-raw,format=I420 ! x264enc tune=zerolatency ! h264parse ! rtph264pay config-interval=1 pt=96 ! udpsink host={} port={}'.format(UDP_IP, UDP_PORT)
out = cv2.VideoWriter(pipeline, cv2.CAP_GSTREAMER, 0, 30.0, (640, 480), True)

# Check if the VideoWriter is opened successfully
if not out.isOpened():
    print("Error: VideoWriter not opened. Check if GStreamer is installed and the pipeline is correct.")
    exit(1)

while True:
    # Capture image
    frame = picam2.capture_array()

    # No need to convert if the camera outputs RGB directly
    # If the camera outputs another format, you would convert it here
    # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_YUV2RGB) # Example for YUV to RGB

    # Encode frame as H.264 and send over UDP
    out.write(frame)

    # Print the sending data in hexadecimal
    #print("Sending frame:", frame.tobytes().hex()[:100], "...")  # Print first 100 hex characters for brevity

    # Display the frame (optional)
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
picam2.stop()
cv2.destroyAllWindows()
out.release()
sock.close()
