import numpy as np

from encode import encode_message
from transmit import Transmitter

if __name__ == "__main__":
    transmitter = Transmitter()

    transmitter.calibrate()
    while True:
        input("Press Enter to calibrate when ready to transmit...")
        transmitter.clear_screen()
        break

    while True:
        try:
            message = input("Enter a binary message (0s and 1s) to encode: ")
            bits = np.array([int(bit) for bit in message if bit in '01'])
            encoded_message = encode_message(bits)
            
            print("Encoded message:\n", encoded_message)

            transmitter.transmit_bits(encoded_message.flatten().astype(str))

            print("Transmission complete. Press Ctrl+C to exit or enter another message.")
            print("-" * 80)
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nTransmission cancelled.")
            break