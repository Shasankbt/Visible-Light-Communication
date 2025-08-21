import cv2
import numpy as np

# def classify_color(frame):
#     def trimmed_mean(channel, trim_ratio=0.75):
#         flat = channel.flatten()
#         sorted_vals = np.sort(flat)
#         k = int(len(sorted_vals) * trim_ratio)
#         trimmed = sorted_vals[k]
#         return trimmed.mean()

#     b, g, r = cv2.split(frame)
#     b = trimmed_mean(b)
#     g = trimmed_mean(g)
#     r = trimmed_mean(r)

#     if r < 100 and g < 100 and b < 100:
#         return "BLACK", (int(r), int(g), int(b))
    
#     if r > 150 and g > 150 and b > 150:
#         return "WHITE", (int(r), int(g), int(b))
    
#     max_color = max(r, g, b, 200)
#     if max_color == 0:
#         return "UNKNOWN", (0, 0, 0)

#     if g > 200 and r < 150 and b < 200: 
#         return "GREEN", (int(r), int(g), int(b))
#     elif b > 200 and r < 150 and g < 150:
#         return "BLUE", (int(r), int(g), int(b))
#     elif r > 200 and g < 150 and b < 150:
#         return "RED", (int(r), int(g), int(b))
#     else:
#         return "UNKNOWN", (int(r), int(g), int(b))


# def get_current_color(cap, bound_frame):
#     def crop_with_points(frame, pts):
#         pts = np.array(pts, dtype="float32")
#         w = int(np.linalg.norm(pts[0] - pts[1]))
#         h = int(np.linalg.norm(pts[0] - pts[3]))
#         dst_pts = np.array([[0,0], [w-1,0], [w-1,h-1], [0,h-1]], dtype="float32")
#         M = cv2.getPerspectiveTransform(pts, dst_pts)
#         cropped = cv2.warpPerspective(frame, M, (w, h))
#         return cropped
    
#     ret, frame = cap.read()
#     frame = crop_with_points(frame, bound_frame) if bound_frame is not None else frame

#     if not ret:
#         print("Failed to read frame from camera.")
#         return "UNKNOWN", (0, 0, 0)
    
#     small_frame = cv2.resize(frame, (100, 100))
#     color, rgb_vals = classify_color(small_frame)

#     # overlay_text = f"Color: {color} | RGB: {rgb_vals}"
#     # cv2.putText(frame, overlay_text, (30, 40),
#     #             cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
#     overlay_text = f"{rgb_vals}"

#     # dynamically place text near the bottom-left corner, with margin
#     h, w = frame.shape[:2]
#     margin_x, margin_y = 5, 10
#     text_x, text_y = margin_x, h - margin_y  

#     cv2.putText(frame, overlay_text, (text_x, text_y),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0, 255, 255), 1)
#     cv2.imshow("Frame", cv2.resize(frame, (500, 500)))

#     key = cv2.waitKey(1) & 0xFF

#     # print(f"Current color: {color}, RGB={rgb_vals}")
#     return color, rgb_vals


def get_bit(frame):   
    r, g, b = np.mean(frame, axis=(0, 1))
    if r > 175 and g > 175 and b > 175:
        return 1
    elif r < 125 and g < 125 and b < 125:
        return 0
    else:
        print(f"Unrecognized color: R={r}, G={g}, B={b}")
        return None
    
