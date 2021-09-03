from pathlib import Path

import numpy as np
import requests
import json
import sys
import traceback

class messenger:
    def __init__(self):
        self.api_url = "http://localhost:8080/message"

    def sendMessage(self,message,isComplete=False):
        data = {"message": message, "completed": isComplete}
        headers = {"Content-Type":"application/json","message_type":'log'}
        response = requests.post(self.api_url, data=json.dumps(data), headers=headers)

    def sendResults(self,result,step):
        headers = {"Content-Type":"application/json","message_type":'result',"step":step}
        response = requests.post(self.api_url, data=json.dumps(result), headers=headers)

    def getAnnotations(self,data_path):
        try:
            response = requests.get(self.api_url)
            while response.status_code == 200:
                response = requests.get(self.api_url)
            annotations = json.load(response.json())  #{sample_id:{label:class,sensitive:gender}}
            labels = []
            sensitive = []
            for annotation in annotations.values():
                labels.append(int(annotation['label']))
                sensitive.append(int(annotation['sensitive']))
            with open(Path.joinpath(data_path, 'input_for_mpc_fair.txt'), 'a+') as outfile:
                np.savetxt(outfile, labels, delimiter='\n', fmt="%d")
            with open(Path.joinpath(data_path, 'input_for_mpc_fair.txt'), 'a+') as outfile:
                np.savetxt(outfile, sensitive, delimiter='\n', fmt="%d")
            outfile.close()
        except:
            print("Some error occurred. Please contact team with below information")
            print("Unexpected error:", sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[1])
            print(traceback.print_exc())
            sys.exit(1)
        return