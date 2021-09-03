########################################################################
# Name: PRIVFAIR
# Contact: sikha@uw.edu
# Description: Read MPC output and fill desired json file
########################################################################
import traceback
from pathlib import Path
import json
import numpy as np
import sys





class ProcessFile:
    def __init__(self, data_path='./upload'):
        self.data_path = data_path
        self.EMOTION_CLASS = {'6': 'neutral', '3': 'happy', '4': 'sad', '0': 'angry',
                              '2': 'fearful', '1': 'disgust', '5': 'surprised'}

    def process_mpc_output_images_infer(self):
        try:
            set_inference = {}
            sample_id = 0
            with open(Path.joinpath(self.data_path, 'mpc_infer_out.txt'), 'r') as mpcfile:
                for line in mpcfile:
                    if line.startswith('Sample:'):
                        sample_inference = {}
                        str_prob = line.split(':')[1]
                        str_prob = str_prob.lstrip('[')
                        str_prob = str_prob.rstrip(']')
                        probs = str_prob.split(", ")
                        for ind,prob in enumerate(probs):
                            sample_inference[self.EMOTION_CLASS[str(ind)]] = float(prob)
                set_inference[sample_id] = sample_inference
                sample_id = sample_id + 1
            mpcfile.close()

        except:
            print("Some error occurred. Please contact team with below information")
            print("Unexpected error:", sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[1])
            print(traceback.print_exc())
            sys.exit(1)
        return json.dump(set_inference)


    def process_mpc_output_images_fair(self):
        json_metrics = {}
        try:
            metrics_male = {}
            metrics_female = {}
            final_metrics_male = {}
            final_metrics_female = {}

            with open(Path.joinpath(self.data_path, 'mpc_out.txt'), 'r') as mpcfile:
                for line in mpcfile:
                    if line.startswith('Male:'):
                        metrics = line.split(':')
                        for ind in range(1, len(metrics)):
                            keyval = metrics[ind].split('-')
                            metrics_male[keyval[0]] = np.fromstring(keyval[1][1:-1], dtype=float, sep=', ')
                    if line.startswith('Female:'):
                        metrics = line.split(':')
                        for ind in range(1, len(metrics)):
                            keyval = metrics[ind].split('-')
                            metrics_female[keyval[0]] = np.fromstring(keyval[1][1:-1], dtype=float, sep=', ')
                    if line.startswith('LogLoss:'):
                        metrics = line.split(':')
                        final_metrics_female['LogLoss'] = metrics[3]
                        final_metrics_male['LogLoss'] = metrics[2]
                        json_metrics['LogLoss'] = metrics[1]
            mpcfile.close()

            #
            # TPR = TP/(TP+FN)
            # TNR = TN/(TN+FP)
            # FPR = FP/(FP+TN)
            # FNR = FN/(TP+FN)

            with np.errstate(divide='ignore', invalid='ignore'):
                tpr_male = metrics_male['TP'] / (metrics_male['TP'] + metrics_male['FN'])
                tnr_male = metrics_male['TN'] / (metrics_male['TN'] + metrics_male['FP'])
                fpr_male = metrics_male['FP'] / (metrics_male['FP'] + metrics_male['TN'])
                fnr_male = metrics_male['FN'] / (metrics_male['TP'] + metrics_male['FN'])
                tpr_female = metrics_female['TP'] / (metrics_female['TP'] + metrics_female['FN'])
                tnr_female = metrics_female['TN'] / (metrics_female['TN'] + metrics_female['FP'])
                fpr_female = metrics_female['FP'] / (metrics_female['FP'] + metrics_female['TN'])
                fnr_female = metrics_female['FN'] / (metrics_female['TP'] + metrics_female['FN'])

            temp = {}
            for i in range(len(tpr_male)):
                temp[self.EMOTION_CLASS[str(i)]] = tpr_male[i]
            final_metrics_male['TPR'] = temp
            temp = {}
            for i in range(len(tnr_male)):
                temp[self.EMOTION_CLASS[str(i)]] = tnr_male[i]
            final_metrics_male['TNR'] = temp
            temp = {}
            for i in range(len(fpr_male)):
                temp[self.EMOTION_CLASS[str(i)]] = fpr_male[i]
            final_metrics_male['FPR'] = temp
            temp = {}
            for i in range(len(fnr_male)):
                temp[self.EMOTION_CLASS[str(i)]] = fnr_male[i]
            final_metrics_male['FNR'] = temp

            temp = {}
            for i in range(len(tpr_female)):
                temp[self.EMOTION_CLASS[str(i)]] = tpr_female[i]
            final_metrics_female['TPR'] = temp
            temp = {}
            for i in range(len(tnr_female)):
                temp[self.EMOTION_CLASS[str(i)]] = tnr_female[i]
            final_metrics_female['TNR'] = temp
            temp = {}
            for i in range(len(fpr_female)):
                temp[self.EMOTION_CLASS[str(i)]] = fpr_female[i]
            final_metrics_female['FPR'] = temp
            temp = {}
            for i in range(len(fnr_female)):
                temp[self.EMOTION_CLASS[str(i)]] = fnr_female[i]
            final_metrics_female['FNR'] = temp

            json_metrics['Male'] = final_metrics_male
            json_metrics['Female'] = final_metrics_female


            #with open(Path.joinpath(self.data_path, 'metrics.json'), "w") as outfile:
            #    json.dump(json_metrics, outfile)

        except:
            print("Some error occurred. Please contact team with below information")
            print("Unexpected error:", sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[1])
            print(traceback.print_exc())
            sys.exit(1)
        return json.dump(json_metrics)

    def process_mpc_output_tab(self):
        try:
            print("To implement")
        except:
            print("Some error occurred. Please contact team with below information")
            print("Unexpected error:", sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[1])
            print(traceback.print_exc())
            sys.exit(1)

    def process_mpc_output_other(self):
        try:
            print("To implement")
        except:
            print("Some error occurred. Please contact team with below information")
            print("Unexpected error:", sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[1])
            print(traceback.print_exc())
            sys.exit(1)
