# files/Resources/menu.py

import pygame
import sys
from constants import screen, screen_width, screen_height, font, DARK_GREEN, GREEN, BLACK

class Menu:
    def __init__(self, high_score_data):
        self.is_active = True
        self.selected_index = 0
        self.high_score_data = high_score_data 
        self.options = ["CHƠI MỚI", "CHƠI TIẾP", "ĐIỂM CAO", "CÀI ĐẶT", "THOÁT"]
        self.option_rects = []
        self.show_high_score = False 
        self.show_settings = False

    def handle_input(self, event, game_object):
        if self.show_high_score or self.show_settings:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.show_high_score = False
                self.show_settings = False
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                self.execute_option(game_object)
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for index, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    self.selected_index = index 
                    self.execute_option(game_object)
                    break
        
        elif event.type == pygame.MOUSEMOTION:
            for index, rect in enumerate(self.option_rects):
                 if rect.collidepoint(event.pos):
                     self.selected_index = index; break

    def execute_option(self, game_object):
        sel = self.options[self.selected_index]
        if sel == "CHƠI MỚI":
            game_object.reset_game() 
            self.is_active = False
        elif sel == "CHƠI TIẾP":
            self.is_active = False
        elif sel == "ĐIỂM CAO":
            self.show_high_score = True
        elif sel == "CÀI ĐẶT":
            self.show_settings = True
        elif sel == "THOÁT":
            pygame.quit(); sys.exit()

    def draw(self):
        screen.fill(GREEN)
        if self.show_high_score: return self.draw_sub_screen("ĐIỂM CAO", str(self.high_score_data))
        if self.show_settings: return self.draw_sub_screen("CÀI ĐẶT", "Tính năng đang phát triển")

        title = font.render("RẮN SĂN MỒI", True, BLACK)
        screen.blit(title, title.get_rect(center=(screen_width//2, screen_height//6)))

        self.option_rects = []
        start_y = screen_height // 3
        for i, opt in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected_index else DARK_GREEN
            surf = font.render(opt, True, color)
            rect = surf.get_rect(center=(screen_width//2, start_y + i * 50))
            screen.blit(surf, rect)
            self.option_rects.append(rect)
        pygame.display.update()

    def draw_sub_screen(self, title, msg):
        t_surf = font.render(title, True, BLACK)
        m_surf = font.render(msg, True, (255, 0, 0))
        esc = font.render("Nhấn ESC để quay lại", True, DARK_GREEN)
        screen.blit(t_surf, t_surf.get_rect(center=(screen_width//2, screen_height//4)))
        screen.blit(m_surf, m_surf.get_rect(center=(screen_width//2, screen_height//2)))
        screen.blit(esc, esc.get_rect(center=(screen_width//2, screen_height*3/4)))
        pygame.display.update()