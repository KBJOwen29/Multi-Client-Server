import socket
import threading

# Server Configuration
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345

# List to keep track of connected clients: (socket, name, color)
clients = []
lock = threading.Lock()

# Simple list of ANSI colors to assign to users
COLORS = ["\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m"]

def broadcast(message, sender_socket=None):
    """Sends a message to all clients except the sender."""
    with lock:
        for client_socket, _, _ in clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode())
                except:
                    client_socket.close()
                    remove_client(client_socket)

def remove_client(s):
    """Removes a client from the list."""
    with lock:
        for c in clients:
            if c[0] == s:
                clients.remove(c)
                break

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    try:
        # 1. Receive the name from client.py (s.send(name.encode()))
        name = conn.recv(1024).decode()
        
        # 2. Assign a color based on current client count
        color = COLORS[len(clients) % len(COLORS)]
        conn.send(f"COLOR_ASSIGN:{color}".encode())
        
        with lock:
            clients.append((conn, name, color))
            
        broadcast(f"\n*** {name} has joined the chat! ***")

        while True:
            # 3. Listen for messages
            msg = conn.recv(1024).decode()
            if not msg or msg.lower() == 'exit':
                break
            
            # Format: [Color][Name]: [Message][Reset]
            formatted_msg = f"{color}{name}: {msg}\033[0m"
            print(f"[{addr}] {name}: {msg}") # Server-side log
            broadcast(formatted_msg, conn)

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        broadcast(f"\n*** {name} has left the chat. ***")
        remove_client(conn)
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()