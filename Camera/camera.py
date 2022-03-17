import datetime
import picamera
import picamera.array
import cv2
from time import sleep
import requests


dt_now = datetime.datetime.now()

url = "https://notify-api.line.me/api/notify"
token = "発行したトークン"
headers = {"Authorization" : "Bearer "+ token} 

videopath="/home/pi/Camera/Video/"
picturepath="/home/pi/Camera/Picture/"
cascadepath="/home/pi/Camera/Cascade/"

cascade_face = cv2.CascadeClassifier(cascadepath + "haarcascade_frontalface_default.xml")

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (512, 384)
        sleep(2)
        camera.start_recording(videopath + str(dt_now) + '.h264')
        while True:
            camera.capture(stream, 'bgr', use_video_port=True)
            gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY)
            face = cascade_face.detectMultiScale(gray,scaleFactor=1.05, minNeighbors=2, minSize=(100, 100))
            if len(face) > 0:
                nowstr=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                for (x, y, w, h) in face:
                    cv2.rectangle(stream.array, (x, y), (x + w, y+h), (0, 0, 200), 3)
                cv2.imwrite(picturepath + str(nowstr) + ".jpeg", stream.array)
                line_img = picturepath + str(nowstr) + ".jpeg"
                payload = {"message" :  nowstr}
                files = {'imageFile': open(line_img, 'rb')}
                r = requests.post(url, headers = headers, params=payload,files=files,timeout=3.5)
                print(r)
            cv2.imshow('camera', stream.array)
            stream.seek(0)
            stream.truncate()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                camera.stop_recording()
                break
cv2.destroyAllWindows()