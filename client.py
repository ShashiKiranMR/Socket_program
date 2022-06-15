from http import client
import socket

PORT    = 5050
HEADER  = 64 #Will be sent at first by the client indicating the length of the actual message
FORMAT  = 'utf-8'
DISCONNECT_MESSAGE  = "!DISCONNECT" #Client sends this to close the conn with server
SERVER  = socket.gethostbyname(socket.gethostname())
ADDR    = (SERVER, PORT)

client  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_length = str(msg_len).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

send("Hello World!")
send(DISCONNECT_MESSAGE)