import socket
import threading
import time

class server:
    hostname=''
    id=0
    port=55555
    display_interval=10

    def __init__(self,hostname,id):
        self.hostname=hostname
        self.myserver=[]
        self.id=id
        
    
    def start_server(self):
        server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        server_socket.bind((self.hostname,self.port))
        server_socket.listen(5)
        print('server is running')
        try:
            while True:
                client_socket,addr=server_socket.accept()
                

