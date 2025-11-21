# files/main.py

import pygame
import sys
import os 
from pygame.math import Vector2 

# --- THIẾT LẬP PATH ĐỂ IMPORT MODULE ---
current_dir = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(os.path.join(current_dir, 'Resources')) 
# ---------------------------------------

from game import Game
from menu import Menu 
from constants import SCREEN_UPDATE, screen 

# --- CẤU HÌNH ---
pygame.time.set_timer(SCREEN_UPDATE, 150) 
game = Game()
menu = Menu(game.high_score) 
is_paused = False 
clock = pygame.time.Clock()

while True:
    # Cập nhật điểm cao cho menu
    menu.high_score_data = game.high_score
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # 1. XỬ LÝ PHÍM ESC (MENU / PAUSE)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if not menu.show_high_score and not menu.show_settings:
                if not menu.is_active:
                    menu.is_active = True
                    is_paused = True 
        
        # 2. XỬ LÝ KHI Ở MENU
        if menu.is_active:
            menu.handle_input(event, game)
            
            # Nếu vừa thoát menu để vào game
            if not menu.is_active:
                is_paused = False
                game.start_countdown() # Bắt đầu đếm ngược

        # 3. XỬ LÝ KHI ĐANG CHƠI GAME
        else: 
            # Xử lý Click Chuột (Nút Tạm Dừng / Quay Lại)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                
                # Nút Tạm Dừng / Tiếp Tục
                if game.pause_button_rect and game.pause_button_rect.collidepoint(mouse_pos):
                    if is_paused:
                        is_paused = False
                        game.start_countdown() # Đếm ngược khi tiếp tục
                    else:
                        is_paused = True
                
                # Nút Quay Lại Menu
                elif game.back_button_rect and game.back_button_rect.collidepoint(mouse_pos):
                    menu.is_active = True
                    is_paused = True
                    
            # Logic Game (Chỉ chạy khi không tạm dừng)
            if event.type == SCREEN_UPDATE:
                if game.game_running and not is_paused:
                    game.update()
                
            # Điều khiển Rắn (Chỉ nhận khi không tạm dừng và không đếm ngược)
            if event.type == pygame.KEYDOWN and not is_paused:
                if game.game_running and not game.countdown_active: 
                    if event.key == pygame.K_UP and game.snake.direction.y != 1: 
                        game.snake.direction = Vector2(0, -1)
                    elif event.key == pygame.K_DOWN and game.snake.direction.y != -1: 
                        game.snake.direction = Vector2(0, 1)
                    elif event.key == pygame.K_LEFT and game.snake.direction.x != 1: 
                        game.snake.direction = Vector2(-1, 0)
                    elif event.key == pygame.K_RIGHT and game.snake.direction.x != -1: 
                        game.snake.direction = Vector2(1, 0)
                
                # Chơi lại khi Game Over (Nhấn SPACE)
                elif event.key == pygame.K_SPACE and not game.game_running: 
                    game.reset_game()
                    game.start_countdown()
                
    # --- VẼ MÀN HÌNH ---
    if menu.is_active:
        menu.draw() 
    else:
        game.draw_elements(is_paused) 
        pygame.display.update() 

    clock.tick(60)