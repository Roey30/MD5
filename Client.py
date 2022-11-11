# IMPORTS:
import multiprocessing
from threading import *
import hashlib
import math
import socket
import time

# CONSTANTS:
LIST_THREADS = []
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
discovered = False

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
    if first_range % 1000 == 0:
        print(f'The first range is: {first_range}, The last range is: {final_range}')
    return first_range, final_range


def solve_function(msg, first_range, final_range, number_thread):
    global final_msg, found, final_hash, discovered
    if not found:
        while first_range < final_range and not found:
            final_msg = hashlib.md5(str(first_range).encode())
            final_hash = final_msg.hexdigest()
            if final_hash == msg:
                print('discovered')
                found = True
            first_range += 1
        if found and not discovered:
            print(f'Found it. it was number - {first_range - 1} for the string - {msg}')
            discovered = True
    return found


def main():
    global found, different, LIST_THREADS, first_range_of_numbers, final_range_of_numbers
    number_of_cores = CORES
    try:
        print(f'The number of Cores you have is: {number_of_cores}')
        CLIENT.connect((SERVER, PORT))
        while not found:
            number_of_cores = CORES
            number_thread = 1
            msg_range = CLIENT.recv(MAX_PACKET).decode()  # msg_range[0] = msg, msg_range[1] = range
            msg_range = msg_range.split(',')
            if msg_range[0] is None:
                break
            range_number = msg_range[1].split('-')
            first_range_of_numbers = int(range_number[0])
            final_range_of_numbers = int(range_number[1])
            different = (first_range_of_numbers - final_range_of_numbers) * -1
            while number_of_cores != 0:
                range_number = range_calculater(number_thread)
                thread = Thread(target=solve_function, args=(msg_range[0], range_number[0], range_number[1],
                                                             number_thread))
                thread.start()
                number_thread += 1
                LIST_THREADS.append(thread)
                number_of_cores = number_of_cores - 1
            for t in LIST_THREADS:
                t.join()
            LIST_THREADS = []
            if found:
                CLIENT.send('True'.encode())
                break
            else:
                CLIENT.send('False'.encode())
        if found:
            CLIENT.send('True'.encode())
    except socket.error and IndexError as err:
        print('Received socket exception - ' + str(err))
    finally:
        print('Someone found it the - client is closing now ')


if __name__ == '__main__':
    main()
