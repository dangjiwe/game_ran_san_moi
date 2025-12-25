import pygame
from constants import (
    screen, font, screen_width, screen_height, 
    OFFSET, cell_size, number_of_cells, 
    BLACK, DARK_GREEN, GRASS_LIGHT, GRASS_DARK, BORDER_COLOR, WALL_COLOR, WALL_BORDER_COLOR, bg_surface
)

class GameRenderer:
    def __init__(self):
        # 1. TỐI ƯU FONT: Tải font to cho countdown 1 lần duy nhất ở đây
        try:
            # Lấy đường dẫn file font từ đối tượng font gốc (nếu có) hoặc dùng mặc định
            self.big_font = pygame.font.Font(None, 150) 
            # Nếu bạn muốn dùng đúng font game, hãy hardcode đường dẫn font ở đây
            # self.big_font = pygame.font.Font("Resources/font_game.ttf", 150)
        except:
            self.big_font = pygame.font.SysFont('Arial', 150)

        # 2. TỐI ƯU VẼ NỀN (Pre-render):
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
    
    def draw_wall(sefl, walls):
        for wall in walls:
            x = OFFSET + wall.x * cell_size
            y = OFFSET + wall.y * cell_size
            rect = pygame.Rect(x, y, cell_size, cell_size)

            pygame.draw.rect(screen, WALL_COLOR, rect)
            pygame.draw.rect(screen,WALL_BORDER_COLOR, rect, 3)

    def draw_button(self, text, x_offset, y_pos):
        text_surf = font.render(text, True, BLACK)
        button_w = text_surf.get_width() + 30
        button_h = text_surf.get_height() + 20
        rect = pygame.Rect(x_offset, y_pos, button_w, button_h)
        pygame.draw.rect(screen, (200, 200, 200), rect, 0, 8) 
        pygame.draw.rect(screen, BLACK, rect, 2, 8)
        screen.blit(text_surf, text_surf.get_rect(center=rect.center))
        return rect

    def draw_score(self, current_score, high_score):
        s_surf = font.render(f"ĐIỂM: {current_score}", True, DARK_GREEN)
        screen.blit(s_surf, (screen_width - OFFSET - s_surf.get_width(), OFFSET - 50))
        
        h_surf = font.render(f"ĐIỂM CAO NHẤT: {high_score}", True, DARK_GREEN)
        screen.blit(h_surf, (OFFSET, OFFSET - 50))

    def draw_countdown(self, value):
        txt = str(value)
        # Sử dụng font đã tải sẵn trong __init__, không tải lại nữa
        surf = self.big_font.render(txt, True, (255, 255, 255))
        outline = self.big_font.render(txt, True, BLACK)
        
        rect = surf.get_rect(center=(screen_width//2, screen_height//2))
        screen.blit(outline, (rect.x+3, rect.y+3)) # Bóng dày hơn chút (3px)
        screen.blit(surf, rect)

    def draw_paused_msg(self):
        surf = font.render("TẠM DỪNG", True, (0, 0, 255))
        grid_center = (OFFSET + (cell_size * number_of_cells)//2)
        screen.blit(surf, surf.get_rect(center=(grid_center, grid_center)))

    def draw_game_over(self):
        l1 = font.render("GAME OVER!", True, (255, 0, 0))
        l2 = font.render("Nhấn SPACE để chơi lại.", True, DARK_GREEN)
        cy = screen_height // 2
        screen.blit(l1, l1.get_rect(center=(screen_width//2, cy - 30)))
        screen.blit(l2, l2.get_rect(center=(screen_width//2, cy + 30)))