import os
import random
import pygame
import threading

import messagebox
from directions import *
import settings
import grid
import snake
import food
import AI

pygame.init()

class Game:
    def __init__(self):
        self.grid = grid.Grid(settings.cols, settings.rows, settings.cell_width, settings.cell_height, True)

        self.WIDTH = self.grid.width
        self.HEIGHT = self.grid.height
        
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Snake Game")

        self.clock = pygame.time.Clock()
        self.bg_color = settings.bg_color

        self.reset_game()
        
    def reset_game(self):
        settings.hardcore = messagebox.askyesno("Hardcore?", "Would You Like To Play In Hardcore Mode?\nNote: In Hardcore Mode, touching a wall makes you lose!")
        settings.AI = messagebox.askyesno("AI?", "Would You Like To Use The AI?")

        self.snake = snake.Snake(grid=self.grid,
                                 head_type=settings.snake_head_type,
                                 head_arg=settings.snake_head_arg,
                                 body_color=settings.snake_body_color,
                                 body_len=settings.snake_start_body_len,
                                 speed=settings.snake_start_speed,
                                 difference=settings.snake_difference)

        self.food = food.Food(grid=self.grid,
                              color=settings.food_color)

    def mainloop(self):
        self.run = True

        threading.Thread(target=self.windowloop).start()

        while self.run:
            self.clock.tick(self.snake.speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.over()

            if not settings.AI:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.snake.direction = NORTH

                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.snake.direction = SOUTH

                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.snake.direction = WEST

                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.snake.direction = EAST

            else:
                if self.food != None:
                    self.snake.direction = AI.get_move(self.snake, self.food, self.grid)

            self.snake.move(settings.hardcore)

            if self.food != None:
                if self.snake.head_pos == self.food.pos:
                    self.snake.body_len += 1
                    self.snake.speed += 1

                    if self.snake.body_len != (len(self.grid.grid) - 1):
                        self.food.generate(self.snake)
                    else:
                        self.food = None

            if self.snake.check_collision(settings.hardcore):
                self.over()

        pygame.quit()

    def windowloop(self):
        while self.run:
            self.win.fill(self.bg_color)
            '''
            for i, (x, y, _, _) in enumerate(self.grid.grid):
                f = font.get("cpgb", 10)
                self.win.blit(f.render(str(i), False, (255, 255, 255)), (x, y+13))
            #'''
            self.snake.draw(self.win)

            if self.food != None:
                self.food.draw(self.win)

            pygame.display.update()

    def over(self):
        print(self.snake.direction)
        score = self.snake.body_len + 1
        total = len(self.grid.grid)
        your_high_score = f"0 / {total}"
        ai_high_score = f"0 / {total}"

        if os.path.exists("your_high_score.txt"):
            with open("your_high_score.txt", 'r') as f:
                your_high_score = f.read().strip()

        if os.path.exists("AI_high_score.txt"):
            with open("AI_high_score.txt", 'r') as f:
                ai_high_score = f.read().strip()

        if not settings.AI:
            if ((score / total) > eval(your_high_score)) or (\
                            ((score / total) == eval(your_high_score)) and \
                            (total > int(your_high_score.split(" / ")[1]))):
                msg = f"Old High Score: {your_high_score}\nCurrent Score / New High Score: {score} / {total}"
                your_high_score = f"{score} / {total}"
            else:
                msg = f"Current Score: {score} / {total}\nHighest Score: {your_high_score}"
        else:
            if ((score / total) > eval(ai_high_score)) or (\
                    ((score / total) > eval(ai_high_score)) and \
                    (total > int(ai_high_score.split(" / ")[1]))):
                msg = f"Old AI High Score: {ai_high_score}\nYour Highest Score: {your_high_score}\nCurrent Score / New AI High Score: {score} / {total}"
                ai_high_score = f"{score} / {total}"
            else:
                msg = f"Current Score: {score} / {total}\nYour Highest Score: {your_high_score}\nAI Highest Score: {ai_high_score}"

        messagebox.showinfo("Game Over!", msg)

        with open("your_high_score.txt", 'w') as f:
            f.write(str(your_high_score))

        with open("ai_high_score.txt", 'w') as f:
            f.write(str(ai_high_score))
        
        if not messagebox.askyesno("Restart?", "Would You Like To Play Again?"):
            self.run = False
            return

        self.reset_game()

if __name__ == "__main__":
    g = Game()
    g.mainloop()
