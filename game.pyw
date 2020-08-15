import os
import random
import pygame
import messagebox
import snake
import food

class Game():
    def __init__(self):
        pygame.init()
        self.boxes_height = 35
        self.boxes_width = 35
        self.grid_height = 20
        self.grid_width = 20
        self.food_color = (0, 0, 255)
        self.snake_body_color = (0, 255, 0)
        self.snake_head_mode = snake.PIC
        self.snake_head_arg = 'head.png'

        self.BOXES = self.get_boxes(self.grid_height, self.grid_width)

        self.HEIGHT = self.grid_height * self.boxes_height
        self.WIDTH = self.grid_width * self.boxes_width

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Snake')

        self.run = True
        self.clock = pygame.time.Clock()
        self.bg_color = (0,0,0)

        if not os.path.exists('AI.txt'):
            with open('AI.txt', 'w') as w:
                w.write('False')
            self.AI = False

        else:
            with open('AI.txt', 'r') as w:
                AI = w.read()

            if AI.lower().strip() in ['false', 'true']:
                self.AI = {'false':False, 'true':True}[AI.lower().strip()]
            else:
                with open('AI.txt', 'w') as w:
                    w.write('False')

                self.AI = False

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

            if not self.AI:
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    self.direction = snake.WEST
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    self.direction = snake.EAST
                if pygame.key.get_pressed()[pygame.K_UP]:
                    self.direction = snake.NORTH
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    self.direction = snake.SOUTH

            else:
                if self.snake.headY == self.food.pos[1]:
                    if not self.snake.collision_upon_move(snake.WEST):
                        self.direction = snake.WEST
                    else:
                        if not self.snake.collision_upon_move(snake.NORTH):
                            self.direction = snake.NORTH
                        elif not self.snake.collision_upon_move(snake.SOUTH):
                            self.direction = snake.SOUTH
                        elif not self.snake.collision_upon_move(snake.EAST):
                            self.direction = snake.EAST
                        elif not self.snake.collision_upon_move(snake.WEST):
                            self.direction = snake.WEST

                else:
                    if not self.snake.collision_upon_move(snake.NORTH):
                        self.direction = snake.NORTH
                    else:
                        if not self.snake.collision_upon_move(snake.WEST):
                            self.direction = snake.WEST
                        else:
                            if not self.snake.collision_upon_move(snake.EAST):
                                self.direction = snake.EAST
                            elif not self.snake.collision_upon_move(snake.WEST):
                                self.direction = snake.WEST
                            elif not self.snake.collision_upon_move(snake.SOUTH):
                                self.direction = snake.SOUTH
                            elif not self.snake.collision_upon_move(snake.NORTH):
                                self.direction = snake.NORTH

            self.window.fill(self.bg_color)

            self.snake.move(self.direction)
            self.snake.handle_food(self.food)
            self.snake.draw(self.window, self.snake_head_mode, self.snake_head_arg)
            self.food.draw(self.window)

            if self.snake.check_head_collision():
                self.quit()

            pygame.display.update()

        pygame.quit()

    def get_boxes(self, h, w):
        boxes = []
        for y in range(h):
            for x in range(w):
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

        print(self.direction)

        if high_score < self.snake.bodyLen:
            messagebox.showinfo('New High Score', f'Old High Score: {high_score}\nNew High Score/Current Score: {self.snake.bodyLen}')

            if not self.AI:
                with open('high_score.cfg', 'wb') as w:
                    w.write(str(self.snake.bodyLen).encode())

        else:
            messagebox.showinfo('Game Over', f'Current Score: {self.snake.bodyLen}\nHighest Score: {high_score}')

        self.reset_game()

    def reset_game(self):
        self.direction = snake.NORTH

        x, y = random.choice(self.BOXES)
        self.snake = snake.Snake(headX=x, headY=y, color=self.snake_body_color, height=self.boxes_height, width=self.boxes_width, screenheight=self.HEIGHT, screenwidth=self.WIDTH)
        self.food = food.Food(self.food_color, self.boxes_height, self.boxes_width, self.BOXES)
        self.food.generate((self.snake.headX, self.snake.headY), self.snake.bodyLen, self.snake.logs)

if __name__ == '__main__':
    Game()