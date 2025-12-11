import pygame
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
        
        # --- LOGIC ---
        self.hs_manager = HighScoreManager()
        self.renderer = GameRenderer() # Gọi class vẽ từ file bên kia
        
        self.high_score = self.hs_manager.load()
        
        # Biến lưu vị trí nút bấm (để check click chuột trong main)
        self.pause_button_rect = None 
        self.back_button_rect = None
        
        # Biến đếm ngược
        self.countdown_active = False
        self.countdown_value = 3
        self.last_countdown_time = 0

    def start_countdown(self):
        self.countdown_active = True
        self.countdown_value = 3
        self.last_countdown_time = pygame.time.get_ticks()

    def update(self):
        if self.game_running:
            self.snake.move_snake()
            
            # --- CHỨC NĂNG XUYÊN TƯỜNG (A ra B) ---
            self.wrap_around_walls() 
            
            self.check_eat_food()
            self.check_wall_collision()
            self.check_self_collision()

    def draw_elements(self, is_paused):
        """
        Hàm này đóng vai trò 'nhạc trưởng', chỉ đạo renderer vẽ cái gì
        """
        # Vẽ nền
        self.renderer.draw_grass()
        
        # Vẽ nút bấm và lưu lại rect để main.py xử lý click
        if self.game_running or is_paused:
            grid_bottom = OFFSET + (cell_size * number_of_cells)
            btn_y = grid_bottom + 15
            pause_txt = "TẠM DỪNG" if not is_paused else "TIẾP TỤC"
            
            self.pause_button_rect = self.renderer.draw_button(pause_txt, OFFSET, btn_y)
            
            back_x = OFFSET + self.pause_button_rect.width + 20
            self.back_button_rect = self.renderer.draw_button("QUAY LẠI", back_x, btn_y)

        # Vẽ rắn/mồi
        if self.game_running and not is_paused:
            self.food.draw()
            self.snake.draw()
        elif is_paused:
            self.renderer.draw_paused_msg()
            
        # Vẽ Game Over
        if not self.game_running:
            self.renderer.draw_game_over()
        
        # Vẽ Điểm
        current_score = len(self.snake.body) - 3
        self.renderer.draw_score(current_score, self.high_score)
        
        # Vẽ đếm ngược
        if self.countdown_active:
            self.renderer.draw_countdown(self.countdown_value)

    def check_eat_food(self):
        if self.food.position == self.snake.body[0]:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_block()
            if eat_sound:
                eat_sound.play()

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
        current_score = len(self.snake.body) - 3
        if current_score > self.high_score:
            self.high_score = current_score
            self.hs_manager.save(self.high_score)
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