import numpy as np
import argparse
import sys
from pathlib import Path

from transmit import Transmitter

GRID_SIZE = 6

def text_encoder(string):
    """Convert a string to a binary message."""
    bits = np.array([int(bit) for bit in ''.join(format(ord(c), '08b') for c in string)])
    return bits

def num_to_binary(num):
    """Convert a number to a binary string."""
    return np.array([int(digit) for digit in format(num, '08b')])



if __name__ == "__main__":
    transmitter = Transmitter(GRID_SIZE)

    while True:
        try:
            message = input("Enter a text message to encode (1024): ")
            if not message:
                print("No message entered")
                continue
            
            if (len(message) > 1024):
                print("Message exceeds 1024 characters. Please enter a shorter message.")
                continue

            bits = np.hstack((num_to_binary(len(message)), text_encoder(message)))
            print(bits)
            if len(bits) == 0:
                print("Error: No valid binary digits entered. Please enter a valid text message.")
                continue
            
            
            print("Encoded message:\n", bits)
            transmitter.transmit_bits(bits.flatten().astype(str))
            
            print("Transmission complete. Press Ctrl+C to exit or enter another message.")
            print("-" * 80)

        except KeyboardInterrupt:
            print("\nExiting transmission.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")