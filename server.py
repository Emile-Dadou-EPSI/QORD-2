import pickle
import socket
import threading
from quantum import *
import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from numpy.random import randint
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m','--mode', dest='mode', choices=['1','2'])
args = parser.parse_args()
print(int(args.mode))

host = 'localhost'
port = 5050

# Starting server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists for clients and nicknames
clients = []
nicknames = []

sec_key = ''

# quantum process
def quantum():
    np.random.seed(seed=0)
    n = 100

    ## Step 1
    # Alice generates bits
    alice_bits = randint(2, size=n)

    ## Step 2
    # Create an array to tell us which qubits
    # are encoded in which bases
    alice_bases = randint(2, size=n)
    message = encode_message(alice_bits, alice_bases)

    ## Step 3
    # Decide which basis to measure in:
    bob_bases = randint(2, size=n)
    bob_results = measure_message(message, bob_bases, n)

    ## Step 4
    alice_key = remove_garbage(alice_bases, bob_bases, alice_bits, n)
    bob_key = remove_garbage(alice_bases, bob_bases, bob_results, n)

    ## Step 5
    sample_size = 15
    bit_selection = randint(n, size=sample_size)

    bob_sample = sample_bits(bob_key, bit_selection)
    print("  bob_sample = " + str(bob_sample))
    alice_sample = sample_bits(alice_key, bit_selection)
    print("alice_sample = "+ str(alice_sample))
    if bob_sample == alice_sample:
        return True
    else:
        return False

def quantum2():
    np.random.seed(seed=3)
    n = 100
    ## Step 1
    alice_bits = randint(2, size=n)
    ## Step 2
    alice_bases = randint(2, size=n)
    message = encode_message(alice_bits, alice_bases)
    ## Interception!!
    eve_bases = randint(2, size=n)
    intercepted_message = measure_message(message, eve_bases, n)
    ## Step 3
    bob_bases = randint(2, size=n)
    bob_results = measure_message(message, bob_bases, n)
    ## Step 4
    bob_key = remove_garbage(alice_bases, bob_bases, bob_results, n)
    alice_key = remove_garbage(alice_bases, bob_bases, alice_bits, n)
    ## Step 5
    sample_size = 15
    bit_selection = randint(n, size=sample_size)
    bob_sample = sample_bits(bob_key, bit_selection)
    print("  bob_sample = " + str(bob_sample))
    alice_sample = sample_bits(alice_key, bit_selection)
    print("alice_sample = "+ str(alice_sample))

    if bob_sample == alice_sample:
        return True
    else:
        return False

# Sending messages to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            # getting sent key
            # key = client.recv(1024).decode('utf-8')
            # print(key)
            print('handling')
            # if key.contains('key'):

            #     break
            try:
                # Broadcasting Messages
                message = client.recv(1024)
                broadcast(message)
            except:
                # Removing And Closing Clients
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast('{} left!'.format(nickname).encode('ascii'))
                nicknames.remove(nickname)
                break
        except:
            print('cannot get key')
            break
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # prep key
        if len(clients) < 2:
            key = client.recv(1024).decode('utf-8')
            client.send('waiting for another user'.encode('ascii'))
        else:
            if int(args.mode) == 1:
                print('without interception')
                test = quantum()
                if test == True:
                    for cli in clients:
                        print('starting clients')
                        # Start Handling Thread For Client mettre cette partie la dans une auter fonction
                        thread = threading.Thread(target=handle, args=(cli,))
                        thread.start()
                    broadcast(b"Connection is secured start communications")
                else:
                    broadcast(b"connection is not secured stop")
                    break
            else:
                print('with interception')
                test = quantum2()
                if test == True:
                    for cli in clients:
                        print('starting clients')
                        # Start Handling Thread For Client mettre cette partie la dans une auter fonction
                        thread = threading.Thread(target=handle, args=(cli,))
                        thread.start()
                    broadcast(b"Connection is secured start communications")
                else:
                    broadcast(b"connection is not secured stop")
                    break
                
receive()