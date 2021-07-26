import os
import datetime
import shutil
import csv
import numpy
import sys
import time
from pathlib import Path
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person
# import RPi.GPIO as GPIO

PERSON_GROUP_ID = "authorizedface"

WORKING_DIR=os.path.dirname(__file__)
LATEST_PIC=1
LAST_PIC=0
EXTENSIONS=["PNG","png","jpg","jpeg","gif","BMP","bmp"]

KEY = 'b58b2e93530b40c9b0f508926451c21d'
BASE_URL = 'https://japaneast.api.cognitive.microsoft.com/face/v1.0'
END_POINT = 'https://faceidoor.cognitiveservices.azure.com/'
AREA = 'japanwest'

FC = FaceClient(END_POINT, CognitiveServicesCredentials(KEY))

def check_dir(face_dir):
    """
    result:
    1: find new file
    0: no changes
    """
    global LATEST_PIC
    NOW_PIC=LATEST_PIC
    now_files = Path(face_dir)
    if now_files is not None:
        for file_name in now_files.glob("[0-9][0-9]*.*"):
            if os.path.splitext(os.path.join(file_name))[-1][1:] in EXTENSIONS:
                file_num = os.path.splitext(file_name)[0]
                if int(file_num) > LATEST_PIC:
                    LATEST_PIC=int(file_num)
            else:
                print(os.path.splitext(os.path.join(file_name))[-1][1:])
                print(file_name)
                continue
            print(file_name)
    if NOW_PIC == LATEST_PIC:
        return 0
    else:        
        return 1

def Face_Auth(face_dir):
    """
    result:
    1: Authorized
    0: Failed
    """
    global LAST_PIC
    if LAST_PIC == LATEST_PIC:
        return 0;
    
    img_url = os.path.join(face_dir,"{PIC}.jpg".format(PIC=LATEST_PIC))
    LAST_PIC = LATEST_PIC
    try:
        with open(img_url, 'r+b') as image:
            face_ids = []
            faces = FC.face.detect_with_stream(image, detection_model="detection_03") # the faces including in pic
            for face in faces:
                face_ids.append(face.face_id)
            results = FC.face.identify(face_ids, PERSON_GROUP_ID) 
            if results :
                for person in results:
                    if len(person.candidates) > 0:
                        print(person.candidates)
                        return 1
    except FileNotFoundError as e :
        print(e)
        return 0
    return 0

def open_the_door():
    gpio_authorize = 17
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(gpio_authorize, GPIO.OUT)
    # GPIO.output(gpio_authorize, 1)
    # GPIO.output(gpio_authorize, 0)

def logging(auth_result):
    with open("FaceIDoor.log", mode="a") as log:
        text="{date}:{auth}\n".format(date=datetime.datetime.now(), auth=("Authorized" if auth_result else "Failed"))
        log.write(text)

def main(face_dir):
    while True:
        if check_dir(face_dir):
            auth_result = Face_Auth(face_dir)
            if auth_result:
                open_the_door()
            logging(auth_result)
            time.sleep(60) # API limit is one call per 60s

def make_person_group(auth_dir):
    try:
        FC.person_group.create(person_group_id=PERSON_GROUP_ID,name=PERSON_GROUP_ID)
    except : # azure.cognitiveservices.vision.face.models._models_py3.APIErrorException
        # FC.person_group.delete(person_group_id=PERSON_GROUP_ID)
        # FC.person_group.create(person_group_id=PERSON_GROUP_ID,name=PERSON_GROUP_ID)
        return
    name_kind = os.listdir(path=auth_dir) # define face tag
    auth_faces = [[] for _ in range(len(name_kind))] #  auth_face[who][pic of face]
    PG_persons = [] #len(name_kind))
    for i, name in zip(range(len(name_kind)), name_kind):
        PG_persons.append(FC.person_group_person.create(PERSON_GROUP_ID, name)) # make person in PG
        auth_faces[i].append([os.path.join(auth_dir, name, f.name) for f in os.scandir(os.path.join(auth_dir, name)) if f.is_file()])
    for i,names in zip(range(len(auth_faces)),auth_faces):
        for face_name in names :
            for face_file in face_name:
                try:
                    # with open("auth.csv", mode="a") as f:
                    #     face_ID = FC.face.detect(os.path.join(auth_dir,aface))
                    #     csvM=csv.writer(f)
                    #     csvM.writerow(aface, face_ID["faceId"])
                    with open(face_file, 'r+b') as ff :
                        try:
                            FC.person_group_person.add_face_from_stream(PERSON_GROUP_ID, PG_persons[i].person_id, ff)
                        except :
                            print("No face detected in " + face_file)
                            pass
                except Exception as e:
                    FC.person_group.delete(person_group_id=PERSON_GROUP_ID)
                    print(PG_persons[i])
                    sys.exit(e)
    FC.person_group.train(PERSON_GROUP_ID)
    while True :
        training_status = FC.person_group.get_training_status(PERSON_GROUP_ID)
        print("Traning Status: {}".format(training_status))
        if training_status.status is TrainingStatusType.succeeded:
            break
        elif training_status.status is TrainingStatusType.failed:
            FC.person_group.delete(person_group_id=PERSON_GROUP_ID)
            sys.exit('Training the person group has failed.')
        time.sleep(5)

if __name__ == '__main__':
    face_dir=os.path.join(WORKING_DIR, "face")
    auth_dir=os.path.join(WORKING_DIR, "auth_face")
    shutil.rmtree(face_dir)
    os.mkdir(face_dir)
    make_person_group(auth_dir)
    main(face_dir=face_dir)
