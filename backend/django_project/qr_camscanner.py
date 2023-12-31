from os import path, environ
from sys import path as sys_path
from django import setup

import time
sys_path.append("setting.py")    
environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
setup()

import cv2

from qr_manager.views import check_qrcode, get_var
from rest_framework import status
from multiprocessing.pool import Pool
from multiprocessing import Queue, Value, Process, Lock

queue = Queue()
status = Value("b", False)
lock = Lock()

def process_image(img, detector):
    token, bbox, _ = detector.detectAndDecode(img)

    # check if there is a QRCode in the image
    if token:
        lock.acquire(timeout=1)
        ret = check_qrcode(token)
        lock.release()
        print(ret)
        if ret == 200:
            return True
        if ret == 401:
            print("Unauthorized")
            return False
        if ret == 410:
            print("Past Due")
            return False           

def process():
    detector = cv2.QRCodeDetector()
    while True:
        img = queue.get()
        if img is not None:
            if process_image(img, detector):
                status.value = True
        if status.value:
            time.sleep(5)


def loopscan():
    print("START")

    rtsp_address = get_var("rtsp")["value"]
    print(rtsp_address)
    cap = cv2.VideoCapture(rtsp_address)
    # initialize the cv2 QRCode detector

    count=0

    for i in range(3):
        p = Process(target = process)
        p.start()

    while True:
        ret, img = cap.read()
    
        if ret:
            if count % 10 == 0:
                if queue.qsize() < 5:
                    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    queue.put(gray_frame)
                
            count=count+1

            if status.value:
                
                print("It is open")
                while not queue.empty():
                    queue.get()
                time.sleep(5) 
                status.value = False

if __name__ == "__main__":
    loopscan()