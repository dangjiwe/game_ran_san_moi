# game.py

from snake import Snake
from food import Food
# Import thêm các hằng số cần thiết
from constants import screen, GREEN, DARK_GREEN, cell_size, number_of_cells, OFFSET, font
import pygame
from pygame.math import Vector2 # Cần thiết cho các vị trí Vector2

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.game_running = True # Trạng thái trò chơi

    def update(self):
        if self.game_running:
            self.snake.move_snake()
            self.check_eat_food()
            self.check_wall_collision()
            self.check_self_collision()

    def draw_elements(self):
        # Vẽ các thành phần trò chơi
        self.draw_grass() # Vẽ nền và khung
        self.food.draw()
        self.snake.draw()
        
        # --- VẼ GAME OVER KHI DỪNG ---
        if not self.game_running:
            self.draw_game_over()

    def draw_grass(self):
        # 1. Tô nền
        screen.fill(GREEN)
        
        # 2. Vẽ khung viền lưới
        pygame.draw.rect(screen, DARK_GREEN, 
            (OFFSET - 5, OFFSET - 5, 
             cell_size * number_of_cells + 10, 
             cell_size * number_of_cells + 10), 5)
        
    def check_eat_food(self):
        # Lấy vị trí đầu rắn
        head = self.snake.body[0]
        
        # 1. Kiểm tra va chạm (Vị trí đầu rắn == Vị trí thức ăn)
        if head == self.food.position:
            # 2. Gọi chức năng rắn dài ra
            self.snake.add_block()
            
            # 3. Tạo thức ăn mới (không trùng với thân rắn)
            self.food.position = self.food.generate_random_pos(self.snake.body)
            
    def check_self_collision(self):
        if self.snake.check_self_bite(): # Giả sử check_self_bite có trong class Snake
            self.game_over()
            
    def check_wall_collision(self):
        head = self.snake.body[0]
        
        # KIỂM TRA VA CHẠM TƯỜNG (khi đầu rắn vừa chạm vào biên 0 hoặc N-1)
        if (head.x == 0 or 
            head.x == number_of_cells - 1 or 
            head.y == 0 or 
            head.y == number_of_cells - 1):
            self.game_over()
            
    def game_over(self):
        # Dừng trò chơi
        self.game_running = False
        
    # --- ĐÃ SỬA: HIỂN THỊ GAME OVER TRÊN 2 DÒNG VÀ CĂN GIỮA ---
    def draw_game_over(self):
        # 1. Định nghĩa văn bản cho hai dòng
        line1_text = "GAME OVER!"
        line2_text = "Nhan SPACE de choi lai."
        
        # 2. Render hai dòng văn bản thành hai Surface riêng biệt
        line1_surf = font.render(line1_text, True, DARK_GREEN)
        line2_surf = font.render(line2_text, True, DARK_GREEN)
        
        # 3. Lấy kích thước màn hình
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()
        
        # 4. Tính toán vị trí Y cơ bản (căn giữa tổng thể)
        total_height = line1_surf.get_height() + line2_surf.get_height() + 10 # 10 là khoảng cách giữa 2 dòng
        start_y = (screen_height - total_height) // 2
        
        # 5. Tính toán vị trí X (căn giữa theo chiều ngang)
        line1_x = (screen_width - line1_surf.get_width()) // 2
        line2_x = (screen_width - line2_surf.get_width()) // 2
        
        # 6. Vẽ văn bản lên màn hình
        # Dòng 1
        screen.blit(line1_surf, (line1_x, start_y))
        # Dòng 2 (cộng thêm chiều cao dòng 1 và khoảng cách 10)
        screen.blit(line2_surf, (line2_x, start_y + line1_surf.get_height() + 10))