import pygame
import sys
from pygame.math import Vector2

pygame.init()
pygame.mixer.init()

from game import Game
from menu import Menu
from constants import *
'''(
    SCREEN_UPDATE, MUSIC_LOADED, screen, font, 
    screen_width, screen_height, GRASS_LIGHT, loading_bg_surface
)'''
import sys
# Ép buộc Python in ra mã UTF-8 để hiển thị được tiếng Việt
sys.stdout.reconfigure(encoding='utf-8')
pygame.time.set_timer(SCREEN_UPDATE, 150)
clock = pygame.time.Clock()

def show_loading_screen():
    start_time = pygame.time.get_ticks()
    loading_duration = 3000
    
    if MUSIC_LOADED:
        try:
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    while pygame.time.get_ticks() - start_time < loading_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if loading_bg_surface:
            screen.blit(loading_bg_surface, (0, 0))
        else:
            screen.fill(GRASS_LIGHT)
        
        text_str = "ĐANG TẢI TÀI NGUYÊN..."
        
        shadow_surf = font.render(text_str, True, (50, 50, 50))
        shadow_rect = shadow_surf.get_rect(center=(screen_width // 2 + 2, screen_height // 2 + 2))
        screen.blit(shadow_surf, shadow_rect)
        
        text_surf = font.render(text_str, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text_surf, text_rect)
        
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

        if menu.is_active:
            menu.high_score_data = game.high_score
            menu.handle_input(event, game)
            if not menu.is_active:
                is_paused = False
                game.start_countdown()

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if not menu.show_high_score and not menu.show_settings:
                    menu.is_active = True
                    is_paused = True
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if game.pause_button_rect and game.pause_button_rect.collidepoint(mouse_pos):
                    is_paused = not is_paused
                    if not is_paused:
                        game.start_countdown()
                
                elif game.back_button_rect and game.back_button_rect.collidepoint(mouse_pos):
                    menu.is_active = True
                    is_paused = True

            if event.type == SCREEN_UPDATE:
                if game.game_running and not is_paused:
                    game.update()
            # Tính điểm hiện tại
                    current_score = len(game.snake.body) - 3
                    
                    # Công thức: Tốc độ cơ bản 150ms, mỗi 1 điểm giảm 2ms (nhanh hơn). 
                    # Giới hạn nhanh nhất là 40ms (không nhanh quá kẻo không chơi nổi)
                    new_delay = max(40, 150 - (current_score * 2))
                    
                    # Cập nhật lại tốc độ game
                    pygame.time.set_timer(SCREEN_UPDATE, new_delay)
            
            if event.type == pygame.KEYDOWN and not is_paused:
                if game.game_running and not game.countdown_active:
                   if game.snake.can_move:
                        if event.key == pygame.K_UP and game.snake.direction.y != 1:
                            game.snake.direction = Vector2(0, -1)
                            game.snake.can_move = False  # Khóa lại ngay
                            
                        elif event.key == pygame.K_DOWN and game.snake.direction.y != -1:
                            game.snake.direction = Vector2(0, 1)
                            game.snake.can_move = False
                            
                        elif event.key == pygame.K_LEFT and game.snake.direction.x != 1:
                            game.snake.direction = Vector2(-1, 0)
                            game.snake.can_move = False
                            
                        elif event.key == pygame.K_RIGHT and game.snake.direction.x != -1:
                            game.snake.direction = Vector2(1, 0)
                            game.snake.can_move = False

                elif event.key == pygame.K_SPACE and not game.game_running:
                    game.reset_game()
                    game.start_countdown()

    if menu.is_active:
        menu.draw()
    else:
        game.draw_elements(is_paused)
        pygame.display.update()

    clock.tick(60)