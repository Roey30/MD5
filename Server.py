"""

"""
# IMPORTS
import socket
import math
from threading import *

# CONSTANTS
MAX_PACKETS = 1024
QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 32564
SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
LIST_THREADS = []

WORD_TO_FIND = 'EC9C0F7EDCC18A98B1F31853B1813301'
EXAMPLE = '16583616b2cb7d6cd3393bb2e3694c26'  # 76859
MAX_NUMBER = 1000
MAX_CLIENTS = 50
CLIENT_NUMBER = 0

MSG = ''
DID_FOUND = 'False'
DISCOVERED = False


# FUNCTIONS


def range_giver():
    first_range_of_number = math.trunc((MAX_NUMBER / MAX_CLIENTS) * (CLIENT_NUMBER - 1))
    final_range_of_number = math.trunc((MAX_NUMBER / MAX_CLIENTS) * CLIENT_NUMBER)
    return first_range_of_number, final_range_of_number


def handle_clients(client_socket, client_address):
    global DID_FOUND, CLIENT_NUMBER, DISCOVERED, MSG
    while not DISCOVERED:
        first_range_of_number = range_giver()[0]
        final_range_of_number = range_giver()[1]
        CLIENT_NUMBER += 1
        range_number = str(first_range_of_number) + '-' + str(final_range_of_number)
        message = EXAMPLE, str(range_number)
        client_socket.send(message[0].encode() + ','.encode() + message[1].encode())
        if not DISCOVERED:
            MSG = client_socket.recv(MAX_PACKETS).decode()
            MSG = MSG.split(',')
            DID_FOUND = MSG[0]
        if DID_FOUND == 'False':
            pass
        elif DID_FOUND == 'True':
            print(f'The client {client_address} found it, it was the hash of number {MSG[1]} ')
            DISCOVERED = True
            return


def main():
    """

    :return:
    """
    global CLIENT_NUMBER, DID_FOUND
    try:
        SERVER_SOCKET.bind((IP, PORT))
        SERVER_SOCKET.listen(QUEUE_SIZE)
        print('Starting process')
        while CLIENT_NUMBER < MAX_CLIENTS and not DISCOVERED:
            client_socket, client_address = SERVER_SOCKET.accept()
            print(f'Hello client {client_address}')
            thread = Thread(target=handle_clients, args=(client_socket, client_address))
            LIST_THREADS.append(thread)
            CLIENT_NUMBER += 1
            thread.start()
        for t in LIST_THREADS:
            t.join()
        if DISCOVERED:
            exit()
        else:
            print('The client did not found it')
    except socket.error and ConnectionAbortedError as err:
        print('Some problem came up - ' + str(err))
    finally:
        SERVER_SOCKET.close()
        if DISCOVERED:
            print('Done')


if __name__ == '__main__':
    main()
