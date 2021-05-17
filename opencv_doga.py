
'''
入力：カメラから動画
出力：顔認識してモザイク
https://itport.cloud/?p=6983
'''

import cv2,os,time

#動画を読込み
#カメラ等でストリーム再生の場合は引数に0等のデバイスIDを記述する
video = cv2.VideoCapture(0)

LATEST_PIC = 0
FOLDER_NAME = "auth_face"
    

cascade_path = "haarcascade_frontalface_default.xml"
cascade = cv2.CascadeClassifier(cascade_path)

while video.isOpened():
    # フレームを読込み
    ret, frame = video.read()

    # フレームが読み込めなかった場合は終了（動画が終わると読み込めなくなる）
    if not ret: break
    # 顔検出
    facerect = cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))

    # 矩形線の色
    rectangle_color = (0, 255, 0) #緑色

    # 顔を検出した場合
    if len(facerect) > 0:
        LATEST_PIC+=1
        cv2.imwrite("{folder_name}/{image_num}.jpg".format(folder_name= FOLDER_NAME, image_num=LATEST_PIC), frame)
        time.sleep(10)


    # フレームの描画
    cv2.imshow('frame', frame)

    # qキーの押下で処理を中止
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break

    #save_frame('sample_video.mp4', 100, 'pic/'+AAA+'.jpg')

#メモリの解放
video.release()
cv2.destroyAllWindows()



