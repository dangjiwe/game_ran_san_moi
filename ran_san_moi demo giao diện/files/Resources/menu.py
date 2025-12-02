# files/Resources/menu.py

import pygame
import sys
from constants import screen, screen_width, screen_height, font, DARK_GREEN, GRASS_LIGHT, BLACK, WHITE, menu_bg_surface

class Menu:
    def __init__(self, high_score_data):
        self.is_active = True
        self.selected_index = 0
        self.high_score_data = high_score_data 
        
        # Danh sách các mục
        self.options = ["CHƠI MỚI", "CHƠI TIẾP", "ĐIỂM CAO", "HƯỚNG DẪN", "CÀI ĐẶT", "THOÁT"]
        
        self.option_rects = [] # Chứa các hình chữ nhật để check chuột
        
        # Biến cờ màn hình phụ
        self.show_high_score = False 
        self.show_settings = False
        self.show_tutorial = False

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

    # --- HÀM VẼ NÚT ĐẸP (MỚI) ---
    def draw_fancy_button(self, text, x, y, is_selected):
        # Màu sắc thay đổi theo trạng thái chọn
        if is_selected:
            bg_color = (200, 230, 100) # Màu sáng (Xanh nõn chuối)
            text_color = BLACK
            offset = 0 # Khi chọn, nút cảm giác "nổi" lên
        else:
            bg_color = (60, 80, 40)    # Màu tối (Xanh rêu đậm)
            text_color = WHITE
            offset = 0

        # Kích thước nút
        button_w = 300
        button_h = 60
        
        # Tính toán vị trí hình chữ nhật
        # rect chính giữa
        rect = pygame.Rect(0, 0, button_w, button_h)
        rect.center = (x, y)
        
        # 1. Vẽ bóng đổ (Shadow) - Màu đen mờ lệch xuống dưới
        shadow_rect = rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        pygame.draw.rect(screen, (30, 30, 30), shadow_rect, border_radius=15)
        
        # 2. Vẽ nền nút
        pygame.draw.rect(screen, bg_color, rect, border_radius=15)
        
        # 3. Vẽ viền nút
        pygame.draw.rect(screen, BLACK, rect, 3, border_radius=15)
        
        # 4. Vẽ mũi tên chỉ thị nếu đang chọn
        if is_selected:
             # Vẽ tam giác nhỏ bên trái nút
             tri_points = [(rect.left - 20, rect.centery - 10),
                           (rect.left - 20, rect.centery + 10),
                           (rect.left - 5, rect.centery)]
             pygame.draw.polygon(screen, BLACK, tri_points)

        # 5. Vẽ chữ
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)
        
        return rect # Trả về để xử lý va chạm chuột
    # ----------------------------

    def draw(self):
        # Vẽ nền
        if menu_bg_surface:
            screen.blit(menu_bg_surface, (0, 0))
        else:
            screen.fill(GRASS_LIGHT)

        # Vẽ màn hình con nếu có
        if self.show_high_score: return self.draw_sub_screen("ĐIỂM CAO", str(self.high_score_data))
        if self.show_settings: return self.draw_sub_screen("CÀI ĐẶT", "Tính năng đang phát triển")
        if self.show_tutorial: return self.draw_tutorial_screen()

        # Tiêu đề Game
        title = font.render("RẮN SĂN MỒI", True, BLACK)
        # Vẽ bóng tiêu đề
        title_shadow = font.render("RẮN SĂN MỒI", True, (200, 200, 200))
        t_rect = title.get_rect(center=(screen_width//2, screen_height//6))
        screen.blit(title_shadow, (t_rect.x+3, t_rect.y+3))
        screen.blit(title, t_rect)

        # Vẽ Danh sách Nút
        self.option_rects = []
        start_y = screen_height // 3 + 20
        
        for i, opt in enumerate(self.options):
            is_selected = (i == self.selected_index)
            # Gọi hàm vẽ nút mới
            rect = self.draw_fancy_button(opt, screen_width//2, start_y + i * 75, is_selected)
            self.option_rects.append(rect)
            
        pygame.display.update()

    # --- CÁC HÀM VẼ MÀN HÌNH PHỤ ---
    def draw_sub_screen(self, title, msg):
        if menu_bg_surface: screen.blit(menu_bg_surface, (0,0))
        else: screen.fill(GRASS_LIGHT)
        
        # Khung nền
        s = pygame.Surface((screen_width - 80, screen_height - 80))
        s.set_alpha(220)
        s.fill(WHITE)
        screen.blit(s, (40, 40))
        
        # Viền khung
        pygame.draw.rect(screen, BLACK, (40, 40, screen_width-80, screen_height-80), 4)

        t_surf = font.render(title, True, BLACK)
        m_surf = font.render(msg, True, (255, 0, 0))
        es = font.render("Nhấn ESC để quay lại", True, DARK_GREEN)
        
        screen.blit(t_surf, t_surf.get_rect(center=(screen_width//2, screen_height//4)))
        screen.blit(m_surf, m_surf.get_rect(center=(screen_width//2, screen_height//2)))
        screen.blit(es, es.get_rect(center=(screen_width//2, screen_height*3/4)))
        pygame.display.update()

    def draw_tutorial_screen(self):
        if menu_bg_surface: screen.blit(menu_bg_surface, (0,0))
        else: screen.fill(GRASS_LIGHT)
        
        overlay = pygame.Surface((screen_width - 40, screen_height - 40))
        overlay.set_alpha(230)
        overlay.fill(WHITE)
        screen.blit(overlay, (20, 20))
        pygame.draw.rect(screen, BLACK, (20, 20, screen_width-40, screen_height-40), 4)

        title = font.render("HƯỚNG DẪN CHƠI", True, (255, 0, 0))
        screen.blit(title, title.get_rect(center=(screen_width//2, 70)))
        
        lines = [
            "1. Dùng 4 phím MŨI TÊN để di chuyển.",
            "2. Ăn mồi để ghi điểm và lớn lên.",
            "3. Không được đâm vào tường.",
            "4. Không được đâm vào thân mình.",
            "5. Nhấn SPACE để chơi lại khi thua.",
            "6. Nhấn ESC để Tạm dừng / Quay lại."
        ]
        
        start_y = 130
        for line in lines:
            line_surf = font.render(line, True, BLACK)
            if line_surf.get_width() > screen_width - 60:
                scaled_w = screen_width - 60
                scaled_h = int(line_surf.get_height() * (scaled_w / line_surf.get_width()))
                line_surf = pygame.transform.scale(line_surf, (scaled_w, scaled_h))
            screen.blit(line_surf, (40, start_y))
            start_y += 50 

        esc = font.render("Nhấn ESC để quay lại", True, DARK_GREEN)
        screen.blit(esc, esc.get_rect(center=(screen_width//2, screen_height - 50)))
        
        pygame.display.update()