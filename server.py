import socket
import threading
import time

class server:
    hostname=''
    id=0
    port=55555
    display_interval=10
    tuple={}
    total_clients=0
    read_num=0
    get_num=0
    put_num=0
    error_num=0
    operation_num=0

    def __init__(self,hostname,id):
        self.hostname=hostname
        self.myserver=[]
        self.id=id

    def handle_clients(self,client_socket,addr):
        print(f"connected from {addr}...")
        try:
            message=client_socket.recv(1024).decode('utf-8')
            message_split=message.split()
            action=message_split(0)
            key=message_split(1)
            value=message_split(2)
            handle_request()
        except Exception as ex:
            print(f"Error handling client {addr}")
            self.error_num+=1
        finally:
            client_socket.close()
            print(f"connection with {addr} closed")

        def handle_request(self,message):
            global tuple
            part=message.split(' ')
            size=part[0]
            operation=part[1]
            key=part[2]
            dict_tuple=dict(self.tuple)

            match operation:
                case 'R':
                    if(dict_tuple[f'{key}']!=None):
                        response=f"{size} OK ({key}{dict_tuple[f'{key}']} read)"
                        client_socket.sendall(response.encode('utf-8'))
                    else:
                        self.error_num+=1
                        response=f"{size} ERR {key} does not exist"
                case 'G':



        
    
    def start_server(self):
        server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        server_socket.bind((self.hostname,self.port))
        server_socket.listen(5)
        print('server is running')
        try:
            while True:
                client_socket,addr=server_socket.accept()
                

