def Server(host, port):
    import pickle
    import socket
    import struct
    import numpy as np
    import cv2
    import torch

    HOST = host
    PORT = port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  # for file/URI/PIL/cv2/np inputs and NMS
    s.bind((HOST, PORT))
    print('Socket bind complete')
    s.listen(10)
    print('Socket now listening')

    conn, addr = s.accept()

    data = b''
    payload_size = struct.calcsize("L")

    while True:

        # Retrieve message size
        while len(data) < payload_size:
            data += conn.recv(4096)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        # Retrieve all data based on message size
        while len(data) < msg_size:
            data += conn.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Extract frame
        frame = pickle.loads(frame_data)

        # Inference
        results = model(frame, size=1080)
        
        # Display
        cv2.imshow('Original Video', frame)
        cv2.imshow('Model Output', results.render()[0])
        cv2.waitKey(1)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    Server('localhost', 9000)