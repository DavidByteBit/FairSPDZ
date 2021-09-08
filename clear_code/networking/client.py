import socket


def run(settings_map, metadata, host_ip=None, share_party_id=True):

    if host_ip is None:
        host_ip = settings_map["model_holders_ip"]

    host_port = int(settings_map['model_holders_port'])
    party_id = settings_map["party"]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host_ip, host_port))

        msg = ""

        if share_party_id:
            msg = str(party_id) + metadata
        else:
            msg = metadata

        print("sending: " + msg)
        s.sendall(str.encode(msg))
        # data = s.recv(1024)

    # print('Received', repr(data))



def _client_send(settings_map, metadata):

    host_ip = settings_map['model_holders_ip']
    host_port = int(settings_map['model_holders_port'])

    party_id = settings_map["party"]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host_ip, host_port))
        print("sending: " + str(party_id) + metadata)
        s.sendall(str.encode(str(party_id) + metadata))
        # data = s.recv(1024)

    # print('Received', repr(data))


def _client_rec(settings_map):

    host_ip = settings_map['model_holders_ip']
    host_port = int(settings_map['model_holders_port'])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host_ip, host_port))
        s.sendall(str.encode("looking for data"))
        others_metadata = s.recv(1024).decode()

    return others_metadata
