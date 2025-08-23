import cv2
import numpy as np
from datetime import datetime
import csv
import os

# ---- settings ----
PATCH = 11  # odd number; median is robust
FONT = cv2.FONT_HERSHEY_SIMPLEX

# ---- state ----
last_x, last_y = -1, -1
frozen = False
target_rgb = None  # set via keys: r,g,b,w,k
meas_rgb = (0, 0, 0)
meas_hsv = (0, 0, 0)

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def roi_median_bgr(frame, x, y, k=PATCH):
    h, w = frame.shape[:2]
    r_ = k // 2
    x0, x1 = clamp(x - r_, 0, w - 1), clamp(x + r_ + 1, 0, w)
    y0, y1 = clamp(y - r_, 0, h - 1), clamp(y + r_ + 1, 0, h)
    patch = frame[y0:y1, x0:x1]
    if patch.size == 0:
        return frame[y, x].astype(int)
    # median is more stable than mean for small noisy patches
    med = np.median(patch.reshape(-1, 3), axis=0)
    return med.astype(int)

def to_hsv_from_bgr(bgr):
    b, g, r = bgr
    hsv = cv2.cvtColor(np.uint8([[[b, g, r]]]), cv2.COLOR_BGR2HSV)[0][0]
    return tuple(int(v) for v in hsv)

def draw_hud(frame, pos_rgb, pos_hsv, cursor, target_rgb):
    h, w = frame.shape[:2]
    x, y = cursor
    # marker
    if x >= 0 and y >= 0:
        cv2.drawMarker(frame, (x, y), (0, 255, 255), cv2.MARKER_CROSS, 15, 2)

    # panel bg
    panel_w, panel_h = 470, 120 if target_rgb is None else 150
    cv2.rectangle(frame, (10, 10), (10 + panel_w, 10 + panel_h), (0, 0, 0), -1)
    cv2.rectangle(frame, (10, 10), (10 + panel_w, 10 + panel_h), (80, 80, 80), 1)

    # measured swatch
    mr, mg, mb = pos_rgb
    cv2.rectangle(frame, (20, 20), (120, 80), (mb, mg, mr), -1)
    cv2.rectangle(frame, (20, 20), (120, 80), (50, 50, 50), 1)

    # text
    y0 = 25
    cv2.putText(frame, f"XY: ({x},{y})", (140, y0), FONT, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, f"RGB: ({mr},{mg},{mb})", (140, y0 + 22), FONT, 0.6, (255, 255, 255), 2)
    h_, s_, v_ = pos_hsv
    cv2.putText(frame, f"HSV: ({h_},{s_},{v_})", (140, y0 + 44), FONT, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, f"PATCH: {PATCH}x{PATCH}  (LMB to freeze)", (140, y0 + 66), FONT, 0.55, (180, 180, 180), 1)

    # target block & delta
    if target_rgb is not None:
        tr, tg, tb = target_rgb
        cv2.rectangle(frame, (20, 90), (120, 140), (tb, tg, tr), -1)
        cv2.rectangle(frame, (20, 90), (120, 140), (50, 50, 50), 1)
        dr, dg, db = mr - tr, mg - tg, mb - tb
        l1 = abs(dr) + abs(dg) + abs(db)
        rms = int(np.sqrt((dr*dr + dg*dg + db*db)/3))
        cv2.putText(frame, f"TGT RGB: ({tr},{tg},{tb})", (140, y0 + 88), FONT, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"ΔRGB L1: {l1}   RMS: {rms}", (140, y0 + 110), FONT, 0.6, (255, 255, 255), 2)

def on_mouse(event, x, y, flags, param):
    global last_x, last_y, frozen
    if event == cv2.EVENT_LBUTTONDOWN:
        frozen = not frozen
    if not frozen and event == cv2.EVENT_MOUSEMOVE:
        last_x, last_y = x, y

def save_sample(meas_rgb, target_rgb, path="calibration_samples.csv"):
    header = ["timestamp", "meas_r", "meas_g", "meas_b", "tgt_r", "tgt_g", "tgt_b"]
    exists = os.path.exists(path)
    with open(path, "a", newline="") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(header)
        w.writerow([datetime.now().isoformat(timespec="seconds"),
                    *meas_rgb, *(target_rgb if target_rgb else ("", "", ""))])

def main():
    global meas_rgb, meas_hsv, target_rgb, last_x, last_y

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera")
        return

    # optional: lock some camera params
    # cap.set(cv2.CAP_PROP_AUTO_WB, 0)
    # cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    # cap.set(cv2.CAP_PROP_EXPOSURE, -6)

    cv2.namedWindow("Color Calibrator")
    cv2.setMouseCallback("Color Calibrator", on_mouse)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        if last_x < 0 or last_y < 0:
            last_x, last_y = w // 2, h // 2  # start at center

        # sample
        bgr = roi_median_bgr(frame, last_x, last_y, PATCH)
        b, g, r = map(int, bgr)
        meas_rgb = (r, g, b)
        meas_hsv = to_hsv_from_bgr((b, g, r))

        # overlay HUD
        draw_hud(frame, meas_rgb, meas_hsv, (last_x, last_y), target_rgb)

        # show
        cv2.imshow("Color Calibrator", frame)
        key = cv2.waitKey(1) & 0xFF

        # target shortcuts
        if key == ord('r'): target_rgb = (255, 0, 0)
        elif key == ord('g'): target_rgb = (0, 255, 0)
        elif key == ord('b'): target_rgb = (0, 0, 255)
        elif key == ord('w'): target_rgb = (255, 255, 255)
        elif key == ord('k'): target_rgb = (0, 0, 0)
        elif key == ord('c'): target_rgb = None  # clear
        elif key == ord('s'):  # save sample pair
            save_sample(meas_rgb, target_rgb)
            print("Saved sample to calibration_samples.csv")
        elif key == ord('q') or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()