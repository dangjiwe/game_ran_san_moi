# main.py

import pygame
import sys
from constants import SCREEN_UPDATE 
from game import Game
from pygame.math import Vector2 

# Thiết lập tốc độ di chuyển
pygame.time.set_timer(SCREEN_UPDATE, 150)

# Khởi tạo đối tượng Game
game = Game()

# Khởi tạo Clock
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # 1. Xử lý sự kiện tự động di chuyển
        if event.type == SCREEN_UPDATE:
            game.update()
            
        # 2. Xử lý Input điều khiển rắn 
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
    
    # --- SỬA LỖI 2: XÓA giới hạn FPS clock.tick(60) ---
    # Giữ nguyên tốc độ khung hình (FPS) tối đa của màn hình
    # và chỉ sử dụng timer SCREEN_UPDATE để điều khiển tốc độ game logic.
    # clock.tick(60)
    
    # NOTE: Nếu muốn ổn định FPS, có thể dùng clock.tick(60) nhưng phải đảm bảo 
    # tốc độ logic game (150ms) là bội số/ước số của 1/60s. 
    # Tuy nhiên, để tuân thủ phương án "bỏ tick(55)" của tài liệu, tôi đã xóa clock.tick().