import socket
import threading
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES
from quantum import encode_message
from quantum import gen_basis
from quantum import tobits
import pickle
import time
from tkinter import *
from tkinter import ttk

# def receive():
#     while True:
#         try:
#             # Receive Message From Server
#             # If 'NICK' Send Nickname
#             message = client.recv(1024)
#             #print(message)
#             if message == 'NICK':
#                 client.send(nickname.encode('ascii'))
#             else:
#                 print(message)
#         except:
#             # Close Connection When Error
#             print("An error occured!")
#             client.close()
#             break

# # Sending Messages To Server
# def write():
#     while True:
#         message = '{}: {}'.format(nickname, input(''))
#         client.send(message.encode('ascii'))


# win = Tk()

# win.config(bg = "#AC10CB")
# # Définir les dimensions par défaut la fenêtre principale :
# win.geometry("640x480")

# entrée1 = Entry (win)
# entrée1.pack()
# # # Choosing Nickname
# # nickname = input("Choose your nickname: ")
# # with tkinter
# def set_username():
#     nickname = entrée1.get()
#     print(nickname)

#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect(('3.9.117.24', 5050))    
#     # Starting Threads For Listening And Writing
#     receive_thread = threading.Thread(target=receive)
#     receive_thread.start()

#     write_thread = threading.Thread(target=write)
#     write_thread.start()


# nickname = ''
# ttk.Button(win, text= "username",width= 20, command= set_username).pack(pady=20)

# win.title("Mon application")

# win.geometry("640x480")
# # Affichage de la fenêtre créée :
# win.mainloop()

# # Connecting To Server
# #client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #client.connect(('3.9.117.24', 5050))

# key_test = ''
# key = ''

# # generate key
# def gen_key():
#     key = get_random_bytes(32)
#     #print(key)
#     cipher = AES.new(key, AES.MODE_EAX)
#     return key, cipher

# # transform the key to bits
# def key_to_bits(key):
#     s_key = key.decode('latin-1')
#     key_test = s_key
#     #print(s_key)
#     bits = tobits(s_key)
#     # basis = gen_basis(len(bits))
#     # #print(basis)
#     # key_to_send = encode_message(bits, basis)
#     # data = pickle.dumps(key_to_send)
#     message = '{}: {}'.format("key", bits)
#     client.send(message.encode('latin-1'))


# # Listening to Server and Sending Nickname
# # def receive():
# #     while True:
# #         try:
# #             # Receive Message From Server
# #             # If 'NICK' Send Nickname
# #             message = client.recv(1024)
# #             #print(message)
# #             if message == 'NICK':
# #                 client.send(nickname.encode('ascii'))
# #             else:
# #                 print(message)
# #         except:
# #             # Close Connection When Error
# #             print("An error occured!")
# #             client.close()
# #             break

# # # Sending Messages To Server
# # def write():
# #     while True:
# #         message = '{}: {}'.format(nickname, input(''))
# #         client.send(message.encode('ascii'))

# # # Starting Threads For Listening And Writing
# # receive_thread = threading.Thread(target=receive)
# # receive_thread.start()

# # write_thread = threading.Thread(target=write)
# # write_thread.start()

# # print('sending key...')
# # #time.sleep(5)
# # key, cipher = gen_key()
# # key_to_bits(key)

# # Ajout d'un titre à la fenêtre principale :


nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('3.9.117.24', 5050))

key_test = ''
key = ''

# generate key
def gen_key():
    key = get_random_bytes(32)
    #print(key)
    cipher = AES.new(key, AES.MODE_EAX)
    return key, cipher

# transform the key to bits
def key_to_bits(key):
    s_key = key.decode('latin-1')
    key_test = s_key
    #print(s_key)
    bits = tobits(s_key)
    # basis = gen_basis(len(bits))
    # #print(basis)
    # key_to_send = encode_message(bits, basis)
    # data = pickle.dumps(key_to_send)
    message = '{}: {}'.format("key", bits)
    client.send(message.encode('latin-1'))


# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024)
            #print(message)
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()