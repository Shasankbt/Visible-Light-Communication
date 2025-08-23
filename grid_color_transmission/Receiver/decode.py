import numpy as np

HEADER_SIZE = 5
MAX_BODY_SIZE = 20
GRID_HT = 6
GRID_WT = 6


def check_and_correct(encoded: np.ndarray) -> tuple[np.ndarray]:
    if encoded.shape != (GRID_HT, GRID_WT):
        raise ValueError("Encoded message has incorrect shape.")
    
    def get_parity_bit(bits: np.ndarray) -> int:
        return sum(bits) % 2
    
    
    row_parity = []
    col_parity = []
    for r in range(GRID_HT):
        if get_parity_bit(encoded[r, :GRID_WT - 1]) != encoded[r, GRID_WT - 1]:
            row_parity.append(r)

        if get_parity_bit(encoded[:GRID_HT - 1, r]) != encoded[GRID_HT - 1, r]:
            col_parity.append(r)

            
    print(f"Row parity errors at: {row_parity}, Column parity errors at: {col_parity}")
    if len(row_parity) > 1 or len(col_parity) > 1:
        raise ValueError("More than one error detected, cannot correct.")
    
    if len(row_parity) == 1 and len(col_parity) == 1:
        encoded[row_parity[0], col_parity[0]] ^= 1
        print(f"Single-bit error detected and corrected at ({row_parity[0]}, {col_parity[0]})")
        print(f"index wrt message: {(row_parity[0] - 1) * (GRID_WT - 1) + col_parity[0]}")
        print(f"index wrt encoded: {row_parity[0] * GRID_WT + col_parity[0]}") 

    return encoded

def decode_message(encoded: np.ndarray) -> tuple[np.ndarray]:
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

def decode_message_str(encoded_str: str) -> tuple[np.ndarray]:
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

# if __name__ == "__main__":
#     print(check_and_correct(np.array([0,1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1]).reshape((6,6))))