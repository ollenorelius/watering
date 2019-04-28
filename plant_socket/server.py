import socket
import threading
import json
from datetime import datetime
import os

from SqlConnection import SqlConnection

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 7800        # Port to listen on (non-privileged ports are > 1023)


# Create the server listener socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()


def handle_client(client):
""" Handle a connection from one sensor."""
    client.settimeout(10)
    while True:
        try:
            data = client.recv(1024) #Receive up to 1024 bytes. In reality a data package should be around 100, so this is excessive
        except socket.timeout:
            break
        if not data:
            break
        print(data)
        try:
            data_package = json.loads(data.decode())
        except json.JSONDecodeError:
            print("Invalid request, data is not JSON")
            break
        if "name" not in data_package \
           or "dryness" not in data_package:
            print("Invalid keys in data")
            break
        save_data_sql(data_package) # If we are reasonably sure we got a correct JSON package, save it to the database


def save_data_sql(data_package):
    sql = SqlConnection()
    plants = [plant["name"] for plant in sql.get_plants()]
    if data_package["name"] not in plants:
        sql.add_plant(data_package["name"])

    sql.add_data_point(data_package["name"], data_package["dryness"])

if __name__ == "__main__":
    while True:
        client, addr = server_socket.accept()
        print('Connected by', addr)
        threading.Thread(target=handle_client, args=(client,)).start() # Handle each client in a separate thread.
