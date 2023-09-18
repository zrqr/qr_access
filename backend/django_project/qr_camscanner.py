from os import path, environ
from sys import path as sys_path
from django import setup

sys_path.append("setting.py")    
environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
setup()

import cv2
from qr_manager.models import QrCode
from qr_manager.views import check_qrcode
from rest_framework import status


def loopscan():
    print("START")
    cap = cv2.VideoCapture("http://192.168.0.7:8081/video.mjpg")
    # initialize the cv2 QRCode detector
    detector = cv2.QRCodeDetector()

    while True:
        _, img = cap.read()
    
        token, bbox, _ = detector.detectAndDecode(img)

        # check if there is a QRCode in the image
        if token:
            ret = check_qrcode(token)
            if ret == status.HTTP_200_OK:
                open_the_gate()

            if ret == status.HTTP_401_UNAUTHORIZED:
                print("Unauthorized")

        #cv2.imshow("QRCODEscanner", img)    
        if cv2.waitKey(1) == ord("q"):
            break

def open_the_gate():
    print("It is open")

if __name__ == "__main__":
    loopscan()