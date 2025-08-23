import cv2
import numpy as np
import time

def classify_color(frame):
    def trimmed_mean(channel, trim_ratio=0.5):
        flat = channel.ravel()
        k = int(len(flat) * trim_ratio)
        # partition puts kth element in place, lower values before it (unsorted)
        thresh = np.partition(flat, k)[k]
        return np.mean(flat[flat >= thresh])

    b, g, r = cv2.split(frame)
    b = trimmed_mean(b)
    g = trimmed_mean(g)
    r = trimmed_mean(r)

    if r < 130 and g < 130 and b < 130:
        return "BLACK", (int(r), int(g), int(b))
    
    if r > 140 and g > 140 and b > 140:
        return "WHITE", (int(r), int(g), int(b))
    
    max_color = max(r, g, b, 200)
    if max_color == 0:
        return "UNKNOWN", (0, 0, 0)

    if g > 170 and (g-r) > 80 and (g-b) > 50:
        return "GREEN", (int(r), int(g), int(b))
    elif b > 170 and (b-r) > 80 and (b-g) > 50:
        return "BLUE", (int(r), int(g), int(b))
    elif r > 170 and (r-g) > 50 and (r-b) > 50:
        return "RED", (int(r), int(g), int(b))
    else:
        return "UNKNOWN", (int(r), int(g), int(b))


def get_current_colors(frame, grid_length, grid_trim = 0.1):
    start_time = time.time()

    small_frame = cv2.resize(frame, (120, 120))
    h, w = small_frame.shape[:2]
    cell_h, cell_w = h // grid_length, w // grid_length
    dy = int(grid_trim * cell_h / 2)
    dx = int(grid_trim * cell_w / 2)

    colors = []
    rgbs = []

    for i in range(grid_length):
        for j in range(grid_length):
            cell = small_frame[i*cell_h + dy:(i+1)*cell_h - dy, j*cell_w + dx:(j+1)*cell_w - dx]
            color, rgb_vals = classify_color(cell)
            colors.append(color)
            rgbs.append(rgb_vals)

    # cv2.imshow("Frame", small_frame)
    key = cv2.waitKey(1) & 0xFF
    # print(rgbs)
    return colors, rgbs