# files/Resources/game.py

from snake import Snake
from food import Food
# IMPORT ĐẦY ĐỦ (BAO GỒM eat_sound)
from constants import screen, GRASS_LIGHT, GRASS_DARK, BORDER_COLOR, DARK_GREEN, cell_size, number_of_cells, OFFSET, font, screen_width, screen_height, PROJECT_ROOT, BLACK, bg_surface, eat_sound
import pygame
import sys 
import json 
import os 

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.game_running = True 

        self.save_dir = os.path.join(PROJECT_ROOT, "save") 
        self.save_file_path = os.path.join(self.save_dir, "high_score.json") 
        self.high_score = 0
        self.load_high_score()
        
        self.pause_button_rect = None 
        self.back_button_rect = None
        
        self.countdown_active = False
        self.countdown_value = 3
        self.last_countdown_time = 0

    def load_high_score(self):
        if os.path.exists(self.save_file_path):
            try:
                with open(self.save_file_path, 'r') as f:
                    data = json.load(f)
                self.high_score = data.get('high_score', 0)
            except: self.high_score = 0
        else: self.high_score = 0

    def save_high_score(self):
        current_score = len(self.snake.body) - 3
        if current_score >= self.high_score:
            self.high_score = current_score
            if not os.path.exists(self.save_dir):
                os.makedirs(self.save_dir)
            try:
                with open(self.save_file_path, 'w') as f:
                    json.dump({'high_score': self.high_score}, f, indent=4)
            except: pass

    def start_countdown(self):
        self.countdown_active = True
        self.countdown_value = 3
        self.last_countdown_time = pygame.time.get_ticks()

    def update(self):
        if self.countdown_active:
            if pygame.time.get_ticks() - self.last_countdown_time >= 1000:
                self.countdown_value -= 1
                self.last_countdown_time = pygame.time.get_ticks()
                if self.countdown_value == 0:
                    self.countdown_active = False
            return 

        if self.game_running:
            self.snake.move_snake()
            self.check_eat_food()
            self.check_wall_collision()
            self.check_self_collision()

    def draw_button(self, text, x_offset, y_pos):
        text_surf = font.render(text, True, BLACK)
        button_w = text_surf.get_width() + 30
        button_h = text_surf.get_height() + 20
        rect = pygame.Rect(x_offset, y_pos, button_w, button_h)
        pygame.draw.rect(screen, (200, 200, 200), rect, 0, 8) 
        pygame.draw.rect(screen, BLACK, rect, 2, 8)
        screen.blit(text_surf, text_surf.get_rect(center=rect.center))
        return rect

    def draw_elements(self, is_paused):
        self.draw_grass() 
        
        if self.game_running or is_paused:
            grid_bottom = OFFSET + (cell_size * number_of_cells)
            btn_y = grid_bottom + 15
            
            pause_txt = "TẠM DỪNG" if not is_paused else "TIẾP TỤC"
            self.pause_button_rect = self.draw_button(pause_txt, OFFSET, btn_y)
            
            back_x = OFFSET + self.pause_button_rect.width + 20
            self.back_button_rect = self.draw_button("QUAY LẠI", back_x, btn_y)

        if self.game_running and not is_paused:
            self.food.draw()
            self.snake.draw()
        elif is_paused:
            self.draw_paused_msg()
            
        if not self.game_running:
            self.draw_game_over()
        
        self.draw_score() 
        if self.countdown_active:
            self.draw_countdown()

    def draw_grass(self):
        # Ưu tiên vẽ background từ ảnh (nếu có load được)
        if bg_surface:
             screen.blit(bg_surface, (0, 0))
        else:
            # Nếu không có ảnh, vẽ bàn cờ caro
            screen.fill(BORDER_COLOR)
            for row in range(number_of_cells):
                for col in range(number_of_cells):
                    x = OFFSET + col * cell_size
                    y = OFFSET + row * cell_size
                    rect = pygame.Rect(x, y, cell_size, cell_size)
                    if (row + col) % 2 == 0:
                        pygame.draw.rect(screen, GRASS_LIGHT, rect)
                    else:
                        pygame.draw.rect(screen, GRASS_DARK, rect)

    def draw_countdown(self):
        txt = str(self.countdown_value)
        try: big_font = pygame.font.Font(font, 150) 
        except: big_font = pygame.font.SysFont('Arial', 150)
        surf = big_font.render(txt, True, (255, 255, 255))
        outline = big_font.render(txt, True, BLACK)
        rect = surf.get_rect(center=(screen_width//2, screen_height//2))
        screen.blit(outline, (rect.x+2, rect.y+2))
        screen.blit(surf, rect)

    def draw_paused_msg(self):
        surf = font.render("TẠM DỪNG", True, (0, 0, 255))
        grid_center = (OFFSET + (cell_size * number_of_cells)//2)
        screen.blit(surf, surf.get_rect(center=(grid_center, grid_center)))

    def draw_score(self):
        score = len(self.snake.body) - 3
        s_surf = font.render(f"ĐIỂM: {score}", True, DARK_GREEN)
        screen.blit(s_surf, (screen_width - OFFSET - s_surf.get_width(), OFFSET - 50))
        h_surf = font.render(f"CAO NHẤT: {self.high_score}", True, DARK_GREEN)
        screen.blit(h_surf, (OFFSET, OFFSET - 50))
             
    def draw_game_over(self):
        l1 = font.render("GAME OVER!", True, (255, 0, 0))
        l2 = font.render("Nhấn SPACE để chơi lại.", True, DARK_GREEN)
        cy = screen_height // 2
        screen.blit(l1, l1.get_rect(center=(screen_width//2, cy - 30)))
        screen.blit(l2, l2.get_rect(center=(screen_width//2, cy + 30)))

    def check_eat_food(self):
        if self.food.position == self.snake.body[0]:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_block()
            
            # --- PHÁT ÂM THANH VÀ DEBUG ---
            if eat_sound:
                eat_sound.play()
                # print("----> Đã ăn!") 
            else:
                print("----> Lỗi: Không tìm thấy âm thanh ăn!")
            # ------------------------------

    def check_wall_collision(self):
        head = self.snake.body[0]
        if not (0 <= head.x < number_of_cells and 0 <= head.y < number_of_cells):
            self.game_over()

    def check_self_collision(self):
        if self.snake.body[0] in self.snake.body[1:]:
            self.game_over()

    def game_over(self):
        self.save_high_score() 
        self.game_running = False 

    def reset_game(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.game_running = True
        self.countdown_active = False
        self.load_high_score()