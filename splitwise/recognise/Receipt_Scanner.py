import cv2
import base64
import requests
import json
import re
from receipt_reader import find_amount

class Receipt_Scanner:
    def scan_receipt(self):
        video_capture = cv2.VideoCapture(0)
        print("Please press SPACE to save receipt or ESC to end program")

        while True:
            ret, frame = video_capture.read()
            cv2.imshow('Video', frame)
            key = cv2.waitKey(1)
            # hit space to continue reading
            if key == 32:
                retval, buffer = cv2.imencode('.jpg', frame)
                encoded_string = base64.b64encode(buffer).decode("utf-8")
                amount = find_amount(encoded_string)
                print(amount)
            elif key == 27:
                    video_capture.release()
                    break

ter = Receipt_Scanner()
ter.scan_receipt()
