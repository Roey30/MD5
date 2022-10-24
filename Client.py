# IMPORTS:
import multiprocessing
from threading import *
import hashlib
import math
import socket

# CONSTANTS:
LIST_THREADS = []
CORES = multiprocessing.cpu_count()
TEST_WORD = 'ec9c0f7edcc18a98b1f31853b1813301'
TEST_NUMBER = 3735928559
final_msg = ''
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


def solve_function(msg, range_number_first, range_number_last, number_thread):
    global final_msg, found, final_number, thread_found
    print('Begging the solving part')
    print(f'Number of thread is: {number_thread}')
    while range_number_first < range_number_last and not found:
        final_msg = hashlib.md5(str(range_number_first).encode())
        final_hash = final_msg.hexdigest()
        print(f'The number is: {range_number_first}')
        if final_hash == msg:
            print('discovered')
            found = True
            final_number = range_number_first
            thread_found = number_thread
        range_number_first += 1
        print(f'The hash is: {final_hash}')
    if found:
        print(f'thread number: {thread_found} fount it. it was number - {final_number} for the string - {msg}')
    else:
        print(f'thread number {number_thread} did not found it')
    return found


def main():
    global first_range_of_numbers, final_range_of_numbers, different
    number_of_cores = CORES
    number_thread = 1
    print(f'The number of Cores you have is: {number_of_cores}')
    try:
        CLIENT.connect((SERVER, PORT))
        msg = CLIENT.recv(MAX_PACKET).decode()
        print(f'The word that the server sent is: {msg}')
        data = CLIENT.recv(MAX_PACKET).decode()
        range_number = data.split('-')
        first_range_of_numbers = int(range_number[0])
        final_range_of_numbers = int(range_number[1])
        different = final_range_of_numbers - first_range_of_numbers
        print(f'The first range is: {first_range_of_numbers} and The final range is: {final_range_of_numbers}'
              f' and the different is: {different}')
        while number_of_cores != 0:
            range_number = range_calculater(number_thread)
            thread = Thread(target=solve_function, args=(msg, range_number[0], range_number[1], number_thread))
            number_thread += 1
            LIST_THREADS.append(thread)
            print(f'List of threads: {LIST_THREADS}')
            print(f'The number of Cores is: {number_of_cores}')
            print(f'The number of threads is: {number_thread}')
            number_of_cores = number_of_cores - 1
        for i in LIST_THREADS:
            i.run()
        print(f'found = {found}')
        if found:
            CLIENT.send('1'.encode())
        else:
            CLIENT.send('2'.encode())
    except socket.error and KeyboardInterrupt and ConnectionRefusedError and ConnectionResetError as err:
        print('Received socket exception - ' + str(err))
    finally:
        print('The client is closing now ')


if __name__ == '__main__':
    main()
