import os
import datetime
import shutil
import csv
from pathlib import Path

WORKING_DIR=os.path.dirname(__file__)
LATEST_PIC=0
EXTENSIONS=["PNG","png","jpg","jpeg","gif","BMP","bmp"]

KEY = 'サブスクリプションキー'
BASE_URL = 'https://japaneast.api.cognitive.microsoft.com/face/v1.0']

def check_dir(face_dir):
    """
    result:
    1: find new file
    0: no changes
    """
    NOW_PIC=LATEST_PIC
    now_files = Path(face_dir)
    if now_files is not None:
        for file_name in now_files.glob("[0-9]+.*"):
            if os.path.splitext(os.path.join(file_name) in EXTENSIONS:
                file_num = os.path.splitext(file_name)[0]
                if int(file_num) > LATEST_PIC:
                    LATEST_PIC=int(file_num)
            else:
                continue
    if NOW_PIC == LATEST_PIC:
        return 1
    else:
        return 0

def API_manager():
    """
    result:
    1: Authorized
    0: Failed
    """

    img_url = "{DIR}face/{PIC}.png".format(DIR=WORKING_DIR,PIC=LATEST_PIC)
    faces = CF.face.detect(img_url, attributes='emotion')

    pass

def open_the_door():
    pass

def logging(auth_result):
    with open("FaceIDoor.log", mode="a") as log:
        text="{date}:{auth}".format(date=datetime.datetime.now(), auth=("Authorized" if auth_result else "Failed"))
        log.write(text)

def main(face_dir):
    if check_dir(face_dir):
        auth_result = API_manager(face_dir)
        if auth_result:
            open_the_door()
        logging(auth_result)

if __name__ == '__main__':
    face_dir=os.path.join(WORKING_DIR, "face")
    auth_file=os.path.join(WORKING_DIR, "auth")
    shutil.rmtree(face_dir)
    os.mkdir(face_dir)
    CF.Key.set(KEY)
    CF.BaseUrl.set(BASE_URL)
    auth_faces=Path(os.path.join(WORKING_DIR, "auth_face"))
    for aface in authfaces:
        try:
            with open("auth.csv", mode="a") as f:
                face_ID = CF.face.detect(os.path.join(WORKING_DIR,"auth_face",aface))
                csvM=csv.writer(f)
                csvM.writerow(aface, face_ID["faceId"])
        except 
            pass
    main(face_dir=face_dir)

    
