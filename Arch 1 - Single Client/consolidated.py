import multiprocessing
import time
from RTIS_Final_Client import Client
from RTIS_Final_Server import Server

if __name__ == '__main__':
    host, port = 'localhost', 9000
    file = 'Chicago.mp4'
    
    s = multiprocessing.Process(target=Server, args=(host, port))
    s.start()
    time.sleep(5)
    
    c = multiprocessing.Process(target=Client, args=(host, port, file))
    c.start()
    
    s.join()
    c.join()