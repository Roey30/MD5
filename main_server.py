# IMPORTS
import socket
from threading import *
import math

# CONSTANTS
MaxPacket = 1024
QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 3256
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
LIST_THREADS = []

EXAMPLE = 'EC9C0F7EDCC18A98B1F31853B1813301'
EXAMPLE2 = '202cb962ac59075b964b07152d234b70'  # 123
MAX_NUMBER = 1000
MAX_CLIENTS = 50
CLIENT_NUMBER = 0

did_found = '2'

#FUNCTIONS

def handle_clients(client_socket,client_address ):


def main():
    global CLIENT_NUMBER, did_found
    found = False
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print("Listening for connections on port %d" % PORT)
        while CLIENT_NUMBER < MAX_CLIENTS and found == False:
            client_socket, client_address = server_socket.accept()
            thread = Thread(target=handle_clients, args=(client_socket, client_address))
            LIST_THREADS.append(thread)
            CLIENT_NUMBER += 1
            print(f'List of threads: {LIST_THREADS}')
            print(f'THe number of clients is - {CLIENT_NUMBER}')
            thread.start()
            if did_found == '1':
                exit()
    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()