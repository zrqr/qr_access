import cv2

def loopscan():
    
    cap = cv2.VideoCapture("http://192.168.0.7:8081/video.mjpg")
    # initialize the cv2 QRCode detector
    detector = cv2.QRCodeDetector()

    while True:
        _, img = cap.read()
    
        data, bbox, _ = detector.detectAndDecode(img)

        # check if there is a QRCode in the image
        if data:
            print(data)
            break


        cv2.imshow("QRCODEscanner", img)    
        if cv2.waitKey(1) == ord("q"):
            break

if __name__ == "__main__":
    loopscan()