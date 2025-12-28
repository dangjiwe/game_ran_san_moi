import pygame
import sys
from pygame.math import Vector2

pygame.init()
pygame.mixer.init()

from game import Game
from menu import Menu
from constants import *
import sys

# Ép buộc Python in ra mã UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# --- CẤU HÌNH TỐC ĐỘ ---
SCREEN_UPDATE = pygame.USEREVENT
initial_speed = 150 # Tốc độ khởi điểm (ms)
current_delay = initial_speed 
pygame.time.set_timer(SCREEN_UPDATE, current_delay)

clock = pygame.time.Clock()

def show_loading_screen():
    start_time = pygame.time.get_ticks()
    loading_duration = 3000
    
    if MUSIC_LOADED:
        try: pygame.mixer.music.play(-1)
        except Exception: pass

    while pygame.time.get_ticks() - start_time < loading_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        if loading_bg_surface: screen.blit(loading_bg_surface, (0, 0))
        else: screen.fill(GRASS_LIGHT)
        
        text_str = "ĐANG TẢI TÀI NGUYÊN..."
        shadow_surf = font.render(text_str, True, (50, 50, 50))
        screen.blit(shadow_surf, (screen_width // 2 - shadow_surf.get_width()//2 + 2, screen_height // 2 - shadow_surf.get_height()//2 + 2))
        
        text_surf = font.render(text_str, True, (255, 255, 255))
        screen.blit(text_surf, text_surf.get_rect(center=(screen_width // 2, screen_height // 2)))
        
        pygame.display.update()
        clock.tick(60)

show_loading_screen()

game = Game()
menu = Menu(game.high_score)
is_paused = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if game.game_running:
                game.save_current_game()
            pygame.quit()
            sys.exit()

        # Bắt sự kiện hẹn giờ tắt nhạc khi Game Over
        if event.type == pygame.USEREVENT + 1:
            pygame.mixer.music.unpause() 

        # --- XỬ LÝ MENU ---
        if menu.is_active:
            # Nếu đang ở menu, KHÔNG gọi game.update() ở đây
            menu.high_score_data = game.high_score
            menu.handle_input(event, game)
            if not menu.is_active:
                is_paused = False
                game.start_countdown()
        
        # --- XỬ LÝ GAMEPLAY ---
        else:
            if event.type == SCREEN_UPDATE:
                if game.game_running and not is_paused:
                    game.update() # <--- CHỈ GỌI UPDATE Ở ĐÂY LÀ ĐỦ
                    
                    # --- LOGIC TĂNG TỐC ĐỘ MƯỢT MÀ ---
                    # Tính toán tốc độ mới dựa trên điểm số (game.score)
                    # Tốc độ tối đa là 50ms (rất nhanh), khởi điểm 150ms
                    new_delay = max(50, 150 - (game.score * 2))
                    
                    # Chỉ set lại timer khi tốc độ THỰC SỰ thay đổi 
                    # (Tránh gọi set_timer liên tục gây giật bộ đếm)
                    if new_delay != current_delay:
                        current_delay = new_delay
                        pygame.time.set_timer(SCREEN_UPDATE, new_delay)

            # Xử lý phím ESC và Chuột
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if not menu.show_high_score and not menu.show_settings:
                    menu.is_active = True
                    is_paused = True
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if game.pause_button_rect and game.pause_button_rect.collidepoint(mouse_pos):
                    is_paused = not is_paused
                    if not is_paused: game.start_countdown()
                elif game.back_button_rect and game.back_button_rect.collidepoint(mouse_pos):
                    menu.is_active = True; is_paused = True

            # Xử lý điều khiển rắn
            if event.type == pygame.KEYDOWN and not is_paused:
                if game.game_running and not game.countdown_active:
                   if game.snake.can_move:
                        if event.key == pygame.K_UP and game.snake.direction.y != 1:
                            game.snake.direction = Vector2(0, -1); game.snake.can_move = False
                        elif event.key == pygame.K_DOWN and game.snake.direction.y != -1:
                            game.snake.direction = Vector2(0, 1); game.snake.can_move = False
                        elif event.key == pygame.K_LEFT and game.snake.direction.x != 1:
                            game.snake.direction = Vector2(-1, 0); game.snake.can_move = False
                        elif event.key == pygame.K_RIGHT and game.snake.direction.x != -1:
                            game.snake.direction = Vector2(1, 0); game.snake.can_move = False

                elif event.key == pygame.K_SPACE and not game.game_running:
                    game.reset_game(); game.start_countdown()

    # Vẽ màn hình
    if menu.is_active:
        menu.draw_with_game_data(game.snake.skin_id)
    else:
        game.draw_elements(screen, is_paused)
        pygame.display.update()

    clock.tick(60)