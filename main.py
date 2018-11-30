import cv2
import threading
import time

import led_control
import utils
import video_capture
from flask import *

horiz_pixels = 16
vert_pixels = 8

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

frame = None
video = None
running = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setup')
def setup():
    if frame is not None:
        frame_copy = frame.copy()
        corners = video.get_corners()

        for corner in corners:
            cv2.circle(frame_copy, corner, 6, (0, 255, 0), thickness=-1)

        cv2.line(frame_copy, corners[0], corners[1], (0, 255, 0), thickness=2)
        cv2.line(frame_copy, corners[0], corners[2], (0, 255, 0), thickness=2)
        cv2.line(frame_copy, corners[2], corners[3], (0, 255, 0), thickness=2)
        cv2.line(frame_copy, corners[1], corners[3], (0, 255, 0), thickness=2)

        cv2.imwrite('static/last_frame.jpg', frame_copy)

    return render_template('setup.html')


@app.route('/setup/update_point', methods=['POST'])
def update_point():
    global video
    change_amount = 10

    data = request.form
    point = int(data['point'])
    direction = data['direction'].upper()
    corners = video.get_corners()

    if direction == 'LEFT':
        corners[point] = (corners[point][0] - change_amount, corners[point][1])
        if corners[point][0] < 0:
            corners[point] = (0, corners[point][1])

    elif direction == 'RIGHT':
        corners[point] = (corners[point][0] + change_amount, corners[point][1])
        if corners[point][0] > video.width:
            corners[point] = (video.width - 1, corners[point][1])

    elif direction == 'UP':
        corners[point] = (corners[point][0], corners[point][1] - change_amount)
        if corners[point][1] < 0:
            corners[point] = (corners[point][0], 0)
    else:
        # down
        corners[point] = (corners[point][0], corners[point][1] + change_amount)
        if corners[point][1] > video.height:
            corners[point][1] = (corners[point][0], video.height - 1)

    video.set_corners(corners)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/setup/save_settings', methods=['POST'])
def save_settings():
    video.save_settings()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response


def main():
    global frame, video, running

    led_controller = led_control.LEDController(horiz_pixels, vert_pixels)

    while True:
        if running:
            if video is None:
                video = video_capture.VideoCapture()

            frame = video.get_next_frame()
            transformed_frame = video.transform_image(frame)
            color_buffer = utils.average_pixels(transformed_frame, horiz_pixels, vert_pixels)
            led_controller.update_colors(color_buffer)
            cv2.imshow('res', transformed_frame)

        else:
            if video is not None:
                video.stop()
                led_controller.stop()
                video = None

            time.sleep(5)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False


@app.route('/stop')
def stop():
    global running
    running = False
    return "<p>Stopped</p>"


@app.route('/start')
def start():
    global running
    running = True
    return "<p>Started</p>"


if __name__ == '__main__':
    t = threading.Thread(target=main)
    t.start()
    app.run(host='0.0.0.0', port=5000)




