import random
import pygame

class Food():
    def __init__(self, color, height, width, all_pos):
        self.height = height
        self.width = width
        self.color = color
        self.all_pos = all_pos
        self.pos = None

    def generate(self, snake_head, snake_len, snake_logs):
        bodyPos = [list(snake_logs[len(snake_logs) - f]) for f in range(1, snake_len)]

        while 1:
            r = random.choice(self.all_pos)
            if list(r) != list(snake_head) and list(r) not in bodyPos:
                break

        self.pos = list(r)

    def draw(self, window):
        if self.pos != None:
            x, y = self.pos
            pygame.draw.rect(window, self.color, (x, y, self.height, self.width))