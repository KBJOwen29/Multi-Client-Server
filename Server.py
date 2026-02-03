from socket import *
from threading import Thread

all_connected_members = []

def send_to_all_members(message, current_sender_connection):
    for member in all_connected_members:
        if member != current_sender_connection:
            try:
                member.send(message)
            except:
                all_connected_members.remove(member)
                

def handle_individual_member(connection):
    while True:
        try:
            message_received = connection.recv(1024)
            if not message_received:
                break

            send_to_all_members(message_received, connection)
        except:
            break
    
    all_connected_members.remove(connection)
    connection.close()

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12345))
server_socket.listen()

print("Server is active and waiting for members...")

while True:
    
    connection, address = server_socket.accept()
    all_connected_members.append(connection)
    print(f"Member joined from {address}")
    
    Thread(target=handle_individual_member, args=(connection,)).start()
