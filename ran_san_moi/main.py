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
initial_speed = 250 # Tốc độ khởi điểm (ms)
current_delay = initial_speed 
pygame.time.set_timer(SCREEN_UPDATE, current_delay)

clock = pygame.time.Clock()

def play_bg_music(music_path):
    """Hàm này giúp chuyển bài hát mượt mà"""
    if not music_path: return
    
    try:
        # Dừng nhạc cũ
        pygame.mixer.music.stop()
        # Load nhạc mới
        pygame.mixer.music.load(music_path)
        # Phát lặp lại vô tận
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Lỗi phát nhạc: {e}")

def show_loading_screen():
    start_time = pygame.time.get_ticks()
    loading_duration = 3000
    
    # [MỚI] Bắt đầu bằng nhạc Menu
    play_bg_music(MENU_MUSIC_PATH)
    # Cập nhật volume ban đầu
    try: pygame.mixer.music.set_volume(1.0)
    except: pass

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

        if event.type == pygame.USEREVENT + 1:
            pygame.mixer.music.unpause() 

        # --- XỬ LÝ MENU ---
        if menu.is_active:
            menu.high_score_data = game.all_high_scores
            menu.handle_input(event, game)
            
            # [LOGIC CHUYỂN CẢNH] MENU -> GAME
            if not menu.is_active:
                is_paused = False
                game.start_countdown()
                # [MỚI] Chuyển sang nhạc Game
                play_bg_music(GAME_MUSIC_PATH)
                # Cập nhật lại volume theo biến volume hiện tại trong menu
                menu.update_volume()
        
        # --- XỬ LÝ GAMEPLAY ---
        else:
            if event.type == SCREEN_UPDATE:
                if game.game_running and not is_paused:
                    game.update() 
                    
                    new_delay = max(100, initial_speed - (game.score * 2))
                    if new_delay != current_delay:
                        current_delay = new_delay
                        pygame.time.set_timer(SCREEN_UPDATE, new_delay)

            # Xử lý phím ESC và Chuột
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if not menu.show_high_score and not menu.show_settings:
                    # [LOGIC CHUYỂN CẢNH] GAME -> MENU
                    stop_all_sfx()
                    menu.is_active = True
                    is_paused = True
                    # [MỚI] Chuyển về nhạc Menu
                    play_bg_music(MENU_MUSIC_PATH)
                    # Cập nhật lại volume
                    menu.update_volume()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if game.pause_button_rect and game.pause_button_rect.collidepoint(mouse_pos):
                    is_paused = not is_paused
                    if not is_paused: game.start_countdown()
                elif game.back_button_rect and game.back_button_rect.collidepoint(mouse_pos):
                    # [LOGIC CHUYỂN CẢNH] GAME -> MENU (Bằng chuột)
                    stop_all_sfx()
                    menu.is_active = True; is_paused = True
                    # [MỚI] Chuyển về nhạc Menu
                    play_bg_music(MENU_MUSIC_PATH)
                    menu.update_volume()

            # Xử lý điều khiển rắn
            if event.type == pygame.KEYDOWN and not is_paused:
                if game.game_running and not game.countdown_active:
                   if game.snake.can_move:
                        # Lên: Mũi tên Lên HOẶC phím W
                        if (event.key == pygame.K_UP or event.key == pygame.K_w) and game.snake.direction.y != 1:
                            game.snake.direction = Vector2(0, -1)
                            game.snake.can_move = False
                        
                        # Xuống: Mũi tên Xuống HOẶC phím S
                        elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and game.snake.direction.y != -1:
                            game.snake.direction = Vector2(0, 1)
                            game.snake.can_move = False
                        
                        # Trái: Mũi tên Trái HOẶC phím A
                        elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and game.snake.direction.x != 1:
                            game.snake.direction = Vector2(-1, 0)
                            game.snake.can_move = False
                        
                        # Phải: Mũi tên Phải HOẶC phím D
                        elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and game.snake.direction.x != -1:
                            game.snake.direction = Vector2(1, 0)
                            game.snake.can_move = False

                elif event.key == pygame.K_SPACE and not game.game_running:
                    game.reset_game(); game.start_countdown()
                    current_delay = initial_speed
                    pygame.time.set_timer(SCREEN_UPDATE, current_delay)

                elif event.key == pygame.K_SPACE and not game.game_running:
                    game.reset_game(); game.start_countdown()
                    current_delay = initial_speed
                    pygame.time.set_timer(SCREEN_UPDATE, current_delay)
                    
                    # [MỚI] Khi chơi lại (Reset), đảm bảo nhạc Game đang chạy
                    # (Phòng trường hợp nhạc Game Over làm ngắt quãng)
                    if not pygame.mixer.music.get_busy():
                        play_bg_music(GAME_MUSIC_PATH)
                        menu.update_volume()


    # Vẽ màn hình
    if menu.is_active:
        menu.draw_with_game_data(game.snake.skin_id)
    else:
        game.draw_elements(screen, is_paused)
        pygame.display.update()

    clock.tick(60)