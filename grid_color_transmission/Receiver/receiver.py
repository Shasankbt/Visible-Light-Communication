import cv2
import numpy as np
import sys
from decode import decode_message_str
from find_window import GetFrame
from color_classify import get_current_colors
import time

GRID_LENGTH = 3
DISPLAY_TIME = 0.25

class Receiver:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        # self.cap.set(cv2.CAP_PROP_EXPOSURE, -10)

        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            exit()
        print("Camera opened successfully.")
        
        pts = GetFrame(self.cap, "Frame")
        if pts is None:
            print("No rectangle detected. Exiting.")
            exit()
        
        print("rectangle coordinates:", pts)
        self.w = int(np.linalg.norm(pts[0] - pts[1]))
        self.h = int(np.linalg.norm(pts[0] - pts[3]))
        pts = np.array(pts, dtype=np.float32)      # ensure float32
        dst_pts = np.array([
            [0, 0],
            [self.w - 1, 0],
            [self.w - 1, self.h - 1],
            [0, self.h - 1]
        ], dtype=np.float32)

        self.M = cv2.getPerspectiveTransform(pts, dst_pts)

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()

    def getFrame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to read frame from camera.")
            return None
        frame = cv2.warpPerspective(frame, self.M, (self.w, self.h))
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        return frame
    
    def _contains_unknown_color(self, colors, rgb):
        if (
            "UNKNOWN" in colors or
            ("GREEN" in colors and not self.is_color(colors, "GREEN")) or
            ("RED" in colors and not self.is_color(colors, "RED"))
        ):
            print("Unknown color detected, waiting for valid sequence...")
            print(f"RGB values: {rgb}")
            return True
        
        return False
    
    def is_color(self, colors, target_color):
        return np.all(np.array(colors) == target_color)

    def receive(self):
        color = None
        print("Waiting for GREEN to start...")

        while color is None or not self.is_color(color, "GREEN"):
            color, rgb = get_current_colors(self.getFrame(), GRID_LENGTH)
            print(color)
            print(rgb)
            if color is None:
                continue

        print("Detected GREEN, ready for color sequence")

        while (
            color is None or
            self._contains_unknown_color(color, rgb) or
            self.is_color(color, "GREEN")
        ):  
            # print(color)
            start = time.time()
            color, rgb = get_current_colors(self.getFrame(), GRID_LENGTH)

        print("Start of frame: ------")
        
        
        color_sequence = []
        print(f"Grid-0: {color} at {start}")
        color_sequence.append(color)

          # Start time for the
        batch_num = 1
        while True:
            while time.time() - start < DISPLAY_TIME * (batch_num + 0.25):
                pass

            color, rgb = get_current_colors(self.getFrame(), GRID_LENGTH)
            # print(color)
            if self.is_color(color, "RED"):
                print("Detected RED, stopping the sequence")
                break

            if (
                self._contains_unknown_color(color, rgb) or
                self.is_color(color, "GREEN") or
                color == color_sequence[-1]
            ):
                print("Debug Value: ", color, rgb)
                continue

            print(f"Grid-{batch_num}: {color} at {time.time()}")
            color_sequence.append(color)
            batch_num += 1

        print("ended reading frame, time taken:", time.time() - start)
        return color_sequence