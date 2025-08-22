import numpy as np
import argparse
import sys
from pathlib import Path

from encode import encode_message
from transmit import Transmitter

GRID_SIZE = 3

def read_bits_from_file(file_path):
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File '{file_path}' not found")
    
        with file_path.open('r') as f:
            return f.readlines()
        
    except Exception as e:
        raise ValueError(f"Error reading file: {e}")

def main():
    parser = argparse.ArgumentParser(description='Binary Message Transmitter')
    parser.add_argument('-f', '--file', help='Read binary message from file')
    args = parser.parse_args()
    
    transmitter = Transmitter(GRID_SIZE)

    try:
        if args.file:
            # File mode: read from file and transmit once
            print(f"Reading binary message from file: {args.file}")
            encoded_messages = read_bits_from_file(args.file)

            input("press any key to start transmission...")
            
            for encoded_message in encoded_messages:
                print("Encoded message:\n", encoded_message)
                transmitter.transmit_bits(encoded_message[:-1])

            input("Transmission complete. Press any key to exit.")
            
        else:
            # Interactive mode: original behavior
            while True:
                try:
                    message = input("Enter a binary message (0s and 1s) to encode: ")
                    bits = np.array([int(bit) for bit in message if bit in '01'])
                    if len(bits) == 0:
                        print("Error: No valid binary digits entered. Please enter only 0s and 1s.")
                        continue
                    
                    encoded_message = encode_message(bits)
                    
                    print("Encoded message:\n", encoded_message)
                    transmitter.transmit_bits(encoded_message.flatten().astype(str))
                    
                    print("Transmission complete. Press Ctrl+C to exit or enter another message.")
                    print("-" * 80)
                    
                except ValueError as e:
                    print(f"Error: {e}")
                    
    except KeyboardInterrupt:
        print("\nTransmission cancelled.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()