# files/main.py

import pygame
import sys
import os 
from pygame.math import Vector2 

current_dir = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(os.path.join(current_dir, 'Resources')) 

from game import Game
from menu import Menu 
from constants import SCREEN_UPDATE, MUSIC_LOADED, screen, font, screen_width, screen_height, GRASS_LIGHT, BLACK, loading_bg_surface

def show_loading_screen():
    if loading_bg_surface: screen.blit(loading_bg_surface, (0, 0))
    else: screen.fill(GRASS_LIGHT)
    text_str = "ĐANG TẢI TÀI NGUYÊN..."
    shadow_surf = font.render(text_str, True, (50, 50, 50))
    screen.blit(shadow_surf, shadow_surf.get_rect(center=(screen_width // 2 + 2, screen_height // 2 + 2)))
    text_surf = font.render(text_str, True, (255, 255, 255))
    screen.blit(text_surf, text_surf.get_rect(center=(screen_width // 2, screen_height // 2)))
    pygame.display.update()
    if MUSIC_LOADED:
        try: pygame.mixer.music.play(-1) 
        except: pass
    pygame.time.delay(3000) 

pygame.time.set_timer(SCREEN_UPDATE, 150) 
clock = pygame.time.Clock()
show_loading_screen()

game = Game()
menu = Menu(game.high_score) 
is_paused = False 

while True:
    menu.high_score_data = game.high_score
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if game.game_running:
                game.save_current_game()
                print("----> (QUIT) Da luu game!")
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if not menu.show_high_score and not menu.show_settings and not menu.show_tutorial and not menu.show_mode_selection and not menu.show_no_save_popup:
                if not menu.is_active:
                    if game.game_running:
                        game.save_current_game()
                    menu.is_active = True
                    is_paused = True 
        
        # --- XỬ LÝ MENU ---
        if menu.is_active:
            menu.handle_input(event, game)
            
            # === [FIX LỖI ĐƠ - DÙNG BIẾN CỜ CHUẨN] ===
            # Nếu Menu bật tín hiệu "Bắt đầu game"
            if menu.start_game_trigger:
                menu.start_game_trigger = False # Reset cờ ngay
                is_paused = False               # Bỏ pause
                game.start_countdown()          # Đếm ngược 3-2-1
            # Hoặc nếu menu tắt (ví dụ nút Chơi Tiếp) mà chưa chạy game
            elif not menu.is_active and is_paused:
                 is_paused = False
                 # (Không gọi start_countdown ở đây để tránh reset rắn đang chạy)
            # ==========================================

        # --- XỬ LÝ GAME ---
        else: 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if game.game_running or is_paused:
                    if game.pause_button_rect and game.pause_button_rect.collidepoint(mouse_pos):
                        if is_paused:
                            is_paused = False
                            game.start_countdown()
                        else:
                            is_paused = True
                    elif game.back_button_rect and game.back_button_rect.collidepoint(mouse_pos):
                        if game.game_running:
                            game.save_current_game()
                        menu.is_active = True
                        is_paused = True
                
                if not game.game_running:
                    if game.go_home_rect and game.go_home_rect.collidepoint(mouse_pos):
                        menu.is_active = True
                        is_paused = False
                    elif game.go_replay_rect and game.go_replay_rect.collidepoint(mouse_pos):
                        game.reset_game()
                        game.start_countdown()

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
                
    if menu.is_active:
        menu.draw() 
    else:
        game.draw_elements(is_paused) 
        pygame.display.update() 

    clock.tick(60)