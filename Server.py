import socket
from threading import *
import math

MaxPacket = 1024
QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 3256
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
LIST_THREADS = []

EXAMPLE = 'EC9C0F7EDCC18A98B1F31853B1813301'
EXAMPLE2 = '0e160c30ad1efc25ac48540f50798e17'  # 564721
MAX_NUMBER = 1000
MAX_CLIENTS = 50
CLIENT_NUMBER = 0

did_found = 'False'
discovered = False


def main():
    global CLIENT_NUMBER, did_found
    found = False
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        while CLIENT_NUMBER < MAX_CLIENTS and discovered == False:
            client_socket, client_address = server_socket.accept()
            thread = Thread(target=handle_clients, args=(client_socket, client_address))
            LIST_THREADS.append(thread)
            CLIENT_NUMBER += 1
            thread.start()
        for t in LIST_THREADS:
            t.join()
        if discovered:
            exit(f'The client found it ')
    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()
        print('Done')


def handle_clients(client_socket, client_address):
    global did_found, CLIENT_NUMBER, discovered
    while not discovered:
        first_range_of_number = math.trunc((MAX_NUMBER / 50) * (CLIENT_NUMBER - 1))
        final_range_of_number = math.trunc((MAX_NUMBER / 50) * CLIENT_NUMBER)
        CLIENT_NUMBER += 1
        range_number = str(first_range_of_number) + '-' + str(final_range_of_number)
        message = EXAMPLE2, str(range_number)
        client_socket.send(message[0].encode() + ','.encode() + message[1].encode())
        if not discovered:
            did_found = client_socket.recv(MaxPacket).decode()
        if did_found == 'False':
            pass
        elif did_found == 'True':
            print(f'The client {client_address} found it ')
            discovered = True
    if discovered:
        client_socket.close()
        return


if __name__ == '__main__':
    main()
