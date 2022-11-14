"""
Name : Roey Firan
Program name : Project MD5
Date : 14/11/2022
Description: Uses to find a reverse hash function,
gets a sting and returns the number that if you do the hash function on you
get the string
"""
# IMPORTS:
import multiprocessing
import hashlib
import math
import socket
from threading import *


# CONSTANTS:
LIST_THREADS = []
CORES = multiprocessing.cpu_count()
FINAL_MSG = ''
FINAL_HASH = ''
FOUND = False
FIRST_RANGE_OF_NUMBERS = 0
FINAL_RANGE_OF_NUMBERS = 0
DIFFERENT = 0
DISCOVERED = False
FINAL_ANSWER_NUMBER = 0

MAX_PACKET = 2048
SERVER = "127.0.0.1"
CLIENT_SOCKET = socket.socket()
PORT = 32564
CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# FUNCTIONS:


def range_calculater(number_threads):
    """
    calculates the range for each thread(core)
    """
    global FIRST_RANGE_OF_NUMBERS, FINAL_RANGE_OF_NUMBERS, DIFFERENT
    first_range = math.trunc(FIRST_RANGE_OF_NUMBERS + ((DIFFERENT / CORES) * (number_threads - 1)))
    final_range = math.trunc(FIRST_RANGE_OF_NUMBERS + (DIFFERENT / CORES) * number_threads)
    if first_range % 1000 == 0:
        print(f'The first range is: {first_range}, The last range is: {final_range}')
    return first_range, final_range


def solve_function(msg, first_range, final_range):
    """
    gets the range from the main and finds the
    hash number
    """
    global FINAL_MSG, FOUND, FINAL_HASH, DISCOVERED, FINAL_ANSWER_NUMBER
    if not FOUND:
        while first_range < final_range and not FOUND:
            FINAL_MSG = hashlib.md5(str(first_range).encode())
            FINAL_HASH = FINAL_MSG.hexdigest()
            if FINAL_HASH == msg:
                print('DISCOVERED')
                FOUND = True
                FINAL_ANSWER_NUMBER = first_range
            first_range += 1
        if FOUND and not DISCOVERED:
            print(f'FOUND it. it was number - {first_range - 1} for the string - {msg}')
            DISCOVERED = True
    return FOUND


def main():
    """
    The main function:
    gets the range from the client
    and sends back the hash number to the server
    """
    global FOUND, DIFFERENT, LIST_THREADS, FIRST_RANGE_OF_NUMBERS, FINAL_RANGE_OF_NUMBERS, FINAL_ANSWER_NUMBER
    number_of_cores = CORES
    try:
        print(f'The number of Cores you have is: {number_of_cores}')
        CLIENT.connect((SERVER, PORT))
        while not FOUND:
            number_of_cores = CORES
            number_thread = 1
            msg_range = CLIENT.recv(MAX_PACKET).decode()
            msg_range = msg_range.split(',')
            if range(len(msg_range) == 1):
                exit('Someone found it')
            range_number = msg_range[1].split('-')
            FIRST_RANGE_OF_NUMBERS = int(range_number[0])
            FINAL_RANGE_OF_NUMBERS = int(range_number[1])
            DIFFERENT = (FIRST_RANGE_OF_NUMBERS - FINAL_RANGE_OF_NUMBERS) * -1
            while number_of_cores != 0:
                range_number = range_calculater(number_thread)
                thread = Thread(target=solve_function, args=(msg_range[0], range_number[0], range_number[1]))
                thread.start()
                number_thread += 1
                LIST_THREADS.append(thread)
                number_of_cores = number_of_cores - 1
            for t in LIST_THREADS:
                t.join()
            LIST_THREADS = []
            if FOUND:
                CLIENT.send('True'.encode() + ','.encode() + str(FINAL_ANSWER_NUMBER).encode())
                break
            else:
                CLIENT.send('False'.encode())
        if FOUND:
            CLIENT.send('True'.encode())
    except Exception as err:
        print('There has been a problem try running again - ' + str(err))
    finally:
        if DISCOVERED:
            print('Someone found it - the client is closing now ')


if __name__ == '__main__':
    main()
