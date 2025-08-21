import numpy as np
import cv2
import sys

from receiver import Receiver

def color_to_msg(color_sequence):
    msg = ""
    if not color_sequence:
        return "No colors received."

    for batch in color_sequence:
        for color in batch:
            if color == "WHITE":
                msg += "1"
            elif color == "BLACK":
                msg += "0"

    print(f"Decoded message: {msg}")
    return msg

def get_msg_len(bits):
    if len(bits) != 8:
        raise ValueError("Bit string must be 8 bits long.")
    return int(bits, 2)

def decode_binary_to_text(binary_message):
    """Convert a binary message to a string."""
    chars = []
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) < 8:
            continue
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)

if __name__ == "__main__":
    receiver = Receiver()
    
    while True:        
        color_sequence = receiver.receive()

        if not color_sequence:
            print("No valid color sequence received.")
            sys.exit(1)

        msg = color_to_msg(color_sequence)
        print(f"Received color sequence: {msg}")
        txt_len = get_msg_len(msg[:8])
        print(decode_binary_to_text(msg[8: txt_len * 8 + 8]))
        
        # try:
        #     decoded_message = decode_message_str(msg)
        #     print(f"Decoded message as array: {decoded_message}")
        #     print("-" * 40)
        # except ValueError as e:
        #     print(f"Error decoding message: {e}")
        
    