"""

"""
# IMPORTS
import socket
import math
from threading import *


# CONSTANTS
MAXPACKETS = 1024
QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 3256
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
LIST_THREADS = []

WORD_TO_FIND = 'EC9C0F7EDCC18A98B1F31853B1813301'
EXAMPLE = '16583616b2cb7d6cd3393bb2e3694c26'  # 76859
MAX_NUMBER = 1000
MAX_CLIENTS = 50
CLIENT_NUMBER = 0

DID_FOUND = 'False'
DISCOVERD = False


# FUNCTIONS


def handle_clients(client_socket, client_address):
    global DID_FOUND, CLIENT_NUMBER, DISCOVERD
    while not DISCOVERD:
        first_range_of_number = math.trunc((MAX_NUMBER / 50) * (CLIENT_NUMBER - 1))
        final_range_of_number = math.trunc((MAX_NUMBER / 50) * CLIENT_NUMBER)
        CLIENT_NUMBER += 1
        range_number = str(first_range_of_number) + '-' + str(final_range_of_number)
        message = EXAMPLE, str(range_number)
        client_socket.send(message[0].encode() + ','.encode() + message[1].encode())
        if not DISCOVERD:
            DID_FOUND = client_socket.recv(MAXPACKETS).decode()
        if DID_FOUND == 'False':
            pass
        elif DID_FOUND == 'True':
            print(f'The client {client_address} found it ')
            DISCOVERD = True


def main():
    """

    :return:
    """
    global CLIENT_NUMBER, DID_FOUND
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print('Starting process')
        while CLIENT_NUMBER < MAX_CLIENTS and DISCOVERD == False:
            client_socket, client_address = server_socket.accept()
            print(f'Hello client {client_address}')
            thread = Thread(target=handle_clients, args=(client_socket, client_address), daemon=True)
            LIST_THREADS.append(thread)
            CLIENT_NUMBER += 1
            thread.start()
        for t in LIST_THREADS:
            t.join()
        if DISCOVERD:
            exit(f'The client found it ')
        else:
            print('The client did not found it')
    except socket.error and ConnectionAbortedError as err:
        print('Some problem came up - ' + str(err))
    finally:
        server_socket.close()
        if DISCOVERD:
            print('Done')


if __name__ == '__main__':
    main()
