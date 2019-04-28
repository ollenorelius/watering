import socket
""" Test program. Sends a simple message to the database. """
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 7800        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'{"name": "Doot", "dryness": 123}')
    data = s.recv(1024)

print('Received', repr(data))
