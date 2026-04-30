import socket
import sys
#from server_helper
def receive_n(sock, num_bytes):
    """Read exactly num_bytes from the socket."""
    data = b""
    while len(data) < num_bytes:
        chunk = sock.recv(num_bytes - len(data))
        if not chunk:  # Connection closed or error
            break
        data += chunk
    return data

def send_request(socket,message):
    try:
        total_size=len(message.encode('utf-8'))+4
        fomat_message=f"{total_size} {message}"

        socket.sendall(fomat_message.encode('utf-8'))

        size_bytes=receive_n(socket,3)
        if not size_bytes:
            return "Connection closed by server"
        
        response_size=int(size_bytes.encode('utf-8'))
        rest_bytes=receive_n(socket,response_size-3)

        return rest_bytes.decode('utf-8').lstrip()
    
    except Exception as ex:
        return f"ERR exception {ex}"
    

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 TupleSpaceServer.py <port>")
        sys.exit(1)

    host= int(sys.argv[1])
    port=int(sys.argv[2])
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host,port))
        print(f"Sucessfully connected to {host} {port}")
        with open("client_1.txt",'r',encoding='utf-8') as f:
            for line in f:
                lines=line.strip()
                if not lines:
                    continue

                parts=lines.split(" ",2)
                action=parts[0]
                key=parts[1]
                value=parts[2]
                size=len(f"{key} {value}")
                if size>999:
                    print("ERR size exceeds 999")
                    continue
                if action == "PUT":
                    if len(parts) != 3:
                        print(f"{original_line}: ERR PUT requires key and value")
                        continue
                    protocol_msg = f"P {key} {value}"
                elif action == "READ":
                    protocol_msg = f"R {key}"
                elif action == "GET":
                    protocol_msg = f"G {key}"
                else:
                    print(f"{line}: ERR Unknown command")
                    continue

                msg_bytes=protocol_msg.encode('utf-8')
                total_size=len(msg_bytes)+4
                full_msg=f"{total_size} {protocol_msg}".encode('utf-8')
                client_socket.sendall(full_msg)

                header=receive_n(client_socket,3)
                if not header:
                    print("ERR connection closed by the server")
                    break

                response_size=int(header.decoed('utf-8'))
                rest_msg=receive_n(client_socket,response_size-3)
                if not rest_msg:
                    print("ERR connection closed by the server")
                    break

                response=rest_msg.decode('utf-8').lstrip()
                print(f"{line}:{response}")

    except ConnectionRefusedError:
        print(f"Error: Could not connect to server at {host}:{port}. Is the server running?")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__=="__main__":
    main()