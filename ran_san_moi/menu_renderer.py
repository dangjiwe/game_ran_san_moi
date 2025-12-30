import pygame
from constants import (
    screen, screen_width, screen_height, font, 
    DARK_GREEN, GRASS_LIGHT, BLACK, WHITE, menu_bg_surface, OFFSET, SKINS
)

class MenuRenderer:
    def __init__(self):
        pass

    def draw_background(self):
        if menu_bg_surface:
            screen.blit(menu_bg_surface, (0, 0))
        else:
            screen.fill(GRASS_LIGHT)

    def draw_button(self, text, x, y, width=300, height=60, is_selected=False, is_hovered=False, bg_color_override=None):
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (x, y)
        
        # Xác định màu sắc
        if is_selected or is_hovered:
            bg_color = (200, 230, 100) # Sáng
            text_color = BLACK
        else:
            bg_color = (60, 80, 40)    # Tối
            text_color = WHITE

        if bg_color_override:
            bg_color = bg_color_override
            
        # 1. Bóng đổ
        shadow_rect = rect.copy()
        shadow_rect.x += 5; shadow_rect.y += 5
        pygame.draw.rect(screen, (30, 30, 30), shadow_rect, border_radius=15)
        
        # 2. Thân nút
        pygame.draw.rect(screen, bg_color, rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, rect, 3, border_radius=15)
        
        # 3. Tam giác chỉ thị
        if is_selected:
             tri_points = [(rect.left-20, rect.centery-10), 
                           (rect.left-20, rect.centery+10), 
                           (rect.left-5, rect.centery)]
             pygame.draw.polygon(screen, BLACK, tri_points)
        
        # 4. Text
        if text:
            text_surf = font.render(text, True, text_color)
            # Tự động thu nhỏ chữ nếu dài hơn nút (Logic mới để tránh tràn lề)
            if text_surf.get_width() > width - 20:
                scale_factor = (width - 20) / text_surf.get_width()
                new_h = int(text_surf.get_height() * scale_factor)
                new_w = int(text_surf.get_width() * scale_factor)
                text_surf = pygame.transform.scale(text_surf, (new_w, new_h))
            
            screen.blit(text_surf, text_surf.get_rect(center=rect.center))
            
        return rect

    def draw_main_menu(self, selected_index, options, mouse_pos):
        self.draw_background()

        # Tiêu đề
        title = font.render("RẮN SĂN MỒI", True, "#e2ebff")#DARK_GREEN)
        t_shadow = font.render("RẮN SĂN MỒI", True, BLACK)
        t_rect = title.get_rect(center=(screen_width//2, screen_height//8))
        screen.blit(t_shadow, (t_rect.x+3, t_rect.y+3))
        screen.blit(title, t_rect)

        rects = []
        start_y = screen_height // 4 + 20
        
        for i, opt in enumerate(options):
            is_key_selected = (i == selected_index)
            temp_rect = pygame.Rect(0, 0, 300, 60)
            temp_rect.center = (screen_width//2, start_y + i * 70)
            is_hovered = temp_rect.collidepoint(mouse_pos)
            
            rect = self.draw_button(opt, screen_width//2, start_y + i * 70, 
                                    is_selected=is_key_selected, is_hovered=is_hovered)
            rects.append(rect)
            
        # Nút SKIN
        skin_btn_text = "SKIN"
        skin_rect_temp = pygame.Rect(OFFSET - 50, screen_height - 60 - 25, 100, 50) 
        skin_rect = self.draw_button(skin_btn_text, OFFSET, screen_height - 60, width=100, height=50, 
                                     is_hovered=skin_rect_temp.collidepoint(mouse_pos))
        
        return rects, skin_rect

    def draw_map_selection(self, selected_index, map_names, mouse_pos):
        self.draw_background()
        title = font.render("CHỌN MÀN CHƠI", True, "#ffffff")#BLACK)
        screen.blit(title, title.get_rect(center=(screen_width//2, 80)))
        
        rects = []
        start_y = 150
        col_1_x = screen_width // 4 + 20
        col_2_x = screen_width * 3 // 4 - 20
        
        for i, name in enumerate(map_names):
            is_selected = (i == selected_index)
            if i % 2 == 0:
                x = col_1_x; y = start_y + (i // 2) * 80
            else:
                x = col_2_x; y = start_y + (i // 2) * 80
            
            temp_rect = pygame.Rect(0, 0, 220, 60)
            temp_rect.center = (x, y)
            is_hovered = temp_rect.collidepoint(mouse_pos)
            
            rect = self.draw_button(name, x, y, width=220, height=60, 
                                    is_selected=is_selected, is_hovered=is_hovered)
            rects.append(rect)
            
        back_rect_temp = pygame.Rect(screen_width//2 - 100, screen_height - 60 - 25, 200, 50)
        back_rect = self.draw_button("QUAY LẠI", screen_width//2, screen_height - 60, width=200, height=50,
                                     is_hovered=back_rect_temp.collidepoint(mouse_pos))
        return rects, back_rect

    def draw_settings(self, volume, mouse_pos):
        s = pygame.Surface((screen_width - 80, screen_height - 80))
        s.set_alpha(220); s.fill(WHITE)
        screen.blit(s, (40, 40))
        pygame.draw.rect(screen, BLACK, (40, 40, screen_width-80, screen_height-80), 4)
        
        title = font.render("CÀI ĐẶT", True, BLACK)
        screen.blit(title, title.get_rect(center=(screen_width//2, 100)))
        vol_label = font.render("ÂM THANH", True, DARK_GREEN)
        screen.blit(vol_label, vol_label.get_rect(center=(screen_width//2, 180)))

        center_y = 250
        
        btn_down = self.draw_button("", screen_width//2 - 100, center_y, width=60, height=60)
        col_minus = BLACK if btn_down.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(screen, col_minus, (btn_down.centerx - 10, btn_down.centery - 3, 20, 6))

        btn_up = self.draw_button("", screen_width//2 + 100, center_y, width=60, height=60)
        col_plus = BLACK if btn_up.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(screen, col_plus, (btn_up.centerx - 10, btn_up.centery - 3, 20, 6))
        pygame.draw.rect(screen, col_plus, (btn_up.centerx - 3, btn_up.centery - 10, 6, 20))

        vol_percent = int(volume * 100)
        vol_text = font.render(f"{vol_percent}%", True, BLACK)
        screen.blit(vol_text, vol_text.get_rect(center=(screen_width//2, center_y)))

        back_rect_temp = pygame.Rect(screen_width//2 - 100, screen_height - 100 - 25, 200, 50)
        back_rect = self.draw_button("QUAY LẠI", screen_width//2, screen_height - 100, width=200, height=50,
                                     is_hovered=back_rect_temp.collidepoint(mouse_pos))
        return btn_down, btn_up, back_rect

    def draw_tutorial(self, mouse_pos):
        self.draw_background()
        overlay = pygame.Surface((screen_width - 40, screen_height - 40))
        overlay.set_alpha(230); overlay.fill(WHITE)
        screen.blit(overlay, (20, 20))
        pygame.draw.rect(screen, BLACK, (20, 20, screen_width-40, screen_height-40), 4)

        title = font.render("HƯỚNG DẪN CHƠI", True, (255, 0, 0))
        screen.blit(title, title.get_rect(center=(screen_width//2, 70)))
        
        lines = [
            "1. Di chuyển: Mũi tên hoặc WASD.",
            "2. Ăn Táo 1 điểm - Ruby 3 điểm.",
            "3. Không đâm vào tường.",
            "4. Không tự đâm vào thân mình.",
            "5. Nhấn SPACE để chơi lại.",
            "6. Nhấn ESC: Quay lại."
        ]
        
        start_y = 130
        for line in lines:
            line_surf = font.render(line, True, BLACK)
            
            # Thu nhỏ nếu dòng quá dài
            if line_surf.get_width() > screen_width - 60:
                scaled_w = screen_width - 60
                scaled_h = int(line_surf.get_height() * (scaled_w / line_surf.get_width()))
                line_surf = pygame.transform.scale(line_surf, (scaled_w, scaled_h))
            
            screen.blit(line_surf, (40, start_y))
            
            start_y += 50
            
        back_rect_temp = pygame.Rect(screen_width//2 - 100, screen_height - 60 - 25, 200, 50)
        back_rect = self.draw_button("QUAY LẠI", screen_width//2, screen_height - 60, width=200, height=50,
                                     is_hovered=back_rect_temp.collidepoint(mouse_pos))
        return back_rect

    def draw_high_score(self, data, mouse_pos):
        self.draw_background()
        s = pygame.Surface((screen_width - 80, screen_height - 80))
        s.set_alpha(220); s.fill(WHITE)
        screen.blit(s, (40, 40))
        pygame.draw.rect(screen, BLACK, (40, 40, screen_width-80, screen_height-80), 4)
        
        t_surf = font.render("ĐIỂM CAO", True, BLACK)
        m_surf = font.render(str(data), True, (255, 0, 0))
        
        screen.blit(t_surf, t_surf.get_rect(center=(screen_width//2, screen_height//4)))
        screen.blit(m_surf, m_surf.get_rect(center=(screen_width//2, screen_height//2)))
        
        back_rect_temp = pygame.Rect(screen_width//2 - 100, screen_height - 60 - 25, 200, 50)
        back_rect = self.draw_button("QUAY LẠI", screen_width//2, screen_height - 60, width=200, height=50,
                                     is_hovered=back_rect_temp.collidepoint(mouse_pos))
        return back_rect

    def draw_popup(self, title, msg1, msg2=""):
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(150); overlay.fill(BLACK)
        screen.blit(overlay, (0,0))
        
        box = pygame.Rect(0, 0, 500, 300)
        box.center = (screen_width//2, screen_height//2)
        pygame.draw.rect(screen, WHITE, box, border_radius=20)
        pygame.draw.rect(screen, BLACK, box, 5, border_radius=20)
        
        t_surf = font.render(title, True, (255, 0, 0))
        m1_surf = font.render(msg1, True, BLACK)
        close_surf = font.render("Nhấn phím bất kỳ để đóng", True, (100, 100, 100))
        close_surf = pygame.transform.scale(close_surf, (int(close_surf.get_width()*0.7), int(close_surf.get_height()*0.7)))

        screen.blit(t_surf, t_surf.get_rect(center=(screen_width//2, screen_height//2 - 60)))
        screen.blit(m1_surf, m1_surf.get_rect(center=(screen_width//2, screen_height//2)))
        
        if msg2:
            m2_surf = font.render(msg2, True, DARK_GREEN)
            screen.blit(m2_surf, m2_surf.get_rect(center=(screen_width//2, screen_height//2 + 50)))
            
        screen.blit(close_surf, close_surf.get_rect(center=(screen_width//2, screen_height//2 + 120)))

    # --- ĐÃ SỬA LẠI HÀM NÀY ĐỂ NÚT TO HƠN ---
    def draw_skin_shop(self, current_skin_id, mouse_pos):
        self.draw_background()
        title = font.render("CỬA HÀNG SKIN", True, BLACK)
        screen.blit(title, title.get_rect(center=(screen_width//2, 80)))

        rects = []
        
        # Tăng khoảng cách giữa 2 cột (240px thay vì 160px)
        col_spacing = 240
        start_x_offset = 120 # Một nửa của col_spacing để căn giữa
        start_y = 150
        
        for i, skin in enumerate(SKINS):
            col = i % 2
            row = i // 2
            
            # Tính tọa độ mới rộng rãi hơn
            x = screen_width // 2 - start_x_offset + col * col_spacing
            y = start_y + row * 90
            
            is_active = (i == current_skin_id)
            
            # Tăng kích thước nút từ 140 lên 220 để chứa đủ chữ
            width_btn = 220
            height_btn = 70
            
            btn_rect = self.draw_button(skin["name"], x, y, width=width_btn, height=height_btn, 
                                        bg_color_override=skin["outer"],
                                        is_hovered=pygame.Rect(x - width_btn//2, y - height_btn//2, width_btn, height_btn).collidepoint(mouse_pos))
            
            if is_active:
                pygame.draw.rect(screen, (255, 255, 0), btn_rect, 5, border_radius=15)
                
            rects.append(btn_rect)

        back_rect_temp = pygame.Rect(screen_width//2 - 100, screen_height - 60 - 25, 200, 50)
        back_rect = self.draw_button("QUAY LẠI", screen_width//2, screen_height - 60, width=200, height=50,
                                     is_hovered=back_rect_temp.collidepoint(mouse_pos))
        
        return rects, back_rect