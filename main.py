import cv2

import led_control
import utils
import video_capture

horiz_pixels = 16
vert_pixels = 8


def start():
    video = video_capture.VideoCapture()
    led_controller = led_control.LEDController(horiz_pixels, vert_pixels)

    while True:
        frame = video.get_next_frame()
        color_buffer = utils.average_pixels(frame, horiz_pixels, vert_pixels)
        led_controller.update_colors(color_buffer)

        cv2.imshow('res', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    start()



