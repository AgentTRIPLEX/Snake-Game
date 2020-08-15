import pygame

NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
PIC = 'pic'
COLOR = 'color'

class Snake():
    def __init__(self, **kwargs):
        self.headX = kwargs['headX']
        self.headY = kwargs['headY']
        self.height = kwargs['height']
        self.width = kwargs['width']
        self.color = kwargs['color']
        self.screenheight = kwargs['screenheight']
        self.screenwidth = kwargs['screenwidth']
        self.bodyLen = 2
        self.speed = 5
        self.logs = []

        self.move(NORTH)

    def draw(self, window, mode, arg):
        if mode == COLOR:
            pygame.draw.rect(window, arg, (self.headX, self.headY, self.width, self.height))
        elif mode == PIC:
            window.blit(pygame.image.load(arg), (self.headX, self.headY))

        for f in range(1, self.bodyLen):
            x, y = self.logs[len(self.logs) - f]
            pygame.draw.rect(window, self.color, (x, y, self.width, self.height))

    def move(self, direction):
        self.logs.append([self.headX, self.headY])

        if direction == NORTH:
            self.headY -= self.height
        elif direction == SOUTH:
            self.headY += self.height
        elif direction == EAST:
            self.headX += self.width
        elif direction == WEST:
            self.headX -= self.width

        if self.headY < 0:
            self.headY = self.screenheight - self.height
        if self.headY > (self.screenheight - self.height):
            self.headY = 0
        if self.headX < 0:
            self.headX = self.screenwidth - self.width
        if self.headX > (self.screenwidth - self.width):
            self.headX = 0

    def handle_food(self, food):
        if food.pos != None:
            if food.pos == [self.headX, self.headY]:
                self.speed += 1
                self.bodyLen += 1
                food.generate((self.headX, self.headY), self.bodyLen, self.logs)
                return True

        return False

    def check_head_collision(self):
        return [self.headX, self.headY] in [list(self.logs[len(self.logs) - f]) for f in range(1, self.bodyLen)]

    def pos_upon_move(self, direction):
        headX = self.headX
        headY = self.headY

        if direction == NORTH:
            headY -= self.height
        elif direction == SOUTH:
            headY += self.height
        elif direction == EAST:
            headX += self.width
        elif direction == WEST:
            headX -= self.width

        if headY < 0:
            headY = self.screenheight - self.height
        if headY > (self.screenheight - self.height):
            headY = 0
        if headX < 0:
            headX = self.screenwidth - self.width
        if headX > (self.screenwidth - self.width):
            headX = 0

        return headX, headY

    def collision_upon_move(self, direction):
        headX, headY = self.pos_upon_move(direction)
        return [headX, headY] in [list(self.logs[len(self.logs) - f]) for f in range(1, self.bodyLen)]