def Client(host, port, file):
    import cv2
    import numpy as np
    import socket
    import sys
    import pickle
    import struct

    cap=cv2.VideoCapture(file)
    clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientsocket.connect((host, port))

    while True:
        frame = cap.read()[1]
        # Serialize frame
        data = pickle.dumps(frame)

        # Send message length first
        message_size = struct.pack("L", len(data))

        # Then data
        clientsocket.sendall(message_size + data)

if __name__ == '__main__':
    Client('localhost', 9000, 'Chicago Biking Trimmed.mp4')