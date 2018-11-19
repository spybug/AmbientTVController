import numpy as np
import cv2

def create_roi(points):
    return np.array([points], dtype=np.int32)


def average_point(point1, point2):
    """Takes the average between two points as tuples (x,y)"""
    return (point1[0] + point2[0]) // 2, (point1[1] + point2[1]) // 2


def average_pixels (image, horiz=16, vert=8):
    '''
    Apply a convolution (maybe) over the image to average colors of the scene.
    u x x u     x = horizontal_regions
    y     y     y = vertical_regions
    y     y     u = nodes computed in both directions, for simplicity
    u x x u

    We want to create regions that will represent a single node (LED) in
    the final output. The constants are defined with defaults.
    '''
    # print image.shape
    height, width = image.shape[:2]
    horiz_pixels = int(width / horiz)
    vert_pixels = int(height / vert)

    # top row
    for col in range(horiz):
        bl = horiz_pixels
        tl = vert_pixels * col
        tr = vert_pixels * (col + 1)
        # returns tuple of len 4, but we ignore alpha channel
        color = np.uint8(cv2.mean(image[0:bl, tl:tr])[:3])
        image[0:bl, tl:tr] = color

    # left col
    for row in range(vert):
        rh = horiz_pixels
        top = vert_pixels * row
        bot = vert_pixels * (row + 1)
        color = np.uint8(cv2.mean(image[top:bot, 0:rh])[:3])
        image[top:bot, 0:rh] = color


    # right col
    for row in range(vert):
        rh = width
        lh = rh - horiz_pixels
        top = vert_pixels * row
        bot = vert_pixels * (row + 1)
        color = np.uint8(cv2.mean(image[top:bot, lh:rh])[:3])
        image[top:bot, lh:rh] = color

    # bottom row
    for col in range(horiz):
        bot = height
        top = bot - vert_pixels
        lh = horiz_pixels * col
        rh = horiz_pixels * (col + 1)
        color = np.uint8(cv2.mean(image[top:bot, lh:rh])[:3])
        image[top:bot, lh:rh] = color

    return image


class quad:
    """Four dimensional polygon defined by 4 corners"""
    top_left = None
    top_right = None
    bottom_left = None
    bottom_right = None

    def get_corners(self):
        """Returns corners in top left, top right, bottom left, bottom right order"""
        return [self.top_left, self.top_right, self.bottom_left, self.bottom_right]
