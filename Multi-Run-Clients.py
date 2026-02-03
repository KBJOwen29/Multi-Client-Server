from socket import *
from threading import Thread

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(("127.0.0.1", 12345))

def receive_messages_from_server():
    while True:
        try:
            incoming_message = client_socket.recv(1024).decode()
            print(f"\nFriend: {incoming_message}")
            print("You: ", end="") 
        except:
            print("Lost connection to server.")
            break
        

def send_messages_to_server():
    while True:
        my_message = input("You: ")
        client_socket.send(my_message.encode())


Thread(target=receive_messages_from_server).start()
Thread(target=send_messages_to_server).start()
