import pygame
import sys
from menu_renderer import MenuRenderer  # Import class vẽ mới

class Menu:
    def __init__(self, high_score_data):
        self.is_active = True
        self.selected_index = 0
        self.high_score_data = high_score_data 
        
        # Danh sách các mục
        self.options = ["CHƠI MỚI", "CHƠI TIẾP", "ĐIỂM CAO", "HƯỚNG DẪN", "CÀI ĐẶT", "THOÁT"]
        self.option_rects = [] 
        
        # Biến cờ màn hình phụ
        self.show_high_score = False 
        self.show_settings = False
        self.show_tutorial = False
        
        # Khởi tạo bộ vẽ (Renderer)
        self.renderer = MenuRenderer()

    def handle_input(self, event, game_object):
        # 1. XỬ LÝ KHI Ở MÀN HÌNH PHỤ
        if self.show_high_score or self.show_settings or self.show_tutorial:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.show_high_score = False
                self.show_settings = False
                self.show_tutorial = False
            return

        # 2. XỬ LÝ MENU CHÍNH
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
                      self.selected_index = index
                      break

    def execute_option(self, game_object):
        sel = self.options[self.selected_index]
        if sel == "CHƠI MỚI":
            game_object.reset_game() 
            self.is_active = False
        elif sel == "CHƠI TIẾP":
            self.is_active = False
        elif sel == "ĐIỂM CAO":
            self.show_high_score = True
        elif sel == "HƯỚNG DẪN":
            self.show_tutorial = True
        elif sel == "CÀI ĐẶT":
            self.show_settings = True
        elif sel == "THOÁT":
            pygame.quit(); sys.exit()

    def draw(self):
        # Điều hướng việc vẽ sang cho Renderer
        if self.show_high_score:
            self.renderer.draw_sub_screen("ĐIỂM CAO", str(self.high_score_data))
        elif self.show_settings:
            self.renderer.draw_sub_screen("CÀI ĐẶT", "Tính năng đang phát triển")
        elif self.show_tutorial:
            self.renderer.draw_tutorial_screen()
        else:
            # Vẽ menu chính và nhận lại danh sách khung nút (rects) để check chuột
            self.option_rects = self.renderer.draw_main_menu(self.selected_index, self.options)