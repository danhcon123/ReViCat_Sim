import cv2

# UDP settings
UDP_IP_RECEIVE = "0.0.0.0"  # Listen on all available interfaces
UDP_PORT_RECEIVE = 5004
UDP_IP_SEND = "192.168.100.33"  # Replace with the IP address of the receiver
UDP_PORT_SEND = 5005

# GStreamer pipeline for receiving H.264 over UDP
receive_pipeline = f'udpsrc port={UDP_PORT_RECEIVE} ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! decodebin ! videoconvert ! appsink'

# GStreamer pipeline for sending H.264 over UDP
send_pipeline = f'appsrc ! videoconvert ! video/x-raw,format=I420 ! x264enc tune=zerolatency ! h264parse ! rtph264pay config-interval=1 pt=96 ! udpsink host={UDP_IP_SEND} port={UDP_PORT_SEND}'

# Initialize OpenCV VideoCapture object for receiving with the GStreamer pipeline
cap = cv2.VideoCapture(receive_pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Error: VideoCapture for receiving not opened. Check if GStreamer is installed and the pipeline is correct.")
    exit(1)

# Initialize OpenCV VideoWriter object for sending with the GStreamer pipeline
out = cv2.VideoWriter(send_pipeline, cv2.CAP_GSTREAMER, 0, 30.0, (640, 480), True)

if not out.isOpened():
    print("Error: VideoWriter for sending not opened. Check if GStreamer is installed and the pipeline is correct.")
    exit(1)

print("Waiting for video frames... Press 'q' to quit.")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        continue

    # Display the received frame (optional)
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow('Received Video', frame)

    # Send frame to the specified pipeline for sending
    out.write(frame)

    # Check for 'q' press to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
out.release()
cv2.destroyAllWindows()
