import pygame
import os
from constants import (
    screen, font, screen_width, screen_height, 
    OFFSET, cell_size, number_of_cells, 
    BLACK, DARK_GREEN, GRASS_LIGHT, GRASS_DARK, BORDER_COLOR, WALL_COLOR, WALL_BORDER_COLOR, bg_surface
)

class GameRenderer:
    def __init__(self):
        # --- 1. TẢI FONT TO (Dùng cho Countdown) ---
        try:
            # Tự động tìm đường dẫn đến file font trong thư mục Resources/fonts
            base_dir = os.path.dirname(os.path.abspath(__file__))
            font_path = os.path.join(base_dir, "Resources", "fonts", "font_game.ttf")
            
            # Kiểm tra xem file có tồn tại không trước khi load
            if os.path.exists(font_path):
                self.big_font = pygame.font.Font(font_path, 150)
            else:
                # Nếu không thấy file font_game.ttf thì dùng font mặc định
                print("Không tìm thấy font_game.ttf -> Dùng font hệ thống")
                self.big_font = pygame.font.SysFont('Arial', 150, bold=True)
        except Exception as e:
            print(f"Lỗi tải font to: {e} -> Dùng font mặc định")
            self.big_font = pygame.font.SysFont('Arial', 150, bold=True)

        # --- 2. TỐI ƯU VẼ NỀN (Pre-render) ---
        # Tạo sẵn một bề mặt chứa hình ảnh bàn cờ để không phải vẽ 400 ô mỗi frame
        self.pre_rendered_grass = pygame.Surface((cell_size * number_of_cells, cell_size * number_of_cells))
        self.pre_rendered_grass.fill(GRASS_LIGHT)
        
        for row in range(number_of_cells):
            for col in range(number_of_cells):
                if (row + col) % 2 != 0: # Chỉ vẽ ô tối màu đè lên nền sáng
                    x = col * cell_size
                    y = row * cell_size
                    rect = pygame.Rect(x, y, cell_size, cell_size)
                    pygame.draw.rect(self.pre_rendered_grass, GRASS_DARK, rect)

    def draw_grass(self):
        # Vẽ viền ngoài
        screen.fill(BORDER_COLOR)
        
        # Vẽ nội dung bàn cờ
        if bg_surface:
             screen.blit(bg_surface, (0, 0))
        else:
            # Thay vì vòng lặp for lồng nhau, giờ chỉ cần blit 1 tấm ảnh đã vẽ sẵn
            screen.blit(self.pre_rendered_grass, (OFFSET, OFFSET))
    
    def draw_wall(self, walls):
        for wall in walls:
            x = OFFSET + wall.x * cell_size
            y = OFFSET + wall.y * cell_size
            rect = pygame.Rect(x, y, cell_size, cell_size)

            pygame.draw.rect(screen, WALL_COLOR, rect)
            pygame.draw.rect(screen, WALL_BORDER_COLOR, rect, 3)

    def draw_button(self, text, x_offset, y_pos):
        text_surf = font.render(text, True, BLACK)
        button_w = text_surf.get_width() + 30
        button_h = text_surf.get_height() + 20
        rect = pygame.Rect(x_offset, y_pos, button_w, button_h)
        
        pygame.draw.rect(screen, (200, 200, 200), rect, 0, 8) 
        pygame.draw.rect(screen, BLACK, rect, 2, 8)
        screen.blit(text_surf, text_surf.get_rect(center=rect.center))
        return rect

    def draw_score(self, current_score, high_score, is_new_record=False):
        # 1. Vẽ điểm hiện tại (Bên phải)
        s_surf = font.render(f"ĐIỂM: {current_score}", True, DARK_GREEN)
        screen.blit(s_surf, (screen_width - OFFSET - s_surf.get_width(), OFFSET - 50))
        
        # 2. Vẽ Điểm cao / Kỷ lục mới (Bên trái)
        if not is_new_record:
            txt_str = f"ĐIỂM CAO NHẤT: {high_score}"
            color = DARK_GREEN
        else:
            txt_str = f"KỶ LỤC MỚI: {high_score}"
            # Hiệu ứng nhấp nháy
            current_time = pygame.time.get_ticks()
            if (current_time // 200) % 2 == 0:
                color = (255, 0, 0)     # Màu Đỏ
            else:
                color = (255, 215, 0)   # Màu Vàng Gold

        h_surf = font.render(txt_str, True, color)
        screen.blit(h_surf, (OFFSET, OFFSET - 50))

    def draw_countdown(self, value):
        txt = str(value)
        # Sử dụng self.big_font đã được khởi tạo an toàn trong __init__
        surf = self.big_font.render(txt, True, (255, 255, 255))
        outline = self.big_font.render(txt, True, BLACK)
        
        rect = surf.get_rect(center=(screen_width//2, screen_height//2))
        screen.blit(outline, (rect.x+3, rect.y+3)) 
        screen.blit(surf, rect)

    def draw_paused_msg(self):
        surf = font.render("TẠM DỪNG", True, (0, 0, 255))
        grid_center = (OFFSET + (cell_size * number_of_cells)//2)
        screen.blit(surf, surf.get_rect(center=(grid_center, grid_center)))

    def draw_game_over(self, score):
        try:
             # Cố gắng load font từ file resources nếu có để đồng bộ
             # (Dùng logic tìm file như trên hoặc dùng font hệ thống cho nhanh)
             font_big = pygame.font.SysFont('Arial', 60, bold=True)
        except:
             font_big = pygame.font.SysFont('Arial', 60, bold=True)

        l1 = font_big.render("GAME OVER!", True, (255, 0, 0))
        l_score = font.render(f"ĐIỂM CỦA BẠN: {score}", True, (0, 0, 255)) 
        l2 = font.render("Nhấn SPACE để chơi lại.", True, DARK_GREEN)
        l3 = font.render("Nhấn ESC để về Menu", True, (0, 0, 0))
        
        cy = screen_height // 2
        
        screen.blit(l1, l1.get_rect(center=(screen_width//2, cy - 120))) 
        screen.blit(l_score, l_score.get_rect(center=(screen_width//2, cy - 40)))
        
        screen.blit(l2, l2.get_rect(center=(screen_width//2, cy + 50)))  
        screen.blit(l3, l3.get_rect(center=(screen_width//2, cy + 120))) 