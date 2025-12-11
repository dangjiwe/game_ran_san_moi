# game.py

from snake import Snake
from food import Food
from constants import screen, GREEN, DARK_GREEN, cell_size, number_of_cells, OFFSET, font, score_font
import pygame
from pygame.math import Vector2 

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.game_running = True
        self.score = 0

    def update(self):
        # --- SỬA LỖI 3: Chỉ cập nhật logic game khi game đang chạy ---
        if self.game_running:
            
            # --- SỬA LỖI 1: Cập nhật hướng chính bằng hướng chờ (next_direction) trước move_snake() ---
            self.snake.direction = self.snake.next_direction 
            
            # LỖI 4 (Xuyên tường) ĐÃ CHUYỂN LOGIC SANG snake.py.
            
            self.snake.move_snake()
            
            self.check_eat_food()
            self.check_self_collision()
            
            # --- LỖI 4: wrap_around_walls() đã được di chuyển vào snake.py
            # self.wrap_around_walls() 

    def draw_elements(self):
        self.draw_grass() 
        self.food.draw()
        self.snake.draw()
        self.draw_score() 
        
        if not self.game_running:
            self.draw_game_over()

    def draw_grass(self):
        screen.fill(GREEN)
        pygame.draw.rect(screen, DARK_GREEN, 
            (OFFSET - 5, OFFSET - 5, 
             cell_size * number_of_cells + 10, 
             cell_size * number_of_cells + 10), 5)
        
    def check_eat_food(self):
        head = self.snake.body[0]
        
        if head == self.food.position:
            self.snake.add_block()
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.score += 1
            
    def check_self_collision(self):
        if self.snake.check_self_bite():
            self.game_over()
            
    def check_wall_collision(self):
        pass

    # --- LỖI 4: Hàm wrap_around_walls() đã được di chuyển và tích hợp vào Snake.move_snake()
    # def wrap_around_walls(self):
    #     ...
        
    def game_over(self):
        self.game_running = False
        
    def reset_game(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.game_running = True
        self.score = 0
        
    def draw_score(self):
        score_text = str(self.score)
        score_surf = score_font.render(score_text, True, DARK_GREEN) 
        
        score_x = OFFSET - 5
        score_y = OFFSET + cell_size * number_of_cells + 10 
        
        screen.blit(score_surf, (score_x, score_y))
        
    def draw_game_over(self):
        line1_text = "GAME OVER!"
        line2_text = "NHAN SPACE DE CHOI LAI."
        
        line1_surf = font.render(line1_text, True, DARK_GREEN)
        line2_surf = font.render(line2_text, True, DARK_GREEN)
        
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()
        
        total_height = line1_surf.get_height() + line2_surf.get_height() + 10 
        start_y = (screen_height - total_height) // 2
        
        line1_x = (screen_width - line1_surf.get_width()) // 2
        line2_x = (screen_width - line2_surf.get_width()) // 2
        
        screen.blit(line1_surf, (line1_x, start_y))
        screen.blit(line2_surf, (line2_x, start_y + line1_surf.get_height() + 10))