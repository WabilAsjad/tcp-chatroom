import threading
import socket

nickname = input("Choose a nickname: ")
#Set up client 
host = '127.0.0.1' #localhost
port = 55600

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

'''Method to receive communication from server'''
def receive():
    while True:
        try:
            message = client.recv(1024)
            if message == 'Provide nickname':
                client.send(nickname.encode('ascii'))
                pass
            else:
                print(message)
        except:
            print("An error occurred. Try connecting again later.")
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

#Start thread for client
receive_thread = threading.Thread(target = receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()