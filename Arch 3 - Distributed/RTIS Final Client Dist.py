import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  # for file/URI/PIL/cv2/np inputs and NMS

max_clients = 2
cap=cv2.VideoCapture('Chicago Biking Trimmed.mp4')
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('localhost', 9000))

# id = pickle.loads(clientsocket.recv(4096))
data = clientsocket.recv(4096)
print(data)
id = int(float(data))

i = 0
while True:
    frame = cap.read()[1]
    
    if (i%max_clients)+1==id:
        # Serialize frame
        results = model(frame).render()[0]
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(results, f'Client ID - {id}', (10,25), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(results, f'Frame no. - {i}', (10,50), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        # data = pickle.dumps(frame)
        data = pickle.dumps(results)

        # Send message length first
        message_size = struct.pack("L", len(data))

        # Then data
        clientsocket.sendall(message_size + data)
        # clientsocket.sendall(bytes(str(id), 'utf-8'))
        reply = clientsocket.recv(1)
    
    i+=1