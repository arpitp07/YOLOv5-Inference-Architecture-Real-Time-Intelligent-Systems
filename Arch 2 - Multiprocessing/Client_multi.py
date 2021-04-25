import multiprocessing
from RTIS_Final_Client_Dist import Client
from RTIS_Final_Server_Dist import Server

if __name__ == '__main__':
    m = 2
    host, port = 'localhost', 5000
    file = 'Dogs.mp4'
    
    q = multiprocessing.Process(target=Server, args=(m, host, port))
    q.start()

    processes = []
    for i in range(m):
        p = multiprocessing.Process(target=Client, args=(m, host, port, file))
        processes.append(p)
        p.start()
    
    for pro in processes:
        pro.join()
    
    q.join()