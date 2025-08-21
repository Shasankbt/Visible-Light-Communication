import numpy as np
import cv2
import sys

from receiver import Receiver
from decode import decode_message_str

def color_to_msg(color_sequence):
    msg = ""
    if not color_sequence:
        return "No colors received."

    for color in color_sequence:
        if color == "WHITE":
            msg += "1"
        elif color == "BLACK":
            msg += "0"

    print(f"Decoded message: {msg}")
    return msg



if __name__ == "__main__":
    receiver = Receiver()

    while True:        
        color_sequence = receiver.receive()

        if not color_sequence:
            print("No valid color sequence received.")
            sys.exit(1)

        # msg = color_to_msg(color_sequence)
        
        try:
            decoded_message = decode_message_str(color_sequence)
            print(f"Decoded message as array: {decoded_message}")
        except ValueError as e:
            print(f"Error decoding message: {e}")
        
    