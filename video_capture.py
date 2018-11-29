import numpy as np
import cv2

import json


class VideoCapture:
    top_right = None
    top_left = None
    bottom_right = None
    bottom_left = None
    settings_file = 'settings.json'

    def __init__(self, width=640, height=480):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.width = width
        self.height = height
        self._get_settings(self.settings_file)

    def get_next_frame(self):
        ret, frame = self.cap.read()
        self.height, self.width, _ = frame.shape
        return frame

    def get_corners(self):
        """Returns corners in top left, top right, bottom left, bottom right order"""
        return [self.top_left, self.top_right, self.bottom_left, self.bottom_right]

    def set_corners(self, new_corners):
        if len(new_corners) == 4:
            self.top_left = new_corners[0]
            self.top_right = new_corners[1]
            self.bottom_left = new_corners[2]
            self.bottom_right = new_corners[3]

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

    def save_settings(self):
        json_data = {
            'corners': {
                'top_left': {'x': self.top_left[0], 'y': self.top_left[1]},
                'top_right': {'x': self.top_right[0], 'y': self.top_right[1]},
                'bottom_left': {'x': self.bottom_left[0], 'y': self.bottom_left[1]},
                'bottom_right': {'x': self.bottom_right[0], 'y': self.bottom_right[1]}
            }
        }

        with open(self.settings_file, 'w') as f:
            json.dump(json_data, f)

    def transform_image(self, img):
        """ Convert Trapezoidal region to Rectangle for easier calculations """

        bounds = np.float32([[0, 0], [self.width, 0], [0, self.height], [self.width, self.height]])
        corners = np.float32(self.get_corners())
        M = cv2.getPerspectiveTransform(corners, bounds)
        return cv2.warpPerspective(img, M, (self.width, self.height))
