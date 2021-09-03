
import cv2
import sys
from os import listdir
from os.path import isfile, join


def preprocess_video(path_to_video,emotion,gender,actor):

    try:
        vid_reader = cv2.VideoCapture(path_to_video)
        frame_num = 0
        num_frames_read = 0
        while True:
            grabbed = vid_reader.grab()
            if grabbed:
                if frame_num % 15 == 0:
                    vid_frame = vid_reader.retrieve()[1]
                    cv2.imwrite("/Users/sikha/Documents/RAVDESS/Sample/" + "/PROC_" + str(actor)+ str(frame_num)+ ".jpg__"
                    +str(emotion)+"__"+str(gender) + "__img", vid_frame)
                    #__"+str(emotion)+"__"+str(gender)+"__img"
            else:
                break
            frame_num += 1
    except:
        print("Exception raised in pre_process_video: " + str(sys.exc_info()[1]))

files_to_read = [f for f in listdir('/Users/sikha/Documents/RAVDESS/test/') if isfile(join('/Users/sikha/Documents/RAVDESS/test/', f)) and (f[-4:] == '.mp4')]
for filename in files_to_read:
    vid_meta_data = filename.split("-")
    #print(len(vid_meta_data))
    emotion = int(vid_meta_data[2])
    if emotion == 1:
        emotion_label = 6
    elif emotion == 3:
        emotion_label = 3
    elif emotion == 4:
        emotion_label = 4
    elif emotion == 5:
        emotion_label = 0
    elif emotion == 6:
        emotion_label = 2
    elif emotion == 7:
        emotion_label = 1
    elif emotion == 8:
        emotion_label = 5

    gender = int(vid_meta_data[6].split(".")[0])
    if gender % 2 == 0:
        genderA = 0
    else:
        genderA = 1
    preprocess_video('/Users/sikha/Documents/RAVDESS/test/'+ filename,emotion_label,genderA,gender)