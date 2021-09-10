import socket
import os
import time

from _thread import *


def run(settings_map, introduce=False):

    # if metadata is not None:
    #     _setup_server_send(settings_map, metadata)
    # else:
    #     return _setup_server_rec(settings_map)

    # host_ip = settings_map['model_holders_ip']
    host_ip = settings_map['my_private_ip']
    host_port = int(settings_map['model_holders_port'])

    # print(host_ip)
    # print(host_port)

    others_metadata = None
    addr = None

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        if introduce:
            print("Connecting to Bob...")
            time.sleep(1)

        s.bind((host_ip, host_port))
        s.listen(1)  # We only want to connect with one person
        conn, addr = s.accept()
        with conn:
            if introduce:
                print("Connected - transferring public data\n")
                time.sleep(1)
            #print('Connected by', addr)
            while True:
                data = conn.recv(1024).decode()
                if others_metadata is None:
                    others_metadata = data
                if not data:
                    break

    # print(others_metadata)
    # addr[0] is the ip
    return others_metadata, addr[0]
