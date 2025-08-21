import cv2
import numpy as np
import sys
from decode import decode_message_str
from collections import Counter
from find_window import GetFrame

GRID_LENGTH = 3

# Open log file for writing
LOG_FILE = open("logs.txt", "w")

def log(msg):
    LOG_FILE.write(str(msg) + "\n")
    LOG_FILE.flush()




BOUND_FRAME = None






def readMessage(cap) -> list:
    message = [[] for _ in range(GRID_LENGTH * GRID_LENGTH)]
    readBit = [True] * (GRID_LENGTH * GRID_LENGTH)
    exit_loop = 0
    while True:
        colors, rgb_vals = get_current_color(cap)
        # print(f"Current color: {color}, RGB={rgb_vals}")
        for i,color in enumerate(colors):
            if color == "UNKNOWN":
                print(f"Unknown color detected at index {i}, skipping...")
                continue

            if color == "RED":
                exit_loop=1
                break

            if not readBit[i]:
                if color == "BLUE":
                    readBit[i] = True
                    print("<------------>")
                continue

            if color == "BLACK":
                message[i].append(0)
                readBit[i] = False
                print("Detected BLACK, appending 0")
            elif color == "WHITE":
                message[i].append(1)
                readBit[i] = False
                print("Detected WHITE, appending 1")

        if exit_loop:
            break

    # Combine message bits column-wise (first elements of all sublists, then second, etc.)
    combined_message = []
    for idx in range(len(message[0])):
        for bits in message:
                combined_message.append(bits[idx])
    message = combined_message
    print(f"message received: {message}, RGB={rgb_vals}")
    return message


def receive():
    cap = cv2.VideoCapture(0)
    print("Receiver started. Point camera at transmitter...")

    
    color = None
    while color != "GREEN":
        colors, rgbs = get_current_color(cap)
        color = colors[0]

        print("color:",color, "rgb:",rgbs[0])

    print("Start of frame")
    frame = readMessage(cap)
    print(f"Received frame: {frame}")

    cap.release()
    return frame


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()
    print("Camera opened successfully.")

    bound_frame = GetFrame(cap,"Frame")

    if bound_frame is None:
        print("No rectangle detected. Exiting.")
    else:
        print("Calibration done")
        print(f"Rectangle coordinates: {bound_frame}")
        BOUND_FRAME = bound_frame
        index=1
        while(True):
            received_message = receive()
            received_message = ''.join(str(bit) for bit in received_message)
            print(f"Received frame: {received_message}")
            decoded_message = decode_message_str(received_message)
            print(f"Decoded message {index}: {decoded_message}")
            index+=1

    LOG_FILE.close()




