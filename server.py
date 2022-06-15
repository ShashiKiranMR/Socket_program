from concurrent.futures import thread
from email.headerregistry import Address, HeaderRegistry
from http import server
import socket
import threading

PORT    = 5050
SERVER  = socket.gethostbyname(socket.gethostname())
ADDR    = (SERVER, PORT)
HEADER  = 64 #Will be sent at first by the client indicating the length of the actual message
FORMAT  = 'utf-8'
DISCONNECT_MESSAGE  = "!DISCONNECT" #Client sends this to close the conn with server

server  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected   = True
    while connected:
        msg_length  = conn.recv(HEADER).decode(FORMAT) #Blocking call
        if msg_length:
            msg_length  = int(msg_length)
            msg         = conn.recv(msg_length).decode(FORMAT)

            print(f"[{addr}] {msg}")
            if msg == DISCONNECT_MESSAGE:
                connected = False

            conn.send("Msg received".encode(FORMAT))

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr  = server.accept() #Blocking call
        thread      = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()