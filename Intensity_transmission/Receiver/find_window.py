import cv2
import numpy as np

def GetFrame(cap, frame_name):
    points = []

    def mouse_callback(event, x, y, flags, param):
        nonlocal points
        if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
            points.append((x, y))
            print(f"Point {len(points)}: ({x},{y})")

    cv2.namedWindow(frame_name)
    cv2.setMouseCallback(frame_name, mouse_callback)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # draw already selected points
        for i, (x, y) in enumerate(points):
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
            cv2.putText(frame, f"P{i+1}", (x+5, y-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        cv2.imshow(frame_name, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        if len(points) == 4:
            print("Selected 4 points:", points)
            break

    cv2.destroyWindow(frame_name)
    return np.array(points, dtype=np.int32) if len(points) == 4 else None