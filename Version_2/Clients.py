# DIVINAGRACIA, ALIAH COLEEN L.
# BOGNALBAL, JIM OWEN K.
# ABAYON, CASANDRA P.

from socket import *
import threading
import sys

name = input("Enter your name: ")
HOST = '11.0.30.71' # Use 127.0.0.1 for self-hosting
PORT = 12345
RESET = "\033[0m"
my_color = "" # Initially empty, server will provide this [cite: 7]

def handle_receive(s):
    global my_color
    while True:
        try:
            data = s.recv(1024).decode()
            if not data: break
            
            # --- NEW: Handle the color assignment from the server ---
            if data.startswith("COLOR_ASSIGN:"):
                my_color = data.split(":")[1]
                continue # Don't print this internal message
            
            sys.stdout.write("\r\033[K")
            print(data)
            # Apply server-assigned color to local prompt [cite: 8]
            sys.stdout.write(f"{my_color}{name} (You): ")
            sys.stdout.flush()
        except: break

def handle_send(s):
    global my_color
    while True:
        # Repaint prompt with color locally [cite: 9, 10]
        msg = input(f"{my_color}{name} (You): ")
        s.send(msg.encode()) 
        if msg.lower() == 'exit': break

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))
s.send(name.encode())

t1 = threading.Thread(target=handle_receive, args=(s,))
t2 = threading.Thread(target=handle_send, args=(s,))
t1.start()
t2.start()

t1.join()
t2.join()
s.close()