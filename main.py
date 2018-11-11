import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    height, width, _ = frame.shape

    roi_height = int(height / 2)
    roi_width = int(width / 2)

    frames = []

    for x in range(2):
        for y in range(2):
            start_x = x * roi_height
            end_x = start_x + roi_height
            start_y = y * roi_width
            end_y = start_y + roi_width
            tmp_image = frame[start_x:end_x, start_y:end_y]
            frames.append(tmp_image)

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
        cv2.rectangle(f, (0, 0), (40, 40), color, -1)

        # Display the resulting frame
        frame_n = 'frame{}'.format(str(move))
        cv2.imshow(frame_n, f)
        cv2.moveWindow(frame_n, 0 if (move == 0 or move == 2) else 325, 0 if (move == 0 or move == 1) else 250)
        move += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
