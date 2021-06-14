import os
import datetime
import shutil
import csv
from pathlib import Path
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person
# import RPi.GPIO as GPIO

PERSON_GROUP_ID = "AUTHORIZEDFACE"

WORKING_DIR=os.path.dirname(__file__)
LATEST_PIC=1
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
        for file_name in now_files.glob("[0-9]+.*"):
            if os.path.splitext(os.path.join(file_name)) in EXTENSIONS:
                file_num = os.path.splitext(file_name)[0]
                if int(file_num) > LATEST_PIC:
                    LATEST_PIC=int(file_num)
            else:
                continue
    if NOW_PIC == LATEST_PIC:
        return 1
    else:
        return 0

def Face_Auth(face_dir):
    """
    result:
    1: Authorized
    0: Failed
    """
    
    
    img_url = "{DIR}\\face\\{PIC}.jpg".format(DIR=WORKING_DIR,PIC=LATEST_PIC)
    try:
        with open(img_url, 'r+b') as image:
            # face_ids = []
            # faces = FC.face.detect_with_stream(image, detection_model="detection_03")
            # for face in faces:
            #     face_ids.append(face.face_id)
            # results = FC.face.identify(face_ids, PERSON_GROUP_ID)
            # if results :
            #     for person in results:
            #         if len(person.candidates) > 0:
            #             return 1
            return 1;
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

def api_init(face_dir,auth_dir):
    # FC.person_group.create(person_group_id=PERSON_GROUP_ID,name=PERSON_GROUP_ID)
    # for i in range(100):
    # name = FC.person_group_person.create(PERSON_GROUP_ID, name)
    # auth_faces=[f.name for f in os.scandir(auth_dir) if f.is_file()]
    # for aface in auth_faces:
    #     try:
    #         with open("auth.csv", mode="a") as f:
    #             face_ID = FC.face.detect(os.path.join(auth_dir,aface))
    #             csvM=csv.writer(f)
    #             csvM.writerow(aface, face_ID["faceId"])
    #     except :
    #         pass
    pass

if __name__ == '__main__':
    face_dir=os.path.join(WORKING_DIR, "face")
    auth_dir=os.path.join(WORKING_DIR, "auth_face")
    shutil.rmtree(face_dir)
    os.mkdir(face_dir)
    # api_init(face_dir,auth_dir)
    main(face_dir=face_dir)
