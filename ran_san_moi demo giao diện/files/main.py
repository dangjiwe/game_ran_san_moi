# files/main.py

import pygame
import sys
import os 
from pygame.math import Vector2 

# --- THIẾT LẬP PATH ---
current_dir = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(os.path.join(current_dir, 'Resources')) 

from game import Game
from menu import Menu 
# Import đầy đủ biến
from constants import SCREEN_UPDATE, MUSIC_LOADED, screen, font, screen_width, screen_height, GRASS_LIGHT, BLACK, loading_bg_surface

# --- HÀM VẼ MÀN HÌNH LOADING ---
def show_loading_screen():
    # 1. VẼ GIAO DIỆN
    if loading_bg_surface:
        screen.blit(loading_bg_surface, (0, 0))
    else:
        screen.fill(GRASS_LIGHT)
    
    text_str = "ĐANG TẢI TÀI NGUYÊN..."
    
    # Bóng chữ
    shadow_surf = font.render(text_str, True, (50, 50, 50))
    shadow_rect = shadow_surf.get_rect(center=(screen_width // 2 + 2, screen_height // 2 + 2))
    screen.blit(shadow_surf, shadow_rect)
    
    # Chữ chính
    text_surf = font.render(text_str, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text_surf, text_rect)
    
    # 2. HIỆN HÌNH LÊN (UPDATE MÀN HÌNH)
    pygame.display.update()
    
    # 3. BẬT NHẠC NGAY LẬP TỨC (Không delay)
    # Nhạc sẽ vang lên ngay tích tắc hình ảnh hiện ra
    if MUSIC_LOADED:
        try:
            pygame.mixer.music.play(-1) 
        except: pass

    # 4. GIỮ NGUYÊN TRẠNG THÁI NÀY TRONG 3 GIÂY
    # Để người chơi kịp nhìn thấy màn hình loading và nghe đoạn dạo đầu của nhạc
    pygame.time.delay(3000) 
# -------------------------------

# --- CẤU HÌNH ---
pygame.time.set_timer(SCREEN_UPDATE, 150) 
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
            
        # 1. XỬ LÝ PHÍM ESC
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if not menu.show_high_score and not menu.show_settings:
                if not menu.is_active:
                    menu.is_active = True
                    is_paused = True 
        
        # 2. XỬ LÝ MENU
        if menu.is_active:
            menu.handle_input(event, game)
            if not menu.is_active:
                is_paused = False
                game.start_countdown() 

        # 3. XỬ LÝ GAME
        else: 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if game.pause_button_rect and game.pause_button_rect.collidepoint(mouse_pos):
                    if is_paused:
                        is_paused = False
                        game.start_countdown()
                    else:
                        is_paused = True
                elif game.back_button_rect and game.back_button_rect.collidepoint(mouse_pos):
                    menu.is_active = True
                    is_paused = True
                    
            if event.type == SCREEN_UPDATE:
                if game.game_running and not is_paused:
                    game.update()
                
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
                
                elif event.key == pygame.K_SPACE and not game.game_running: 
                    game.reset_game()
                    game.start_countdown()
                
    # --- VẼ ---
    if menu.is_active:
        menu.draw() 
    else:
        game.draw_elements(is_paused) 
        pygame.display.update() 

    clock.tick(60)