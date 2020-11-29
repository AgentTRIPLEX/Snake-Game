import pygame
import random
from directions import *

class Food:
    def __init__(self, *args, **kwargs):
        self.grid = kwargs["grid"]
        self.color = kwargs["color"]
        x, y, self.width, self.height = random.choice(self.grid.grid)
        self.pos = x, y

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.pos + (self.width, self.height)))\

    def generate(self, snake):
        while 1:
            x, y, _, _ = random.choice(self.grid.grid)
            if (x, y) not in ([snake.head_pos] + snake.get_body_pos()):
                break

        self.pos = x, y