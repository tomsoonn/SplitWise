import base64

import cv2

from splitwise.recognise.receipt_reader import find_amount
from splitwise.recognise.video import Video


class ReceiptScanner(Video):

    @staticmethod
    def scanReceipt(frame):
        isOk, buffer = cv2.imencode('.jpg', frame)
        if not isOk:
            raise IOError

        encoded_string = base64.b64encode(buffer).decode("utf-8")
        amount = find_amount(encoded_string)
        return amount

    def runScanReceipt(self):
        print("Please press SPACE to save receipt or ESC to end program")

        while True:
            ret, frame = self.capture.read()
            cv2.imshow('Video', frame)
            key = cv2.waitKey(1)
            # hit space to continue reading
            if key == 32:
                retval, buffer = cv2.imencode('.jpg', frame)
                encoded_string = base64.b64encode(buffer).decode("utf-8")
                amount = find_amount(encoded_string)
                print(amount)
            elif key == 27:
                self.capture.release()
                break


if __name__ == '__main__':
    ter = ReceiptScanner()
    ter.runScanReceipt()
