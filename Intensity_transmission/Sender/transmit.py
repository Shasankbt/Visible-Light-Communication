# transmitter.py
import pygame
import time
import sys

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

DISPLAY_TIME = 0.075     # seconds for bit display
START_FLAG = '1010'

def msg_to_color(bits):
    colors = []

    for bit in START_FLAG:
        if bit == '1':
            colors.append(WHITE)
        elif bit == '0':
            colors.append(BLACK)

    for bit in bits:
        if bit == '1':
            colors.append(WHITE)
        elif bit == '0':
            colors.append(BLACK)
        else:
            raise ValueError("Bits must be '0' or '1'.")

    return colors

class Transmitter:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 900))
        self.width, self.height = self.screen.get_size()
        self.clear_screen()

    def __del__(self):
        pygame.quit()

    def calibrate(self):
        self.screen.fill(WHITE)
        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill(BLACK)
        pygame.display.flip()

    def transmit_bits(self, bits):
        color_sequence = msg_to_color(bits)

        for color in color_sequence:
            self.screen.fill(color)
            pygame.display.flip()
            time.sleep(DISPLAY_TIME)

        self.clear_screen()

