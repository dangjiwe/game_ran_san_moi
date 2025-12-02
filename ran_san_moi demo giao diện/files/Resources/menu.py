# files/Resources/menu.py

import pygame
import sys

# Import các tài nguyên từ constants.py (cùng thư mục Resources)
from constants import screen, screen_width, screen_height, font, DARK_GREEN, GRASS_LIGHT, BLACK, menu_bg_surface

class Menu:
    def __init__(self, high_score_data):
        self.is_active = True
        self.selected_index = 0
        self.high_score_data = high_score_data 
        
        # --- 1. THÊM MỤC "HƯỚNG DẪN" VÀO DANH SÁCH ---
        self.options = ["CHƠI MỚI", "CHƠI TIẾP", "ĐIỂM CAO", "HƯỚNG DẪN", "CÀI ĐẶT", "THOÁT"]
        
        self.option_rects = []
        
        # Các biến cờ để bật/tắt màn hình con
        self.show_high_score = False 
        self.show_settings = False
        self.show_tutorial = False  # <--- Biến mới cho màn hình hướng dẫn

    def handle_input(self, event, game_object):
        # A. XỬ LÝ KHI ĐANG Ở MÀN HÌNH CON
        if self.show_high_score or self.show_settings or self.show_tutorial:
            # Nhấn ESC để quay lại Menu chính
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.show_high_score = False
                self.show_settings = False
                self.show_tutorial = False
            return

        # B. XỬ LÝ KHI ĐANG Ở MENU CHÍNH
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
        elif sel == "HƯỚNG DẪN":      # <--- Xử lý chọn Hướng dẫn
            self.show_tutorial = True
        elif sel == "CÀI ĐẶT":
            self.show_settings = True
        elif sel == "THOÁT":
            pygame.quit(); sys.exit()

    def draw(self):
        # Vẽ nền Menu (Ảnh hoặc Màu)
        if menu_bg_surface:
            screen.blit(menu_bg_surface, (0, 0))
        else:
            screen.fill(GRASS_LIGHT)

        # Kiểm tra xem có đang mở màn hình con nào không
        if self.show_high_score: return self.draw_sub_screen("ĐIỂM CAO", str(self.high_score_data))
        if self.show_settings: return self.draw_sub_screen("CÀI ĐẶT", "Tính năng đang phát triển")
        if self.show_tutorial: return self.draw_tutorial_screen() # <--- Vẽ màn hình Hướng dẫn

        # --- VẼ MENU CHÍNH ---
        title = font.render("RẮN SĂN MỒI", True, BLACK)
        screen.blit(title, title.get_rect(center=(screen_width//2, screen_height//6)))

        self.option_rects = []
        # Tính toán vị trí để các nút không bị dính nhau
        start_y = screen_height // 3 - 20 
        for i, opt in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected_index else DARK_GREEN
            surf = font.render(opt, True, color)
            rect = surf.get_rect(center=(screen_width//2, start_y + i * 50))
            screen.blit(surf, rect)
            self.option_rects.append(rect)
        pygame.display.update()

    # Hàm vẽ các màn hình phụ đơn giản (Điểm cao, Cài đặt)
    def draw_sub_screen(self, title, msg):
        if menu_bg_surface: screen.blit(menu_bg_surface, (0,0))
        else: screen.fill(GRASS_LIGHT)

        # Khung mờ nền trắng
        s = pygame.Surface((screen_width - 100, screen_height - 100))
        s.set_alpha(200)
        s.fill((255, 255, 255))
        screen.blit(s, (50, 50))

        t_surf = font.render(title, True, BLACK)
        m_surf = font.render(msg, True, (255, 0, 0))
        es = font.render("Nhấn ESC để quay lại", True, DARK_GREEN)
        
        screen.blit(t_surf, t_surf.get_rect(center=(screen_width//2, screen_height//4)))
        screen.blit(m_surf, m_surf.get_rect(center=(screen_width//2, screen_height//2)))
        screen.blit(es, es.get_rect(center=(screen_width//2, screen_height*3/4)))
        pygame.display.update()

    # --- 2. HÀM VẼ GIAO DIỆN HƯỚNG DẪN CHI TIẾT ---
    def draw_tutorial_screen(self):
        # Vẽ nền lại cho đẹp
        if menu_bg_surface: screen.blit(menu_bg_surface, (0,0))
        else: screen.fill(GRASS_LIGHT)
        
        # Vẽ một khung trắng mờ to để chứa chữ
        overlay = pygame.Surface((screen_width - 40, screen_height - 40))
        overlay.set_alpha(230) # Độ trong suốt (0-255, càng cao càng đục)
        overlay.fill((255, 255, 255))
        screen.blit(overlay, (20, 20))

        # Tiêu đề
        title = font.render("HƯỚNG DẪN CHƠI", True, (255, 0, 0))
        screen.blit(title, title.get_rect(center=(screen_width//2, 70)))
        
        # Danh sách các dòng hướng dẫn
        lines = [
            "1. Dùng 4 phím MŨI TÊN để di chuyển.",
            "2. Ăn mồi để ghi điểm và lớn lên.",
            "3. Không được đâm vào tường.",
            "4. Không được đâm vào thân mình.",
            "5. Nhấn SPACE để chơi lại khi thua.",
            "6. Nhấn ESC để Tạm dừng / Quay lại."
        ]
        
        # Vòng lặp vẽ từng dòng chữ
        start_y = 130
        for line in lines:
            # Render chữ
            line_surf = font.render(line, True, BLACK)
            
            # Tự động thu nhỏ chữ nếu màn hình quá bé (phòng hờ)
            if line_surf.get_width() > screen_width - 60:
                scaled_w = screen_width - 60
                scaled_h = int(line_surf.get_height() * (scaled_w / line_surf.get_width()))
                line_surf = pygame.transform.scale(line_surf, (scaled_w, scaled_h))
            
            # Vẽ chữ lùi vào lề trái 40px
            screen.blit(line_surf, (40, start_y))
            start_y += 50 # Khoảng cách xuống dòng

        # Dòng nhắc nhở thoát
        esc = font.render("Nhấn ESC để quay lại", True, DARK_GREEN)
        screen.blit(esc, esc.get_rect(center=(screen_width//2, screen_height - 50)))
        
        pygame.display.update()