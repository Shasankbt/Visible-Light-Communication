import numpy as np
import cv2
import sys

from receiver import Receiver
from decode import decode_message_str

def color_to_msg(color_sequence):
    msg = ""
    if not color_sequence:
        return "No colors received."
    
    def get_frame_bits(frame, prev_frame):
        bits = ""
        for i in range(len(frame)):
            for j in range(len(frame[i])):
                if frame[i][j] == "BLUE":
                    if prev_frame == None:
                        raise ValueError("Blue encountered without previous frame.")
                    frame[i][j] = prev_frame[i][j]
                if frame[i][j] == "WHITE":
                    bits += "1"
                elif frame[i][j] == "BLACK":
                    bits += "0"
        return bits

    msg += get_frame_bits(color_sequence[0], None)

    for i in range(1, len(color_sequence)):
        msg += get_frame_bits(color_sequence[i], color_sequence[i-1])


    print(f"Decoded message: {msg}")
    return msg


print(
    color_to_msg(
        [[['GREEN', 'GREEN', 'GREEN'], ['GREEN', 'GREEN', 'GREEN'], ['GREEN', 'GREEN', 'GREEN']], [['BLACK', 'BLACK', 'WHITE'], ['WHITE', 'BLACK', 'BLACK'], ['WHITE', 'WHITE', 'WHITE']], [['BLUE', 'BLUE', 'BLUE'], ['BLACK', 'BLUE', 'BLUE'], ['BLACK', 'BLACK', 'BLACK']], [['BLACK', 'BLACK', 'BLACK'], ['BLUE', 'BLACK', 'BLACK'], ['BLUE', 'BLUE', 'BLUE']], [['BLUE', 'BLUE', 'BLUE'], ['WHITE', 'WHITE', 'BLUE'], ['WHITE', 'BLACK', 'WHITE']], [['RED', 'RED', 'RED'], ['RED', 'RED', 'RED'], ['RED', 'RED', 'RED']]]
    )
)

# if __name__ == "__main__":
#     receiver = Receiver()
    
#     while True:        
#         color_sequence = receiver.receive()

#         if not color_sequence:
#             print("No valid color sequence received.")
#             sys.exit(1)

#         msg = color_to_msg(color_sequence)
        
#         try:
#             decoded_message = decode_message_str(msg)
#             print(f"Decoded message as array: {decoded_message}")
#             print("-" * 40)
#         except ValueError as e:
#             print(f"Error decoding message: {e}")
        
    