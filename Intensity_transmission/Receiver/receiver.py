import cv2
import numpy as np
import sys
from decode import decode_message_str
from find_window import GetFrame
from color_classify import get_bit
import time


class Receiver:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            exit()
        print("Camera opened successfully.")

        pts = self._getBoundFrame()
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

    def _getBoundFrame(self):
        self.bound_frame = GetFrame(self.cap, "Frame")
        if self.bound_frame is None:
            print("No rectangle detected. Exiting.")
            return None
        
        print("Calibration done")
        print(f"Rectangle coordinates: {self.bound_frame}")
        return self.bound_frame

    def getFrame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to read frame from camera.")
            return None
        frame = cv2.warpPerspective(frame, self.M, (self.w, self.h))
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        return frame

    def sync_clock(self):
        print("Synchronizing clock...")
        last_state = 0   # start as black
        last_change_time = None
        durations = []

        while True:
            if get_bit(self.getFrame()) == 1:
                state = 1
            else:
                state = 0 

            # detect transition
            if state != last_state:
                now = time.time()
                if last_change_time is not None:
                    duration = now - last_change_time
                    durations.append(duration)
                    print(f"Pulse {last_state} lasted {duration:.3f} s")
                last_change_time = now
                last_state = state

            if len(durations) >= 3:
                time.sleep(np.mean(durations))
                return 0.5 # np.mean(durations)  # average of last 3 pulses
    
    

    def receive(self):
        time_interval = self.sync_clock()
        print(f"Time interval for synchronization: {time_interval:.3f} s")

        start = time.time()
        message = ""

        for n in range(36):
            target = start + (n + 0.5) * time_interval   # middle of each bit window
            while time.time() < target:
                pass

            print("reading bit at ", time.time())
            bit = get_bit(self.getFrame())
            message += str(bit)
            print(f"Received bit: {bit}")
           
        print("Final message:", message)
        time.sleep(time_interval)
        return message