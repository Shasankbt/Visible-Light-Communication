import numpy as np
import argparse
import json

from encode import encode_message
from transmit import Transmitter

GRID_SIZE = 3

def Send(transmitter, message, errorwhere, error_pos):
    def add_error(encoded, errorwhere, error_pos, encoded_size=6):
        msg_len = len(encoded)
        if errorwhere==0:
            if error_pos<=msg_len-1 and error_pos>=0:
                encoded[error_pos//(encoded_size-1)+1, error_pos%(encoded_size-1)] ^= 1
        else:
            encoded[error_pos//(encoded_size), error_pos%(encoded_size)] ^= 1

        return encoded
    
    
    bits = np.array([int(bit) for bit in message if bit in '01'])
    if len(bits) == 0:
        print("Error: No valid binary digits entered. Please enter only 0s and 1s.")
        return
    
    encoded_message = encode_message(bits)
    print("Encoded message:\n", encoded_message)

    encoded_message = add_error(encoded_message, int(errorwhere), int(error_pos))
    print("Error included message:\n", encoded_message)

    transmitter.transmit_bits(encoded_message.flatten().astype(str))
    
    print("Transmission complete. Press Ctrl+C to exit or enter another message.")
    print("-" * 80)

def read_from_file(transmitter, file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            for entry in data:
                bits = entry["bits"]
                errorwhere = entry["errorwhere"]
                error_pos = entry["errorpos"]

                transmitter.poll_events()

                Send(transmitter, bits, errorwhere, error_pos)

            transmitter.poll_events()
    except ValueError as e:
        print(f"Error: {e}")
    
def read_from_terminal(transmitter):
    try:
        message = input("Enter a binary message (0s and 1s) to encode: ")
        errorwhere = input("Enter 0 for injecting error in original message or 1 for injecting error in medium: ")
        error_pos = input("Enter the bit position to inject error (0-indexed): ")

        Send(transmitter, message, errorwhere, error_pos)
        
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Binary Message Transmitter')
    parser.add_argument('-f', '--file', help='Read binary message from file')
    args = parser.parse_args()
    
    transmitter = Transmitter(GRID_SIZE)

    if args.file:
        read_from_file(transmitter, args.file)
    else:
        while True:
            read_from_terminal(transmitter)