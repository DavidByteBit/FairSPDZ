#! /usr/bin/python

#######################################################################
# Name: PRIVFAIR
# Contact: sikha@uw.edu
# Description: Main file checks the command line arguments
#######################################################################
import os
import pathlib
import subprocess
import sys
import traceback

from paramiko.client import SSHClient

import fileprocessor

import datetime
import argparse

import messagingSocket
import preprocess
import shutil
from pathlib import Path
import shlex
import CONSTANTS as C
import messagingObj
import scp

# Main
# Arguments - input_path for each session, output_path json

if __name__ == '__main__':
    try:
        messenger_obj = messagingObj.messenger()

        # messenger_mpc = messagingSocket.MessageSocket()

        #messenger_obj.sendMessage("<=== PrivFair: Private Auditing of Fairness on Machine Learning Models  ===>", False)
        #messenger_obj.sendMessage("<=== Processing Started  ===>", False)
        #messenger_obj.sendMessage("1. Parsing Arguments", False)

        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input_path',
                            required=True,
                            type=pathlib.Path,
                            default='./upload',
                            dest="input_path",
                            metavar="<absolute_path_input>",
                            help="Absolute path of the zip file of images")
        parser.add_argument('-d', '--data_type',
                            required=True,
                            type=str,
                            default='img',
                            dest="data_type",
                            metavar="<type_of_data>",
                            help="Type of data to be evaluated, Allowed - img, tab")

        args = parser.parse_args()
        data_type = args.data_type

        #messenger_obj.sendMessage("2. Preprocess data", False)

        pre_processor = preprocess.ProcessRawData(args.input_path)
        pre_process_method = getattr(pre_processor, C.PRE_PROCESS_FUNC[data_type])
        public_const = pre_process_method()
        #messenger_obj.sendMessage("Processed " + str(public_const[0]) + " samples", False)
        if public_const[0] == 0:
            #messenger_obj.sendMessage("No samples to evaluate on", False)
            sys.exit(1)

        '''
        messenger_obj.sendMessage("3. Declare public constants", False)
        public_file_name = '/home/sikha/MP_SPDZ/' + C.SAMPLE_MPC_PROG_NAME[data_type]
        with open(public_file_name, 'w') as public_file:
            for constant in public_const:
                public_file.write(constant)
        public_file.close()

        messenger_obj.sendMessage("4.0 Secret share private inputs of data and annotations to 3 MP-SPDZ engines via INPUT-P0-0", False)
        shutil.copyfile(str(Path.joinpath(args.input_path, 'input_for_mpc_data.txt')),
                        '/home/sikha/MP-SPDZ/Player-Data/Input-P0-0')

        if data_type == 'tab':
            messenger_obj.sendMessage("4.1. Secret share private inputs of model to 3 MP-SPDZ engines via INPUT-P0-0 INPUT-P1-0", False)
            shutil.copyfile(str(Path.joinpath(args.input_path, 'input_for_mpc_model.txt')),
                            '/home/sikha/MP-SPDZ/Player-Data/Input-P1-0')
        elif data_type == 'img':
            messenger_obj.sendMessage("4.1. Get secret shares of selected model", False)

        messenger_obj.sendMessage("5.1 Compile MPC programs", False)
        mpc_program_name = C.SAMPLE_MPC_PROG_NAME[data_type]
        os.system("cd /home/sikha/MP-SPDZ/ && ./compile.py -Y -R 64 " + mpc_program_name + ".mpc")

        ''''''
        if C.NUM_MPC_VMS > 1:
            # Step 5 will change
            for host in C.MPC_HOSTS:
                #ssh = SSHClient()
                #ssh.load_system_host_keys()
                #connect_str = 'privfair@' + host + ':/home/sikha/MP-SPDZ/Programs/'
                #ssh.connect('user@server:path')
                #with scp.SCPClient(ssh.get_transport()) as scpl:
                #    scpl.put('/home/sikha/MP-SPDZ/Programs/' + C.SAMPLE_MPC_PUBLIC_FILE_FAIR[data_type], 'my_file.txt')
                # Better to have a port listening and run python program: other hosts will run messaging socket
                messenger_mpc.startServer(host, C.MPC_PORT)
                messenger_mpc.sendMessage("COMP_" + data_type[0].upper())
                messenger_mpc.endServer()
                # i_i, o_i, e_i = ssh.exec_command("cd /home/sikha/MP-SPDZ/ && nohup ./compile.py -Y -R 64 " + mpc_prog_infer_name + ".mpc &")
                # i_f, o_f, e_f = ssh.exec_command("cd /home/sikha/MP-SPDZ/ && nohup ./compile.py -Y -R 64 " + mpc_prog_fair_name + ".mpc &")
        ''''''

        messenger_obj.sendMessage("5.2 Run MPC program on 3 MP-SPDZ engines ", False)

        run_command = "cd /home/sikha/MP-SPDZ/ && " + C.MPC_PROTOCOL[C.NUM_MPC_VMS] + " " + mpc_program_name + \
                      " > /home/sikha/Sample/mpc_infer_out.txt"
        os.system(run_command)

        # if C.NUM_MPC_VMS > 1:
        #    for host in C.MPC_HOSTS:
        #        messenger_mpc.startServer(host, C.MPC_PORT)
        #        if data_type == 'img':
        #            messenger_mpc.sendMessage("RUN_" + data_type[0].upper() + "_I")
        #        else:
        #            messenger_mpc.sendMessage("RUN_" + data_type[0].upper())
        #        messenger_mpc.endServer()

        messenger_obj.sendMessage("6. Private fairness evaluation completed, get data from file and parse it as json")
        file_parser = fileprocessor.ProcessFile(args.input_path)
        file_parse_method = getattr(file_parser, C.FILE_PROCESSOR_FAIR[data_type])
        json_results = file_parse_method()
        messenger_obj.sendResults(json_results, 1)

        messenger_obj.sendMessage("7. Display metrics to user ")
        '''
        #messenger_obj.sendMessage("<=== Processing Ended ===>")

    except:
        print("Some error occurred. Please contact team with below information")
        print("Unexpected error:", sys.exc_info()[0])
        print("Unexpected error:", sys.exc_info()[1])
        print(traceback.print_exc())
