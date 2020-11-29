import pygame
import random
from directions import *
import graphics

class Snake:
    def __init__(self, *args, **kwargs):
        self.grid = kwargs["grid"]
        self.head_arg = kwargs["head_arg"]
        self.head_type = kwargs["head_type"]
        self.body_color = kwargs["body_color"]
        self.speed = kwargs["speed"]

        if "body_len" not in kwargs:
            self.body_len = 0
        else:
            self.body_len = kwargs["body_len"]

        if "difference" in kwargs:
            self.difference = kwargs["difference"]
        else:
            self.difference = 0

        self.logs = []
        self.direction = random.choice([NORTH, SOUTH, EAST, WEST])

        while 1:
            x, y, self.width, self.height = random.choice(self.grid.grid)
            self.head_pos = x, y

            for _ in range(self.body_len):
                self.move()

            if not self.check_collision(True):
                break

    def draw(self, win):
        w = self.width
        h = self.height
        d = self.direction

        if d in [NORTH, SOUTH]:
            w += self.difference
        elif d in [EAST, WEST]:
            h += self.difference

        w, h = self.width, self.height

        if self.head_type == graphics.COLOR:
            pygame.draw.rect(win, self.head_arg, (self.head_pos + (w, h)))
        else:
            win.blit(pygame.transform.scale(self.head_arg, (w, h)), self.head_pos)

        body_pos = self.get_body_pos(True)
        for i, ((x, y), d) in enumerate(body_pos):
            w = self.width
            h = self.height

            if d in [NORTH, SOUTH]:
                w += self.difference
            elif d in [EAST, WEST]:
                h += self.difference

            if (i + 1) != len(body_pos) and False:
                d2 = body_pos[i + 1][1]
                if d != d2 and d != {NORTH:SOUTH, EAST:WEST, WEST:EAST, SOUTH:NORTH}[d2]:
                    diff = self.difference

                    if str(diff).startswith("-"):
                        diff = -diff

                    diff = diff // 2

                    if d2 == NORTH:
                        y -= diff
                        h += diff
                    elif d2 == SOUTH:
                        y += diff
                        h -= diff
                    elif d2 == EAST:
                        x += diff
                        w -= diff
                    elif d2 == WEST:
                        x -= diff
                        w += diff


            w, h = self.width, self.height

            pygame.draw.rect(win, self.body_color, (x, y, w, h))

    def get_body_pos(self, direction=False):
        if direction:
            return [self.logs[len(self.logs) - f - 1] for f in range(self.body_len)]
        else:
            return [self.logs[len(self.logs) - f - 1][0] for f in range(self.body_len)]

    def check_collision(self, walls=False):
        x, y = self.head_pos

        if self.head_pos in self.get_body_pos():
            return True

        if walls \
                and (((x + self.width) > self.grid.width) or \
                     ((y + self.height) > self.grid.height) or \
                     (x < 0) or (y < 0)):
            return True

        return False

    def check_collision_upon_move(self, direction, walls=False):
        x, y = self.pos_upon_move(direction)
        head_pos = x, y
        logs = self.logs[:]
        logs.append(head_pos)
        body_pos = [logs[len(logs) - f - 1][0] for f in range(self.body_len)]

        if head_pos in body_pos:
            return True

        if walls \
                and (((x + self.width) > self.grid.width) or \
                     ((y + self.height) > self.grid.height) or \
                     (x < 0) or (y < 0)):
            return True

        return False

    def move(self, collision=False):
        x, y = self.pos_upon_move(self.direction)

        if not collision:
            if (x + self.width) > self.grid.width:
                x = 0

            if (y + self.height) > self.grid.height:
                y = 0

            if x < 0:
                x = self.grid.width - self.width

            if y < 0:
                y = self.grid.height - self.height

        self.logs.append([self.head_pos, self.direction])
        self.head_pos = x, y

    def pos_upon_move(self, direction):
        x, y = self.head_pos

        if direction == NORTH:
            return x, (y - self.height)

        elif direction == SOUTH:
            return x, (y + self.height)

        elif direction == WEST:
            return (x - self.width), y

        elif direction == EAST:
            return (x + self.width), y
