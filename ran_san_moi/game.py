# game.py

from snake import Snake
from food import Food
# Import từ constants: BỔ SUNG score_font
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
        if self.game_running:
            self.snake.move_snake()
            
            # --- CHỨC NĂNG XUYÊN TƯỜNG (A ra B) ---
            self.wrap_around_walls() 
            
            self.check_eat_food()
            self.check_self_collision()

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

    def wrap_around_walls(self):
        head = self.snake.body[0]
        
        # Xuyên ngang (Trái sang Phải / Phải sang Trái)
        if head.x >= number_of_cells:
            head.x = 0
        elif head.x < 0:
            head.x = number_of_cells - 1
            
        # Xuyên dọc (Trên xuống Dưới / Dưới lên Trên)
        if head.y >= number_of_cells:
            head.y = 0
        elif head.y < 0:
            head.y = number_of_cells - 1

        
    def game_over(self):
        self.game_running = False
        
    def reset_game(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.game_running = True
        self.score = 0
        
    def draw_score(self):
        # --- ĐÃ SỬA: Dùng score_font (cỡ 60, Times New Roman) ---
        score_text = str(self.score)
        score_surf = score_font.render(score_text, True, DARK_GREEN) 
        
        score_x = OFFSET - 5
        score_y = OFFSET + cell_size * number_of_cells + 10 
        
        screen.blit(score_surf, (score_x, score_y))
        
    def draw_game_over(self):
        # Dùng font (cỡ 40, Times New Roman) cho Game Over
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