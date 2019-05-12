import logging

import cv2

logger = logging.getLogger(__name__)


class Video:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)

    def __enter__(self):
        return self

    def __iter__(self):
        if self.capture.isOpened():
            return self

        logger.error("Cannot open camera")
        raise IOError

    def __next__(self):
        ret, frame = self.capture.read()
        if ret:
            return frame

        logger.error("Camera read error")
        raise IOError

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.capture.release()
