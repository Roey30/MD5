"""
Name : Roey Firan
Program name : Project MD5
Date : 14/11/2022
Description: Uses to find a reverse hash function,
gets a sting and returns the number that if you do the hash function on you
get the string
"""
# IMPORTS
import socket
import math
import logging
from threading import *

# CONSTANTS
MAX_PACKETS = 1024
QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 32564
SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
LIST_THREADS = []

WORD_TO_FIND = 'EC9C0F7EDCC18A98B1F31853B1813301'
MAX_NUMBER = 1000
MAX_CLIENTS = 50
CLIENT_NUMBER = 0
RANGE_NUMBER = 0

MSG = ''
DID_FOUND = 'False'
DISCOVERED = False


# FUNCTIONS


def range_giver():
    """
    calculates the range
    :return: first range and last range
    """
    first_range_of_number = math.trunc((MAX_NUMBER / MAX_CLIENTS) * (RANGE_NUMBER - 1))
    final_range_of_number = math.trunc((MAX_NUMBER / MAX_CLIENTS) * RANGE_NUMBER)
    return first_range_of_number, final_range_of_number


def handle_clients(client_socket, client_address):
    global DID_FOUND, DISCOVERED, MSG, RANGE_NUMBER
    try:
        while not DISCOVERED:
            first_range_of_number = range_giver()[0]
            final_range_of_number = range_giver()[1]
            range_number = str(first_range_of_number) + '-' + str(final_range_of_number)
            RANGE_NUMBER += 1
            message = WORD_TO_FIND, str(range_number)
            client_socket.send(message[0].encode() + ','.encode() + message[1].encode())
            if not DISCOVERED:
                MSG = client_socket.recv(MAX_PACKETS).decode()
                MSG = MSG.split(',')
                DID_FOUND = MSG[0]
            if DID_FOUND == 'False':
                pass
            elif DID_FOUND == 'True':
                print(f'The client {client_address} found it, it was the hash of number {MSG[1]} ')
                logging.debug(f'The client {client_address} found it, it was the hash of number {MSG[1]} ')
                DISCOVERED = True
                return
    except Exception as err:
        print('Some problem came up - ' + str(err))
        logging.error('Some problem came up - ' + str(err))


def main():
    """
    The main function:
    connect to the client and open the threads for each client
    for each client sends the range and prints the answer
    """
    global CLIENT_NUMBER, DID_FOUND, RANGE_NUMBER
    try:
        SERVER_SOCKET.bind((IP, PORT))
        SERVER_SOCKET.listen(QUEUE_SIZE)
        print('Starting process')
        logging.info('Starting process')
        while CLIENT_NUMBER < MAX_CLIENTS and not DISCOVERED:
            client_socket, client_address = SERVER_SOCKET.accept()
            print(f'Hello client {client_address}')
            logging.info(f'Hello client {client_address}')
            thread = Thread(target=handle_clients, args=(client_socket, client_address))
            LIST_THREADS.append(thread)
            CLIENT_NUMBER += 1
            RANGE_NUMBER = CLIENT_NUMBER
            thread.start()
        for t in LIST_THREADS:
            t.join()
        if DISCOVERED:
            exit()
        else:
            print('The client did not found it')
            logging.info('The client did not found it')
    except Exception as err:
        print('Some problem came up - ' + str(err))
        logging.error('Some problem came up - ' + str(err))
    finally:
        SERVER_SOCKET.close()
        if DISCOVERED:
            print('Done')
            logging.info('Done')


if __name__ == '__main__':
    logging.basicConfig(filename='Server_MD5.log', encoding='utf-8', level=logging.DEBUG)
    main()
