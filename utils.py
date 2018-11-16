import numpy as np
import cv2

def create_roi(points):
    return np.array([points], dtype=np.int32)


def average_point(point1, point2):
    """Takes the average between two points as tuples (x,y)"""
    return (point1[0] + point2[0]) // 2, (point1[1] + point2[1]) // 2


def transform_image(img, quadrilateral):
    '''
        Convert Trapezoidal region to Rectangle for easier calculations
    '''

    bounds = np.float32([[0, 0], [640, 0], [0, 480], [640, 480]])
    corners = np.float32(quadrilateral.get_corners())
    M = cv2.getPerspectiveTransform(corners, bounds)
    dst = cv2.warpPerspective(img, M, (640, 480))
    return dst


class quad:
    """Four dimensional polygon defined by 4 corners"""
    top_left = None
    top_right = None
    bottom_left = None
    bottom_right = None

    def get_corners(self):
        """Returns corners in top left, top right, bottom left, bottom right order"""
        return [self.top_left, self.top_right, self.bottom_left, self.bottom_right]
