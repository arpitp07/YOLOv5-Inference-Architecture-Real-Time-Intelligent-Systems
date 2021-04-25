def Server(m, host, port):
    import pickle
    import socket
    import struct
    import numpy as np
    import cv2
    import torch
    import time

    HOST = host
    PORT = port
    max_clients = m

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  # for file/URI/PIL/cv2/np inputs and NMS
    s.bind((HOST, PORT))
    s.listen(10)

    print('Server online')

    clients = []

    for i in range(max_clients):
        print('Waiting to connect')
        conn, addr = s.accept()
        clients += [conn]
        print(f'Connected to {addr}')
        conn.sendall(bytes(str(i+1), 'utf-8'))

    # print(clients)
    data = b''
    payload_size = struct.calcsize("L")

    j = 0
    while True:

        # Retrieve message size
        while len(data) < payload_size:
            data += clients[j%max_clients].recv(4096)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        # Retrieve all data based on message size
        while len(data) < msg_size:
            data += clients[j%max_clients].recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Extract frame
        frame = pickle.loads(frame_data)

        # Inference
        # results = model(frame)
        
        # Display
        cv2.imshow('Original Video', frame)
        # cv2.imshow('Model Output', results.render()[0])
        cv2.waitKey(1)
        
        
        # data = clients[j].recv(4096)
        # num = int(float(data))
        # print(num)
        # time.sleep(3)
        clients[j].send(b'\x0a')
        j=(j+1)%max_clients
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    Server(2)