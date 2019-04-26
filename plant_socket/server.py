import socket
import threading
import json
from datetime import datetime
import os

from SqlConnection import SqlConnection

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 7800        # Port to listen on (non-privileged ports are > 1023)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()


def handle_client(client):
    client.settimeout(10)
    while True:
        try:
            data = client.recv(1024)
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
        save_data_sql(data_package)
        client.sendall(data)

def save_data(data_package):
    current_epoch_time = (datetime.now() - datetime(1970,1,1)).total_seconds()
    now = datetime.now()
    if '.' in data_package["name"]:
        print("Name cannot contain dots")
        return
    path = "/home/pi/plant_data_test/%s" % data_package["name"]
    if not os.path.exists(path):
        os.mkdir(path)

    f = open(path + "/%s-%s-%s.txt" % (now.year, now.month, now.day), 'a')
    f.write("%s\t%s\n" % (current_epoch_time, data_package["dryness"]))
    f.close()

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
        threading.Thread(target=handle_client, args=(client,)).start()
