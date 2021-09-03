import socket
import numpy as np
from io import BytesIO, StringIO
import os

class MessageSocket():
    def __init__(self):
        self.address = 0
        self.port = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.type = None  # server or client


    def startServer(self, address, port):
        self.type = "server"
        self.address = address
        self.port = port
        try:
            self.socket.connect((self.address, self.port))
            print('Connected to %s on port %s' % (self.address, self.port))
        except socket.error as e:
            print('Connection to %s on port %s failed: %s' % (self.address, self.port, e))
            return

    def endServer(self):
        self.socket.shutdown(1)
        self.socket.close()

    def sendMessage(self, message):
        if self.type is not "server":
            print("Not setup as a server")
            return
        try:
            self.socket.sendall(message)
        except Exception:
            exit()
        print('message sent')

    def startClient(self, port):
        self.type = "client"
        self.address = 'localhost' #''
        self.port = port

        self.socket.bind((self.address, self.port))
        self.socket.listen(1)
        print('waiting for a connection...')
        self.client_connection, self.client_address = self.socket.accept()
        print('connected to ', self.client_address[0])

        while True:
            client_input = self.client_connection.recv(1024).upper()
            # RUN_I_I, COMP_I, RUN_F_I,EXIT
            if client_input == 'COMP_I':
                    os.system("cd /home/sikha/MP-SPDZ/ && nohup ./compile.py -Y -R 64 " + "mpc_prog_infer_name" + ".mpc &")
                    os.system("cd /home/sikha/MP-SPDZ/ && nohup ./compile.py -Y -R 64 " + "mpc_prog_fair_name" + ".mpc &")
            elif client_input == 'RUN_I_I':
                    os.system("cd /home/sikha/MP-SPDZ/ && nohup Scripts/ring.sh " + "mpc_prog_infer_name &")
            elif client_input == 'RUN_I_I':
                    os.system("cd /home/sikha/MP-SPDZ/ && nohup Scripts/ring.sh " + "mpc_prog_fair_name &")

            elif client_input == 'EXIT':
                    self.endClient(self)
                    break
            else:
                    print("Unknown")


    def endClient(self):
        self.client_connection.shutdown(1)
        self.client_connection.close()


if __name__ == '__main__':
    messenger = MessageSocket()
    messenger.startClient(2000)

    #if server
    # call in main program
