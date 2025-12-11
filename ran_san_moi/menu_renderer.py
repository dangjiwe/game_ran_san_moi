import pygame
from constants import (
    screen, screen_width, screen_height, font, 
    DARK_GREEN, GRASS_LIGHT, BLACK, WHITE, menu_bg_surface
)

class MenuRenderer:
    def __init__(self):
        pass

    def draw_background(self):
        if menu_bg_surface:
            screen.blit(menu_bg_surface, (0, 0))
        else:
            screen.fill(GRASS_LIGHT)

    def draw_fancy_button(self, text, x, y, is_selected):
        # Màu sắc thay đổi theo trạng thái chọn
        if is_selected:
            bg_color = (200, 230, 100) # Xanh nõn chuối
            text_color = BLACK
        else:
            bg_color = (60, 80, 40)    # Xanh rêu đậm
            text_color = WHITE

        button_w = 300
        button_h = 60
        
        rect = pygame.Rect(0, 0, button_w, button_h)
        rect.center = (x, y)
        
        # 1. Vẽ bóng đổ
        shadow_rect = rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        pygame.draw.rect(screen, (30, 30, 30), shadow_rect, border_radius=15)
        
        # 2. Vẽ nền nút
        pygame.draw.rect(screen, bg_color, rect, border_radius=15)
        
        # 3. Vẽ viền nút
        pygame.draw.rect(screen, BLACK, rect, 3, border_radius=15)
        
        # 4. Vẽ mũi tên chỉ thị
        if is_selected:
             tri_points = [(rect.left - 20, rect.centery - 10),
                           (rect.left - 20, rect.centery + 10),
                           (rect.left - 5, rect.centery)]
             pygame.draw.polygon(screen, BLACK, tri_points)

        # 5. Vẽ chữ
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)
        
        return rect

    def draw_main_menu(self, selected_index, options):
        self.draw_background()

        # Tiêu đề Game
        title = font.render("RẮN SĂN MỒI", True, BLACK)
        title_shadow = font.render("RẮN SĂN MỒI", True, (200, 200, 200))
        t_rect = title.get_rect(center=(screen_width//2, screen_height//6))
        screen.blit(title_shadow, (t_rect.x+3, t_rect.y+3))
        screen.blit(title, t_rect)

        # Vẽ các nút và trả về danh sách rect để logic xử lý chuột
        rects = []
        start_y = screen_height // 3 + 20
        
        for i, opt in enumerate(options):
            is_selected = (i == selected_index)
            rect = self.draw_fancy_button(opt, screen_width//2, start_y + i * 75, is_selected)
            rects.append(rect)
            
        pygame.display.update()
        return rects

    def draw_sub_screen(self, title, msg):
        self.draw_background()
        
        # Khung nền trắng mờ
        s = pygame.Surface((screen_width - 80, screen_height - 80))
        s.set_alpha(220)
        s.fill(WHITE)
        screen.blit(s, (40, 40))
        pygame.draw.rect(screen, BLACK, (40, 40, screen_width-80, screen_height-80), 4)

        # Nội dung
        t_surf = font.render(title, True, BLACK)
        m_surf = font.render(msg, True, (255, 0, 0))
        es = font.render("Nhấn ESC để quay lại", True, DARK_GREEN)
        
        screen.blit(t_surf, t_surf.get_rect(center=(screen_width//2, screen_height//4)))
        screen.blit(m_surf, m_surf.get_rect(center=(screen_width//2, screen_height//2)))
        screen.blit(es, es.get_rect(center=(screen_width//2, screen_height*3/4)))
        pygame.display.update()

    def draw_tutorial_screen(self):
        self.draw_background()
        
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