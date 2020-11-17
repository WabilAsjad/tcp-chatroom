import threading
import socket

#Set up server 
host = '127.0.0.1' #localhost
port = 55600

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(host, port)
server.listen()

clients = []
nicknames = []

'''Method to broadcast message'''
def broadcast(message):
    for client in clients:
        client.send(message)

'''Method to handle client error'''
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            #if unsuccessful, 
            # remove client from collection and remove associated nickname
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat.'.encode('ascii'))
            nicknames.remove(nickname)
            break 

'''Method to connect with new clients'''
def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        #Get nickname from client
        client.send("Provide nickname".encode('ascii'))
        client_nickname = client.recv(1024).decode('ascii')
        clients.append(client)
        nicknames.append(client_nickname)

        broadcast(f'{client_nickname} joined the chat.'.encode('ascii'))
        client.send('Connected to the server.'.encode('ascii'))

        #Start thread for this specific client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is listening...')
receive()
