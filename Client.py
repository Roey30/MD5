# IMPORTS:
import multiprocessing
from threading import *
import hashlib
import math
import socket

# CONSTANTS:
list_thread = []
CORES = multiprocessing.cpu_count()
TEST_WORD = 'ec9c0f7edcc18a98b1f31853b1813301'
TEST_NUMBER = 3735928559
final_msg = ''
final_hash = ''
found = False
"""first_range_of_numbers = 3735928561
final_range_of_numbers = 3735928569"""
first_range_of_numbers = 0
final_range_of_numbers = 0
different = 0
final_number = 0
thread_found = 0

MAX_PACKET = 2048
SERVER = "127.0.0.1"
CLIENT_SOCKET = socket.socket()
PORT = 3256
CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# FUNCTIONS:


def range_calculater(number_threads):
    global first_range_of_numbers, final_range_of_numbers, different
    first_range = math.trunc(first_range_of_numbers + ((different / CORES) * (number_threads - 1)))
    final_range = math.trunc(first_range_of_numbers + (different / CORES) * number_threads)
    print(f'The first range is: {first_range}, The last range is: {final_range}')
    return first_range, final_range


def solve_function(msg, first_range, final_range, number_thread):
    global final_msg, found, final_hash
    print('Begging the solving part')
    print(f'Number of thread is: {number_thread}')
    while first_range < final_range and not found:
        final_msg = hashlib.md5(str(first_range).encode())
        final_hash = final_msg.hexdigest()
        print(f'The number is: {first_range}')
        if final_hash == msg:
            print('discovered')
            found = True
        first_range += 1
    if found:
        print(f'Found it. it was number - {first_range - 1} for the string - {msg}')
    else:
        print(f'thread number {number_thread} did not found it')
    return found


def main():
    global found, different, list_thread, first_range_of_numbers, final_range_of_numbers
    try:
        CLIENT.connect((SERVER, PORT))
        while True:
            number_of_cores = CORES
            number_thread = 1
            print(f'The number of Cores you have is: {number_of_cores}')
            msg_range = CLIENT.recv(MAX_PACKET).decode()  # msg_range[0] = msg, msg_range[1] = range
            print(f'The server send {msg_range}')
            msg_range = msg_range.split(',')
            print(f'The word that the server sent is: {msg_range[0]}')
            range_number = msg_range[1].split('-')
            first_range_of_numbers = int(range_number[0])
            final_range_of_numbers = int(range_number[1])
            different = (first_range_of_numbers - final_range_of_numbers) * -1
            print(f'The first range is: {first_range_of_numbers} and The final range is: {final_range_of_numbers}'
                  f' and the different is: {different}')
            while number_of_cores + 1 != number_thread:
                range_number = range_calculater(number_thread)
                thread = Thread(target=solve_function, args=(msg_range[0], range_number[0], range_number[1],
                                                             number_thread))
                thread.start()
                number_thread += 1
                list_thread.append(thread)
                print(f'List of threads: {list_thread}')
                print(f'The number of Cores is: {number_of_cores}')
                print(f'The number of threads is: {number_thread}')

            for t in list_thread:
                t.join()
            list_thread = []
            if found:
                print('sending True')
                CLIENT.send('True'.encode())
                break
            else:
                print('sending False')
                CLIENT.send('False'.encode())
    except socket.error and KeyboardInterrupt and ConnectionRefusedError and ConnectionResetError as err:
        print('Received socket exception - ' + str(err))
    finally:
        print('The client is closing now ')


if __name__ == '__main__':
    main()
