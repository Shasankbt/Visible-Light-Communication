import cv2
import numpy as np
import time

def classify_color(frame):
    def trimmed_mean(channel, trim_ratio=0.9):
        flat = channel.ravel()
        k = int(len(flat) * trim_ratio)
        # partition puts kth element in place, lower values before it (unsorted)
        thresh = np.partition(flat, k)[k]
        return np.mean(flat[flat >= thresh])

    b, g, r = cv2.split(frame)
    b = trimmed_mean(b)
    g = trimmed_mean(g)
    r = trimmed_mean(r)

    if r < 100 and g < 100 and b < 100:
        return "BLACK", (int(r), int(g), int(b))
    
    if r > 150 and g > 150 and b > 150:
        return "WHITE", (int(r), int(g), int(b))
    
    max_color = max(r, g, b, 200)
    if max_color == 0:
        return "UNKNOWN", (0, 0, 0)

    if g > 200 and r < 150 and b < 150:
        return "GREEN", (int(r), int(g), int(b))
    elif b > 200 and r < 150 and g < 150:
        return "BLUE", (int(r), int(g), int(b))
    elif r > 200 and g < 150 and b < 150:
        return "RED", (int(r), int(g), int(b))
    else:
        return "UNKNOWN", (int(r), int(g), int(b))


def get_current_colors(frame, grid_length):
    start_time = time.time()

    small_frame = cv2.resize(frame, (120, 120))
    h, w = small_frame.shape[:2]
    cell_h, cell_w = h // grid_length, w // grid_length

    colors = []
    rgbs = []

    for i in range(grid_length):
        for j in range(grid_length):
            cell = small_frame[i*cell_h:(i+1)*cell_h, j*cell_w:(j+1)*cell_w]
            color, rgb_vals = classify_color(cell)
            colors.append(color)
            rgbs.append(rgb_vals)

    # cv2.imshow("Frame", small_frame)
    key = cv2.waitKey(1) & 0xFF
    return colors, rgbs