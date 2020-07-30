import socket

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 5000         # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(10)
            size = int(data)
            data = conn.recv(size)
            if not data:
                break
            print(str(data))