# food.py

import random
from pygame.math import Vector2
import pygame
from constants import cell_size, number_of_cells, OFFSET, food_surface, screen

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)

    def draw(self):
        # Tạo hình chữ nhật cho Food
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, 
                                OFFSET + self.position.y * cell_size, 
                                cell_size, cell_size)
        # Vẽ bề mặt Food lên màn hình
        screen.blit(food_surface, food_rect)

    def generate_random_cell(self):
        # Tạo tọa độ (x, y) ngẫu nhiên trong lưới
        x = random.randint(0, number_of_cells - 1)
        y = random.randint(0, number_of_cells - 1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body):
        # Tạo vị trí ngẫu nhiên không trùng với thân Rắn
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position