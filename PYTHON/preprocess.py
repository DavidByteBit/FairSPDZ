########################################################################
# Name: PRIVFAIR
# Contact: sikha@uw.edu
# Description: Preprocess uploaded images
# Assumptions: The images have convention for file name
########################################################################
import traceback
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import log_loss
from keras_preprocessing.image import img_to_array
import sys
from os import listdir
from os.path import isfile, join
import cv2
from mtcnn import MTCNN
import logging
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.models import load_model
import keract

class ProcessRawData:
    def __init__(self, data_path='./upload'):
        self.data_path = data_path
        self.model = load_model("/Users/sikha/Desktop/ICML/Supplementary_PPVC_ICML/SourceCode/models/trainedACT.h5")

    def pre_process_images(self):
        return_public_const = []
        files_count = 0
        try:
            files_to_read = [f for f in listdir(self.data_path) if
                             isfile(join(self.data_path, f)) and (f[-5:] == '__img' or f[-4] == '.jpg')]
                             #(f[-4:] == '.jpg' or f[-5:] == '__img' or f[-4:] == '.png')]
            if len(files_to_read) > 0:
                labels = []
                gender = []
                probs = []
                detector = MTCNN()

                for filename in files_to_read:
                    file_parts = filename.split('__')
                    labels.append(int(file_parts[1]))
                    gender.append(int(file_parts[2]))

                    image = cv2.imread(str(Path.joinpath(self.data_path, filename)))
                    # image_gray = cv2.imread(Path.joinpath(self.data_path, filename),0)
                    faces = detector.detect_faces(image)
                    if faces is not None and len(faces) != 0:
                        if faces[0]['confidence'] > 0.98:
                            rows, cols = image.shape[:2]
                            rightEyeCenter = faces[0]['keypoints']['right_eye']
                            leftEyeCenter = faces[0]['keypoints']['left_eye']
                            dY = rightEyeCenter[1] - leftEyeCenter[1]
                            dX = rightEyeCenter[0] - leftEyeCenter[0]
                            angle = np.degrees(np.arctan2(dY, dX)) - 360

                            # To align face rotate frame, and crop face and resize to 299,299
                            transform_Matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
                            frame_rotated = cv2.warpAffine(image, transform_Matrix, (cols, rows))
                            if len(frame_rotated) == 0:
                                logging.warning("Rotated Frame is empty")

                            faces_rot = detector.detect_faces(frame_rotated)
                            if faces_rot is not None and len(faces_rot) != 0:
                                if faces_rot[0]['confidence'] > 0.98:
                                    (x, y, w, h) = faces_rot[0]['box']
                                    face_frame = cv2.resize(frame_rotated[y - 0:y + h + 0,
                                                            x - 0:x + w + 0],
                                                            (48, 48),
                                                            # (10,10),
                                                            interpolation=cv2.INTER_CUBIC)
                                    face_frame = cv2.cvtColor(face_frame, cv2.COLOR_BGR2GRAY)

                                    # cv2.imwrite("/Users/sikha/Documents/RAVDESS/processed/" + "/PROC_"
                                    #            + str(filename) + ".jpg", face_frame)
                                    face_frame = img_to_array(face_frame)
                                    face_frame = np.array(face_frame, dtype="float32") / 255.0
                                    face_frame = np.expand_dims(face_frame, axis=0)  # (1,48,48,1)


                                    y_p = self.model.predict(face_frame)[0]
                                    emotion_inference_logits = keract.get_activations(self.model, face_frame,
                                                                                     layer_names='dense_5')['dense_5'][0]
                                    probs.append(y_p)
                                    print(emotion_inference_logits)

                                    with open(Path.joinpath(self.data_path, 'input_for_mpc.txt'), 'w+') as outfile:
                                        for i in range(0, face_frame.shape[1]):
                                            for j in range(0, face_frame.shape[2]):
                                                np.savetxt(outfile, face_frame[0, i, j, :], fmt='%14.13f', delimiter='\n')

                                    files_count = files_count + 1
                lb = LabelBinarizer() # preload a label binarizer for 7
                lb.fit([0,1,2,3,4,5,6])
                ohe_labels = lb.transform(labels) # use only transform
                with open(Path.joinpath(self.data_path, 'input_for_mpc.txt'), 'a+') as outfile:
                    np.savetxt(outfile, ohe_labels, delimiter='\n', fmt="%d")
                with open(Path.joinpath(self.data_path, 'input_for_mpc.txt'), 'a+') as outfile:
                    np.savetxt(outfile, gender, delimiter='\n', fmt="%d")
                outfile.close()
                sensitive_indices_male = []
                sensitive_indices_female = []
                for ind in range(len(gender)):
                    if gender[ind] == 1:
                        sensitive_indices_male.append(ind)
                    else:
                        sensitive_indices_female.append(ind)

                y_truth_male = [labels[x] for x in sensitive_indices_male]
                y_truth_female = [labels[x] for x in sensitive_indices_female]

                y_predict_male = [probs[x] for x in sensitive_indices_male]
                y_predict_female = [probs[x] for x in sensitive_indices_female]
                print(log_loss(labels,probs,labels=[0,1,2,3,4,5,6]))
                print(log_loss(y_truth_male,y_predict_male,labels=[0,1,2,3,4,5,6]))
                print(log_loss(y_truth_female,y_predict_female,labels=[0,1,2,3,4,5,6]))
                print(probs)
                return_public_const.append(files_count)
                return_public_const.extend([7,48,48,1])
            else:
                return_public_const.append(files_count)
        except:
            print("Some error occurred. Please contact team with below information")
            print("Unexpected error:", sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[1])
            print(traceback.print_exc())
            sys.exit(1)
        return return_public_const



    def pre_process_tab(self):
        try:
            print("To implement")
            return_public_const = []
            row_count = 0
            col_count = 0
            return_public_const.append(row_count)
            return_public_const.append(2)
            return_public_const.append(col_count)
        except:
            print("Some error occurred. Please contact team with below information")
            print("Unexpected error:", sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[1])
            print(traceback.print_exc())
            sys.exit(1)
        return return_public_const

    def pre_process_audio(self):
        try:
            print("To implement")
            return_public_const = []
            file_count = 0
            return_public_const.append(file_count)
            return_public_const.append(2)
        except:
            print("Some error occurred. Please contact team with below information")
            print("Unexpected error:", sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[1])
            print(traceback.print_exc())
            sys.exit(1)
        return return_public_const

    def pre_process_other(self):
        try:
            print("To implement")
            return_public_const = []
            sample_count = 0
            return_public_const.append(sample_count)
            return_public_const.append(2)
        except:
            print("Some error occurred. Please contact team with below information")
            print("Unexpected error:", sys.exc_info()[0])
            print("Unexpected error:", sys.exc_info()[1])
            print(traceback.print_exc())
            sys.exit(1)
        return return_public_const
