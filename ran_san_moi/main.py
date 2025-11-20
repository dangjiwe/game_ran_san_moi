# main.py

import pygame
import sys
from game import Game
# Cần import SCREEN_UPDATE từ constants
from constants import SCREEN_UPDATE
from pygame.math import Vector2 

# --- BỔ SUNG: CẤU HÌNH THỜI GIAN ---
# Thiết lập tốc độ di chuyển: 150ms/ô (tùy chỉnh tốc độ tại đây)
pygame.time.set_timer(SCREEN_UPDATE, 150)
# ------------------------------------

# Khởi tạo đối tượng Game
game = Game()

# Khởi tạo Clock (dùng để giới hạn tốc độ frame)
clock = pygame.time.Clock()

while True:
    # Xử lý input từ người dùng và sự kiện thời gian
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # 1. Xử lý sự kiện tự động di chuyển (TIMER EVENT)
        if event.type == SCREEN_UPDATE:
            game.update()
            
        # 2. Xử lý Input điều khiển rắn
        if event.type == pygame.KEYDOWN:
            # Điều khiển: Kiểm tra không cho quay ngược 180 độ
            if event.key == pygame.K_UP and game.snake.direction.y != 1: 
                # Chỉ cho phép đổi hướng khi trò chơi đang chạy
                if game.game_running:
                    game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN and game.snake.direction.y != -1: 
                if game.game_running:
                    game.snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_LEFT and game.snake.direction.x != 1: 
                if game.game_running:
                    game.snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT and game.snake.direction.x != -1: 
                if game.game_running:
                    game.snake.direction = Vector2(1, 0)
            
            # Reset Game khi Game Over (nhấn SPACE)
            elif event.key == pygame.K_SPACE and not game.game_running: 
                game.snake.reset()
                # Tạo thức ăn mới, đảm bảo không trùng với vị trí rắn
                game.food.position = game.food.generate_random_pos(game.snake.body) 
                game.game_running = True
                
    # Vẽ tất cả các thành phần trò chơi
    game.draw_elements()
    
    # Cập nhật màn hình
    pygame.display.update()
    
    # Giới hạn tốc độ khung hình (FPS)
    clock.tick(60)