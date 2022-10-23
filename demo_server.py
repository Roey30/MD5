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
EXAMPLE2 = '81448138f5f163ccdba4acc69819f280'
MAX_NUMBER = 1000
MAX_CLIENTS = 50
CLIENT_NUMBER = 0

did_found = False


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
            thread.run()
    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()


def handle_clients(client_socket, client_address):
    global did_found
    print(f'hello client - {client_address} from the socket - {client_socket}')
    print(f'Sending the word - {EXAMPLE2}')
    client_socket.send(EXAMPLE2.encode())
    print('Sending the range')
    first_range_of_number = math.trunc((MAX_NUMBER / 50) * (CLIENT_NUMBER - 1))
    final_range_of_number = math.trunc((MAX_NUMBER / 50) * CLIENT_NUMBER)
    print(f'The first range - {first_range_of_number}')
    print(f'The final range - {final_range_of_number}')
    range_number = str(first_range_of_number) + '-' + str(final_range_of_number)
    client_socket.send(range_number.encode())
    did_found = client_socket.recv(MaxPacket).decode()
    print(did_found)
    if did_found == '2':
        print('The client did not found it')
    else:
        print('The client did found it')


if __name__ == '__main__':
    main()
