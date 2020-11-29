import graphics
import pygame

cols = 20
rows = 20
cell_width = 35
cell_height = 35
bg_color = 0,0,0
snake_start_speed = 5
snake_head_type = graphics.PIC
snake_head_arg = pygame.image.load("head.png")
snake_body_color = 255, 255, 255
snake_difference = -5
snake_start_body_len = 1
food_color = 255, 0, 0
