import pygame
# Import trực tiếp từ constants vì nằm cùng thư mục
from constants import (
    screen, font, screen_width, screen_height, 
    OFFSET, cell_size, number_of_cells, 
    BLACK, DARK_GREEN, GRASS_LIGHT, GRASS_DARK, BORDER_COLOR, bg_surface
)

class GameRenderer:
    def __init__(self):
        pass

    def draw_grass(self):
        if bg_surface:
             screen.blit(bg_surface, (0, 0))
        else:
            screen.fill(BORDER_COLOR)
            for row in range(number_of_cells):
                for col in range(number_of_cells):
                    x = OFFSET + col * cell_size
                    y = OFFSET + row * cell_size
                    rect = pygame.Rect(x, y, cell_size, cell_size)
                    if (row + col) % 2 == 0:
                        pygame.draw.rect(screen, GRASS_LIGHT, rect)
                    else:
                        pygame.draw.rect(screen, GRASS_DARK, rect)

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
        try: 
            big_font = pygame.font.Font(font, 150) 
        except: 
            big_font = pygame.font.SysFont('Arial', 150)
            
        surf = big_font.render(txt, True, (255, 255, 255))
        outline = big_font.render(txt, True, BLACK)
        rect = surf.get_rect(center=(screen_width//2, screen_height//2))
        screen.blit(outline, (rect.x+2, rect.y+2))
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