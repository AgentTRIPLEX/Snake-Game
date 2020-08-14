import os
import random
import pygame
import messagebox
import snake
import food

class Game():
    def __init__(self):
        pygame.init()

        self.HEIGHT = 700
        self.WIDTH = 700

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Snake')

        self.run = True
        self.clock = pygame.time.Clock()
        self.bg_color = (0,0,0)
        self.BOXES = self.get_boxes()

        self.reset_game()

        self.mainloop()

    def mainloop(self):
        while self.run:
            self.clock.tick(self.snake.speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            if not self.run:
                break

            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self.direction = snake.WEST
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.direction = snake.EAST
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.direction = snake.NORTH
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                self.direction = snake.SOUTH

            if self.current_direction != self.direction:
                self.last_direction = self.current_direction
                self.current_direction = self.direction

            self.window.fill(self.bg_color)

            self.snake.move(self.direction)
            self.snake.handle_food(self.food)
            self.snake.draw(self.window, snake.PIC, 'head.png')
            self.food.draw(self.window)

            if self.snake.check_head_collision():
                self.quit()

            pygame.display.update()

        pygame.quit()

    def get_boxes(self):
        boxes = []
        for y in range(20):
            for x in range(20):
                boxes.append([x*35, y*35])

        return boxes

    def quit(self):
        if not os.path.exists('high_score.cfg'):
            with open('high_score.cfg', 'wb') as w:
                w.write(b'0')

        corrupted = False
        with open('high_score.cfg', 'rb') as w:
            try:
                high_score = int(w.read().decode())
            except:
                corrupted = True

        if corrupted:
            with open('high_score.cfg', 'wb') as w:
                w.write(b'0')
            high_score = 0

        if high_score < self.snake.bodyLen:
            messagebox.showinfo('New High Score', f'Old High Score: {high_score}\nNew High Score/Current Score: {self.snake.bodyLen}')

            with open('high_score.cfg', 'wb') as w:
                w.write(str(self.snake.bodyLen).encode())

        else:
            messagebox.showinfo('Game Over', f'Current Score: {self.snake.bodyLen}\nHighest Score: {high_score}')

        self.reset_game()

    def reset_game(self):
        self.direction = snake.NORTH
        self.current_direction = snake.NORTH
        self.last_direction = None

        x, y = random.choice(self.BOXES)
        self.snake = snake.Snake(headX=x, headY=y, color=(0, 255, 0), height=35, width=35, screenheight=self.HEIGHT, screenwidth=self.WIDTH)
        self.food = food.Food((255, 255, 0), 35, 35, self.BOXES)
        self.food.generate((self.snake.headX, self.snake.headY), self.snake.bodyLen, self.snake.logs)

if __name__ == '__main__':
    Game()
