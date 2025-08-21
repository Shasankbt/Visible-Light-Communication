import numpy as np

HEADER_SIZE = 5
MAX_BODY_SIZE = 20
GRID_HT = 6
GRID_WT = 6


def check_and_correct(encoded: np.ndarray) -> np.ndarray:
    if encoded.shape != (GRID_HT, GRID_WT):
        raise ValueError("Encoded message has incorrect shape.")
    
    def get_parity_bit(bits: np.ndarray) -> int:
        return sum(bits) % 2

    row_parity = []
    col_parity = []
    for r in range(GRID_HT - 1):
        if get_parity_bit(encoded[r, :GRID_WT - 1]) != encoded[r, GRID_WT - 1]:
            row_parity.append(r)

        if get_parity_bit(encoded[:GRID_HT - 1, r]) != encoded[GRID_HT - 1, r]:
            col_parity.append(r)

    
    if len(row_parity) > 1 or len(col_parity) > 1:
        raise ValueError("More than one error detected, cannot correct.")
    
    if len(row_parity) == 1 and len(col_parity) == 1:
        encoded[row_parity[0], col_parity[0]] ^= 1

    return encoded

def decode_message(encoded: np.ndarray) -> np.ndarray:
    if encoded.shape != (GRID_HT, GRID_WT):
        raise ValueError("Encoded message has incorrect shape.")
    
    encoded = check_and_correct(encoded)

    header = encoded[0, :HEADER_SIZE]
    msg_len = sum(bit << (HEADER_SIZE - 1 - i) for i, bit in enumerate(header))

    if msg_len > MAX_BODY_SIZE:
        raise ValueError("Encoded message exceeds maximum body size.")

    message = np.zeros(msg_len, dtype=int)
    row, col = 0, HEADER_SIZE + 1

    for i in range(msg_len):
        if col >= GRID_WT - 1:
            row += 1
            col = 0
        if row >= GRID_HT - 1:
            raise ValueError("Encoded message too large for grid.")
        message[i] = encoded[row, col]
        col += 1

    return message

def decode_message_str(encoded_str: str) -> np.ndarray:
    encoded = np.array([int(bit) for bit in encoded_str.strip()], dtype=int).reshape((GRID_HT, GRID_WT))
    
    encoded = check_and_correct(encoded)

    header = encoded[0, :HEADER_SIZE]
    msg_len = sum(bit << (HEADER_SIZE - 1 - i) for i, bit in enumerate(header))

    if msg_len > MAX_BODY_SIZE:
        raise ValueError("Encoded message exceeds maximum body size.")

    message = np.zeros(msg_len, dtype=int)
    row, col = 0, HEADER_SIZE + 1

    for i in range(msg_len):
        if col >= GRID_WT - 1:
            row += 1
            col = 0
        if row >= GRID_HT - 1:
            raise ValueError("Encoded message too large for grid.")
        message[i] = encoded[row, col]
        col += 1

    return message

if __name__ == "__main__":
    print(decode_message_str("001001011000000000010000000000010001"))

