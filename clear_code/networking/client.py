import socket
import time


def run(settings_map, metadata, host_ip=None, share_party_id=True, introduce=False):

    if host_ip is None:
        host_ip = settings_map["model_holders_ip"]

    host_port = int(settings_map['model_holders_port'])
    party_id = settings_map["party"]

    if introduce:
        print("Connecting to Bob...\n")
        time.sleep(1)

    attempts = 0
    max_attempts = 500

    while attempts < max_attempts:
        attempts += 1
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host_ip, host_port))
                # Not the cleanest, but ensures we leave the while loop
                # TODO: Find a better way to query for connection to a host that may not be ready
                attempts = max_attempts

                if introduce:
                    print("Connected to Bob - Hello Bob!\n")
                    time.sleep(1)

                msg = ""

                if share_party_id:
                    msg = str(party_id) + metadata
                else:
                    msg = metadata

                # print("sending: " + msg)
                s.sendall(str.encode(msg))
                # data = s.recv(1024)

        except Exception:
            time.sleep(0.1)

    # print('Received', repr(data))
