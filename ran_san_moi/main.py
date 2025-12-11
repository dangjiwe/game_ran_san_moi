# files/main.py

import pygame
import sys
# Import constants sớm để pygame.init() được gọi (Khắc phục lỗi #1)
from constants import SCREEN_UPDATE 
from game import Game
from pygame.math import Vector2 

# Thiết lập tốc độ di chuyển (Khắc phục lỗi #2)
# Không cần gọi pygame.init() ở đây vì đã gọi trong constants.py
pygame.time.set_timer(SCREEN_UPDATE, 150)

# Khởi tạo đối tượng Game
game = Game()

# Khởi tạo Clock
clock = pygame.time.Clock()

# --- CHẠY LOADING ---
show_loading_screen()
# --------------------

# Sau khi Loading xong mới khởi tạo Game
game = Game()
menu = Menu(game.high_score) 
is_paused = False 

# --- VÒNG LẶP CHÍNH ---
while True:
    menu.high_score_data = game.high_score
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # 1. Xử lý sự kiện tự động di chuyển
        if event.type == SCREEN_UPDATE:
            game.update()
            
        # 2. Xử lý Input điều khiển rắn (Khắc phục lỗi #3 & #4)
        if event.type == pygame.KEYDOWN:
            # Chỉ cập nhật next_direction, ngăn đổi hướng 180 độ
            if game.game_running:
                current_direction = game.snake.direction 
                
                # Kiểm tra hướng ngược để ngăn đổi hướng 180 độ
                if event.key == pygame.K_UP and current_direction.y != 1: 
                    game.snake.next_direction = Vector2(0, -1)
                elif event.key == pygame.K_DOWN and current_direction.y != -1: 
                    game.snake.next_direction = Vector2(0, 1)
                elif event.key == pygame.K_LEFT and current_direction.x != 1: 
                    game.snake.next_direction = Vector2(-1, 0)
                elif event.key == pygame.K_RIGHT and current_direction.x != -1: 
                    game.snake.next_direction = Vector2(1, 0)
            
            # Reset Game khi Game Over (nhấn SPACE)
            elif event.key == pygame.K_SPACE and not game.game_running: 
                game.reset_game()
                
    # Vẽ tất cả các thành phần trò chơi
    game.draw_elements()
    
    # Cập nhật màn hình
    pygame.display.update()
    
    # Giới hạn tốc độ khung hình (FPS)
    clock.tick(55)