# transmitter.py
import pygame
import time
import sys
import numpy as np
from encode import encode_message
import sys


GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0) 
GRID_LENGTH = 3 


def display_green_screen(grid_enabled=1):
    screen.fill(GREEN)
    if(grid_enabled):
        width, height = screen.get_size()
        quad_width = width // GRID_LENGTH
        quad_height = height // GRID_LENGTH
        # Draw vertical lines
        for i in range(1, GRID_LENGTH):
            x = i * quad_width
            pygame.draw.line(screen, BLACK, (x, 0), (x, height), 3)
        # Draw horizontal lines
        for i in range(1, GRID_LENGTH):
            y = i * quad_height
            pygame.draw.line(screen, BLACK, (0, y), (width, y), 3)

    pygame.display.flip()
    


def transmit_bits(bits, screen, grid_length=2): #grid shape is grid_length * grid_length
    DISPLAY_TIME = 0.5      # seconds for bit display
    SEPARATOR_TIME = 0.5    # seconds for blue
    grid_size = grid_length * grid_length
    # Divide bits into windows of 4
    n = len(bits)
    assert n % grid_size == 0, "Bits length must be divisible by grid_size"
    windows = [bits[i:i+grid_size] for i in range(0, n, grid_size)]

    # Quadrant positions and sizes
    width, height = screen.get_size()
    quad_width = width // grid_length
    quad_height = height // grid_length
    quad_rects = []
    for i in range(grid_size):
        row = i // grid_length
        col = i % grid_length
        rect = pygame.Rect(
            col * quad_width,
            row * quad_height,
            quad_width,
            quad_height
        )
        quad_rects.append(rect)

    # === Idle: show green and wait for Enter ===
    screen.fill(GREEN)
    pygame.display.flip()
    print("Press ENTER to start transmission, 'q' to quit.")

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                elif event.key == pygame.K_RETURN:
                    waiting = False

    # === Transmission starts ===
    print("Transmission started...")

    # Start transmission: Green screen (sync)
    screen.fill(GREEN)
    pygame.display.flip()
    time.sleep(DISPLAY_TIME)

    # Transmit each window of 4 bits
    for win_idx, window in enumerate(windows):
        # Draw each bit in its quadrant
        for i in range(grid_size):
            color = WHITE if window[i] == '1' else BLACK
            pygame.draw.rect(screen, color, quad_rects[i])
        pygame.display.flip()
        time.sleep(DISPLAY_TIME)

        # Separator (not after last window)
        if win_idx != len(windows) - 1:
            for rect in quad_rects:
                pygame.draw.rect(screen, BLUE, rect)
            pygame.display.flip()
            time.sleep(SEPARATOR_TIME)

    # End transmission: Red screen
    screen.fill(RED)
    pygame.display.flip()
    time.sleep(DISPLAY_TIME)

    print("Transmission finished.")


if __name__ == "__main__":
    pygame.init()
    # Set a fixed window size, e.g., 1200x900, instead of full screen
    screen = pygame.display.set_mode((1200, 900))
    

    while True:
        # Draw green background with grid
        display_green_screen(grid_enabled=1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # test_message_len = np.random.randint(1, 21)  # Random length between 1 and 20
        # test_message = np.random.randint(0, 2, test_message_len)  # Random binary message  
        test_message = input("Enter bits to transmit: (max length 20) ")
        test_message = np.array([int(bit) for bit in test_message.strip()], dtype=np.int8)
        print("Test message:\n", test_message)
        encoded_message = encode_message(test_message)
        encoded_message[3, 1] ^= 1  # Flip a bit to simulate
        encoded_message_str = ''.join(str(bit) for bit in encoded_message.flatten())
        print("Encoded message string:", encoded_message_str, "Length:", len(encoded_message_str))
        transmit_bits(encoded_message_str, screen, grid_length=GRID_LENGTH)
