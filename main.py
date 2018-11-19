import numpy as np
import cv2

import utils

import video_capture


def start():
    video = video_capture.VideoCapture()
    while True:
        frame = video.get_next_frame()
        colored_frame = utils.average_pixels(frame, 16, 8)
        cv2.imshow('res', colored_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    start()



