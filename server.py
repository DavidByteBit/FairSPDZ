import socket
import os
from _thread import *


def run(settings_map, metadata=None):

    if metadata is not None:
        _setup_server_send(settings_map, metadata)
    else:
        return _setup_server_rec(settings_map)


def _setup_server_send(settings_map, metadata):

    host_ip = settings_map['model_holders_ip']
    host_port = int(settings_map['model_holders_port'])

    party_id = settings_map["party"]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host_ip, host_port))
        s.listen(1)  # We only want to connect with one person
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            conn.sendall(str(party_id) + metadata)


def _setup_server_rec(settings_map):

    host_ip = settings_map['model_holders_ip']
    host_port = int(settings_map['model_holders_port'])

    others_metadata = None

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host_ip, host_port))
        s.listen(1)  # We only want to connect with one person
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                others_metadata = conn.recv(10240)
                if not others_metadata:
                    break

    print(others_metadata)
    return others_metadata
