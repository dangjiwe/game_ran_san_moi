# game.py

from snake import Snake
from food import Food
from constants import screen, GREEN, DARK_GREEN, cell_size, number_of_cells, OFFSET, font
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
            
            # --- KHÔI PHỤC: Xuyên tường (A ra B) ---
            self.wrap_around_walls() 
            # BỎ: self.check_wall_collision()
            
            self.check_eat_food()
            self.check_self_collision()

    def draw_elements(self):
        # Nội dung giữ nguyên
        self.draw_grass() 
        self.food.draw()
        self.snake.draw()
        self.draw_score() 
        
        if not self.game_running:
            self.draw_game_over()

    def draw_grass(self):
        # Nội dung giữ nguyên
        screen.fill(GREEN)
        pygame.draw.rect(screen, DARK_GREEN, 
            (OFFSET - 5, OFFSET - 5, 
             cell_size * number_of_cells + 10, 
             cell_size * number_of_cells + 10), 5)
        
    def check_eat_food(self):
        # Nội dung giữ nguyên
        head = self.snake.body[0]
        
        if head == self.food.position:
            self.snake.add_block()
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.score += 1
            
    def check_self_collision(self):
        # Nội dung giữ nguyên (Thua khi chạm thân)
        if self.snake.check_self_bite():
            self.game_over()
            
    # --- LOẠI BỎ: Va chạm với tường (Biên) ---
    def check_wall_collision(self):
        # Hàm này không còn được gọi trong update()
        pass

    # --- CHỨC NĂNG XUYÊN TƯỜNG (A ra B) ---
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

        # NOTE: Vì head là Vector2, các thay đổi trên head đã thay đổi body[0]
        # Không cần gán lại: self.snake.body[0] = head 
        
    def game_over(self):
        # Nội dung giữ nguyên
        self.game_running = False
        
    def reset_game(self):
        # Nội dung giữ nguyên
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.game_running = True
        self.score = 0
        
    def draw_score(self):
        # Nội dung giữ nguyên
        score_text = str(self.score)
        score_surf = font.render(score_text, True, DARK_GREEN)
        
        score_x = OFFSET - 5
        score_y = OFFSET + cell_size * number_of_cells + 10 
        
        screen.blit(score_surf, (score_x, score_y))
        
    def draw_game_over(self):
        # Nội dung giữ nguyên
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