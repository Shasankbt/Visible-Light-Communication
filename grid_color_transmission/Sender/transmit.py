# transmitter.py
import pygame
import time
import sys
import numpy as np

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
UNKNOWN = (50, 50, 50)

DISPLAY_TIME = 1.0     # seconds for bit display


def msg_to_color(bits, grid_size):

    def pad(bits):
        total_bits = grid_size * grid_size
        if len(bits) % total_bits != 0:
            pad_len = total_bits - (len(bits) % total_bits)
            bits += "0" * pad_len
        return bits
    
    def bits_to_grid(bits, prev_batch):
        color_batch = []
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                color = (WHITE if bits[i][j] == 1 else BLACK)
                color = (BLUE if color == prev_batch[i][j] else color)
                color = (UNKNOWN if bits[i][j] == -1 else color)
                row.append(color)
            color_batch.append(row)
        return color_batch
    
    bits = pad(bits)
    bits = np.array([int(bit) for bit in bits])
    bits = bits.reshape(-1, grid_size, grid_size)

    color_sequence = []

    color_sequence.append([[GREEN] * grid_size for _ in range(grid_size)])

    for batch in bits:
        color_batch = bits_to_grid(batch, color_sequence[-1])
        color_sequence.append(color_batch)

    color_sequence.append([[RED] * grid_size for _ in range(grid_size)])

    # print(color_sequence)
    return color_sequence

class Transmitter:
    def __init__(self, grid_size=3):
        pygame.init()
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode(
            (info.current_w, info.current_h)
        )
        self.width, self.height = self.screen.get_size()
        self.cell_width = self.width // grid_size
        self.cell_height = self.height // grid_size
        self.grid_size = grid_size

        self.grid_rects = [[None for _ in range(grid_size)] for _ in range(grid_size)]

        for i in range(grid_size):
            for j in range(grid_size):
                rect = pygame.Rect(
                    j * self.cell_width,
                    i * self.cell_height,
                    self.cell_width,
                    self.cell_height
                )
                self.grid_rects[i][j] = rect
            
        self.clear_screen()

    def __del__(self):
        pygame.quit()

    def poll_events(self):
        polling = True
        while polling:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        print("Enter pressed, stopping polling.")
                        polling = False

            # keep screen responsive
            pygame.display.flip()


    def _fill_grid(self, color):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                pygame.draw.rect(self.screen, color[i][j], self.grid_rects[i][j])

        for i in range(1, self.grid_size):
            pygame.draw.line(self.screen, BLACK, (i * self.cell_width , 0), (i * self.cell_width, self.height), 3)
            pygame.draw.line(self.screen, BLACK, (0, i * self.cell_height), (self.width, i * self.cell_height), 3)  
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def clear_screen(self):
        self.screen.fill(GREEN) 

        # Draw vertical lines
        for i in range(1, self.grid_size):
            pygame.draw.line(self.screen, BLACK, (i * self.cell_width , 0), (i * self.cell_width, self.height), 3)
            pygame.draw.line(self.screen, BLACK, (0, i * self.cell_height), (self.width, i * self.cell_height), 3)         

        pygame.display.flip()
        time.sleep(DISPLAY_TIME)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def transmit_bits(self, bits):
        color_sequence = msg_to_color(bits, self.grid_size)

        for color in color_sequence:
            self._fill_grid(color)
            time.sleep(DISPLAY_TIME)

        self.clear_screen()

