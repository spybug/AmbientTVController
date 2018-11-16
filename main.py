import numpy as np
import cv2

import utils

cap = cv2.VideoCapture(0)

top_offset = 200
top_left_corner = (top_offset, 25)
top_right_corner = (640 - top_offset, 25)
bottom_left_corner = (25, 480 - 25)
bottom_right_corner = (640 - 25, 480 - 25)

quad = utils.quad()
quad.top_left = top_left_corner
quad.top_right = top_right_corner
quad.bottom_left = bottom_left_corner
quad.bottom_right = bottom_right_corner

middle_top = utils.average_point(top_left_corner, top_right_corner)
middle_bottom = utils.average_point(bottom_left_corner, bottom_right_corner)
middle = utils.average_point(middle_top, middle_bottom)
middle_left = utils.average_point(top_left_corner, bottom_left_corner)
middle_right = utils.average_point(top_right_corner, bottom_right_corner)

roi_top_left = utils.create_roi([top_left_corner, middle_top, middle, middle_left])
roi_top_right = utils.create_roi([middle_top, top_right_corner, middle_right, middle])
roi_bottom_left = utils.create_roi([middle_left, middle, middle_bottom, bottom_left_corner])
roi_bottom_right = utils.create_roi([middle, middle_right, bottom_right_corner, middle_bottom])

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    height, width, _ = frame.shape

    roi_height = int(height / 2)
    roi_width = int(width / 2)

    frames = []

    transformed_frame = utils.transform_image(frame, quad)
    cv2.imshow('transformed', transformed_frame)
    cv2.circle(frame, top_left_corner, 3, (0, 255, 0), thickness=-1)
    cv2.circle(frame, top_right_corner, 3, (0, 255, 0), thickness=-1)
    cv2.circle(frame, bottom_left_corner, 3, (0, 255, 0), thickness=-1)
    cv2.circle(frame, bottom_right_corner, 3, (0, 255, 0), thickness=-1)
    cv2.line(frame, top_left_corner, top_right_corner, (0, 255, 0), thickness=1)
    cv2.line(frame, top_right_corner, bottom_right_corner, (0, 255, 0), thickness=1)
    cv2.line(frame, bottom_right_corner, bottom_left_corner, (0, 255, 0), thickness=1)
    cv2.line(frame, bottom_left_corner, top_left_corner, (0, 255, 0), thickness=1)
    cv2.imshow('original', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    else:
        continue

    for x in range(2):
        for y in range(2):
            start_x = x * roi_height
            end_x = start_x + roi_height
            start_y = y * roi_width
            end_y = start_y + roi_width
            tmp_image = frame[start_x:end_x, start_y:end_y]
            frames.append(tmp_image)

    mask_top_left = np.zeros(frame.shape, dtype=np.uint8)
    mask_top_right = np.zeros(frame.shape, dtype=np.uint8)
    mask_bottom_left = np.zeros(frame.shape, dtype=np.uint8)
    mask_bottom_right = np.zeros(frame.shape, dtype=np.uint8)

    move = 0
    for f in frames:
        arr = np.float32(f)
        pixels = arr.reshape((-1, 3))
        n_colors = 1
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS
        _, labels, centroids = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        palette = np.uint8(centroids)
        quantized = palette[labels.flatten()]
        quantized = quantized.reshape(f.shape)

        count = np.unique(labels, return_counts=True)
        dominant_color = palette[np.argmax(np.unique(labels, return_counts=True)[1])]

        # Our operations on the frame come here

        color = tuple(map(int, dominant_color))
        #cv2.rectangle(f, (0, 0), (40, 40), color, -1)

        # Display the resulting frame
        frame_n = 'frame{}'.format(str(move))
        #cv2.imshow(frame_n, f)
        #cv2.moveWindow(frame_n, 0 if (move == 0 or move == 2) else 325, 0 if (move == 0 or move == 1) else 250)
        move += 1

    cv2.circle(frame, top_left_corner, 3, (0, 0, 255), thickness=-1)
    cv2.circle(frame, top_right_corner, 3, (0, 0, 255), thickness=-1)
    cv2.circle(frame, bottom_left_corner, 3, (0, 0, 255), thickness=-1)
    cv2.circle(frame, bottom_right_corner, 3, (0, 0, 255), thickness=-1)
    cv2.circle(frame, middle_top, 4, (0, 255, 0), thickness=-1)
    cv2.circle(frame, middle_bottom, 4, (0, 255, 0), thickness=-1)

    channel_count = frame.shape[2]  # i.e. 3 or 4 depending on your image
    ignore_mask_color = (255,) * channel_count
    cv2.fillPoly(mask_top_left, roi_top_left, ignore_mask_color)
    cv2.fillPoly(mask_top_right, roi_top_right, ignore_mask_color)
    cv2.fillPoly(mask_bottom_left, roi_bottom_left, ignore_mask_color)
    cv2.fillPoly(mask_bottom_right, roi_bottom_right, ignore_mask_color)

    top_right_list = np.array([0, 255], dtype=np.float32)
    top_left_list = np.array([0, 255], dtype=np.float32)
    bottom_right_list = np.array([0, 255], dtype=np.float32)
    bottom_left_list = np.array([0, 255], dtype=np.float32)

    for row_i in range(frame.shape[0]):
        for col_i in range(frame.shape[1]):
            cur_pixel = np.float32(frame[row_i][col_i])
            top_right = mask_top_right[row_i][col_i][0]
            top_left = mask_top_left[row_i][col_i][0]
            bottom_right = mask_bottom_right[row_i][col_i][0]
            bottom_left = mask_bottom_left[row_i][col_i][0]
            if top_right != 0:
                np.append(top_right_list, np.float32(frame[row_i][col_i]))
                continue
            elif top_left != 0:
                np.append(top_left_list, np.float32(frame[row_i][col_i]))
                continue
            elif bottom_right != 0:
                np.append(bottom_right_list, np.float32(frame[row_i][col_i]))
                continue
            elif bottom_left != 0:
                np.append(bottom_left_list, np.float32(frame[row_i][col_i]))
                continue

    # masked_top_right = cv2.bitwise_and(frame, mask_top_right)
    # masked_top_left = cv2.bitwise_and(frame, mask_top_left)
    masked_bottom_right = cv2.bitwise_and(frame, mask_bottom_right)
    # masked_bottom_left = cv2.bitwise_and(frame, mask_bottom_left)

    cv2.imshow('frame', masked_bottom_right)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


