import numpy as np
import cv2

import json


class VideoCapture:
    top_right = None
    top_left = None
    bottom_right = None
    bottom_left = None

    def __init__(self, width=640, height=480):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.width = width
        self.height = height
        self._get_settings('settings.json')

    def get_next_frame(self):
        ret, frame = self.cap.read()
        self.height, self.width, _ = frame.shape

        transformed_frame = self.transform_image(frame)

        return transformed_frame

    def get_corners(self):
        """Returns corners in top left, top right, bottom left, bottom right order"""
        return [self.top_left, self.top_right, self.bottom_left, self.bottom_right]

    def _get_settings(self, file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)
            try:
                corners = data['corners']
                self.top_right = (corners['top_right']['x'], corners['top_right']['y'])
                self.top_left = (corners['top_left']['x'], corners['top_left']['y'])
                self.bottom_right = (corners['bottom_right']['x'], corners['bottom_right']['y'])
                self.bottom_left = (corners['bottom_left']['x'], corners['bottom_left']['y'])
            except Exception as e:
                print(e)
                print(data)
                return

    def transform_image(self, img):
        """ Convert Trapezoidal region to Rectangle for easier calculations """

        bounds = np.float32([[0, 0], [self.width, 0], [0, self.height], [self.width, self.height]])
        corners = np.float32(self.get_corners())
        M = cv2.getPerspectiveTransform(corners, bounds)
        return cv2.warpPerspective(img, M, (self.width, self.height))
