# IS496: Computer Networks (Spring 2022)
# Programming Assignment 1 -  Starter Code
# Name and NetId of each member:
# Member 1: River Liu, ll24
# Member 2:
# Member 3:


# Note:
# This starter code is optional. Feel free to develop your own solution to Part 1.
# The finished code for Part 1 can also be used for Part 2 of this assignment.


# Import any necessary libraries below
import socket
import sys, struct, time
from pg1lib import *


############## Beginning of Part 1 ##############
# TODO: define a buffer size for the message to be read from the UDP socket
BUFFER = 2048


def part1 ():
    print("********** PART 1 **********")
    # TODO: fill in the hostname and port number
    hostname = ''
    PORT = 41022

    # A dummy message (in bytes) to test the code
    message = b"Hello World"

    # TODO: convert the host name to the corresponding IP address
    HOST = '192.17.61.22'
    sin = (HOST, PORT)

    # TODO: create a datagram socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as msg:
        print('Failed to create socket.')
        sys.exit()

    # TODO: convert the message from string to byte and send it to the server
    sock.sendto(message, sin)

    # TODO:
    # 1. receive the acknowledgement from the server
    # 2. convert it from network byte order to host byte order
    data = sock.recvfrom(BUFFER)
    acknowledgement = socket.ntohs(int.from_bytes(data[0], 'big'))

    # TODO: print the acknowledgement to the screen
    print('Acknowledgement: {}'.format(acknowledgement))

    # TODO: close the socket
    sock.close()




############## End of Part 1 ##############




############## Beginning of Part 2 ##############
# Note: any functions/variables for Part 2 will go here

def part2 (argv):
    print("********** PART 2 **********")
    # TODO: fill in the hostname and port number
    hostname = argv[1]
    PORT = int(argv[2])

    # A dummy message (in bytes) to test the code
    message_raw = bytes(argv[3], encoding="utf8")

    # TODO: convert the host name to the corresponding IP address
    if argv[1] == 'student00.ischool.illinois.edu':
        HOST = '192.17.61.22'
    elif argv[1] == 'student01.ischool.illinois.edu':
        HOST = '192.17.61.23'
    elif argv[1] == 'student02.ischool.illinois.edu':
        HOST = '192.17.61.26'
    elif argv[1] == 'student03.ischool.illinois.edu':
        HOST = '192.17.61.29'

    sin = (HOST, PORT)

    pubkey = getPubKey()

    # TODO: create a datagram socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as msg:
        print('Failed to create socket.')
        sys.exit()

    # Client send its public key to Server and get public key of Server
    sock.sendto(pubkey, sin)
    start = time.time() * 1000000
    pubkey_server_data = sock.recvfrom(BUFFER)
    pubkey_server_e = pubkey_server_data[0]
    pubkey_server = decrypt(pubkey_server_e)

    # Encrypt the message and generate the checksum
    message = encrypt(message_raw, pubkey_server)
    checksum_int = checksum(message_raw)
    checksum_b = bytes(str(checksum_int), encoding='utf8')


    # TODO: convert the message from string to byte and send it to the server
    sock.sendto(message, sin)
    sock.sendto(checksum_b, sin)
    print('Checksum Sent: ', checksum_int)

    # TODO:
    # 1. receive the acknowledgement from the server
    # 2. convert it from network byte order to host byte order
    data = sock.recvfrom(BUFFER)
    acknowledgement = socket.ntohs(int.from_bytes(data[0], 'big'))
    if acknowledgement == 1:
        print('Server has successfully received the message!')
    else:
        print('Server has not successfully received the message!')

    end = time.time() * 1000000
    print('RTT: ', end - start, 'us')
    # TODO: close the socket
    sock.close()



############## End of Part 2 ##############





if __name__ == '__main__':
    # Your program will go with function part1() if there is no command line input.
    # Otherwise, it will go with function part2() to handle the command line input
    # as specified in the assignment instruction.
    if len(sys.argv) == 1:
        part1()
    else:
        part2(sys.argv)
