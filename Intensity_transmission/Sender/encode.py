import numpy as np

HEADER_SIZE = 5
MAX_BODY_SIZE = 20
GRID_HT = 6
GRID_WT = 6

def encode_message(message: np.ndarray) -> np.ndarray:
    msg_len = len(message)

    if msg_len > MAX_BODY_SIZE:
        raise ValueError(f"Message exceeds maximum body size of {MAX_BODY_SIZE} bits.")
    
    def get_parity_bit(bits: np.ndarray) -> int:
        return sum(bits) % 2
    
    encoded = np.zeros((GRID_HT, GRID_WT), dtype=int)

    header = [(msg_len >> i) & 1 for i in reversed(range(HEADER_SIZE))]

    encoded[0, 0:HEADER_SIZE] = header

    row, col = 0, HEADER_SIZE + 1
    for bit in message:
        if col >= GRID_WT - 1:
            row += 1
            col = 0
        if row >= GRID_HT - 1:
            raise ValueError("Message too large for grid.")
        encoded[row, col] = bit
        col += 1

    for r in range(GRID_HT - 1):
        encoded[r, GRID_WT - 1] = get_parity_bit(encoded[r, :GRID_WT - 1])
        encoded[GRID_HT - 1, r] = get_parity_bit(encoded[:GRID_HT - 1, r])

    encoded[GRID_HT - 1, GRID_WT - 1] = get_parity_bit(encoded[GRID_HT - 1, :GRID_WT - 1])


    return encoded