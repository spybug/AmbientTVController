import numpy as np
import cv2


def create_roi(points):
    return np.array([points], dtype=np.int32)


def average_point(point1, point2):
    """Takes the average between two points as tuples (x,y)"""
    return (point1[0] + point2[0]) // 2, (point1[1] + point2[1]) // 2


def average_pixels(image, horiz=16, vert=8):
    '''
    Creates regions that will represent a single LED in
    the final output. The constants are defined for horizontal and vertical pixel amounts

    Order should be clockwise starting from bottom left up, top left right, top right down, bottom right left
    '''

    height, width = image.shape[:2]
    horiz_pixels = int(width / horiz)
    vert_pixels = int(height / vert)

    color_buffer = []

    # left col (bottom -> top)
    for row in range(vert, -1, -1):
        rh = horiz_pixels
        top = vert_pixels * row
        bot = vert_pixels * (row + 1)

        color = np.uint8(cv2.mean(image[top:bot, 0:rh])[:3])
        color_buffer.append(tuple(color))

    # top row (left -> right)
    for col in range(horiz):
        bl = horiz_pixels
        tl = vert_pixels * col
        tr = vert_pixels * (col + 1)

        color = np.uint8(cv2.mean(image[0:bl, tl:tr])[:3])
        color_buffer.append(tuple(color))

    # right col (top -> bottom)
    for row in range(vert):
        rh = width
        lh = rh - horiz_pixels
        top = vert_pixels * row
        bot = vert_pixels * (row + 1)

        color = np.uint8(cv2.mean(image[top:bot, lh:rh])[:3])
        color_buffer.append(tuple(color))

    # bottom row (right -> left)
    for col in range(horiz, -1, -1):
        bot = height
        top = bot - vert_pixels
        lh = horiz_pixels * col
        rh = horiz_pixels * (col + 1)

        color = np.uint8(cv2.mean(image[top:bot, lh:rh])[:3])
        color_buffer.append(tuple(color))

    return color_buffer


class quad:
    """Four dimensional polygon defined by 4 corners"""
    top_left = None
    top_right = None
    bottom_left = None
    bottom_right = None

    def get_corners(self):
        """Returns corners in top left, top right, bottom left, bottom right order"""
        return [self.top_left, self.top_right, self.bottom_left, self.bottom_right]
