# game.py

from snake import Snake
from food import Food
from constants import screen, GREEN, DARK_GREEN, cell_size, number_of_cells, OFFSET
import pygame

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)

    def draw_elements(self):
        # Vẽ các thành phần trò chơi
        self.draw_grass()  # Vẽ nền và khung
        self.food.draw()
        self.snake.draw()

    def draw_grass(self):
        # 1. Tô nền
        screen.fill(GREEN)
        
        # 2. Vẽ khung viền lưới
        pygame.draw.rect(screen, DARK_GREEN, 
            (OFFSET - 5, OFFSET - 5, 
             cell_size * number_of_cells + 10, 
             cell_size * number_of_cells + 10), 5)
        
        # (Bạn có thể thêm phần vẽ lưới ô cờ ở đây nếu muốn)