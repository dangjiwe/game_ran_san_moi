import random
import pygame
import math 
from pygame.math import Vector2
from constants import cell_size, number_of_cells, OFFSET

class Food:
    def __init__(self, snake_body, walls=[]):
        self.walls = walls
        
        self.all_cells = set()
        for x in range(number_of_cells):
            for y in range(number_of_cells):
                self.all_cells.add((x, y))
        
        self.special_position = None         
        self.position = self.generate_random_pos(snake_body)
        self.eat_counter = 0

    def draw(self, screen):
        # --- 1. VẼ MỒI THƯỜNG (QUẢ TÁO ĐỎ 3D) ---
        if self.position:
            # Tính tọa độ tâm và bán kính
            cx = OFFSET + self.position.x * cell_size + cell_size // 2
            cy = OFFSET + self.position.y * cell_size + cell_size // 2
            radius = cell_size // 2 - 2

            # A. Bóng đổ (Shadow) - Vẽ lệch xuống dưới một chút
            pygame.draw.circle(screen, (100, 0, 0), (cx, cy + 2), radius)

            # B. Thân táo (Màu đỏ tươi)
            pygame.draw.circle(screen, (220, 20, 60), (cx, cy), radius)

            # C. Điểm phản quang (Highlight) - Chấm trắng lệch góc
            # Giúp quả táo trông bóng bẩy, căng mọng
            highlight_radius = radius // 3
            pygame.draw.circle(screen, (255, 150, 150), (cx - radius//3, cy - radius//3), highlight_radius)

            # D. Cuống táo (Màu nâu)
            stem_w = 4
            stem_h = 6
            stem_rect = pygame.Rect(cx - stem_w//2, cy - radius - 3, stem_w, stem_h)
            pygame.draw.rect(screen, (101, 67, 33), stem_rect)

        # --- 2. VẼ MỒI ĐẶC BIỆT (RUBY LẤP LÁNH) ---
        if self.special_position:
            cx = OFFSET + self.special_position.x * cell_size + cell_size // 2
            cy = OFFSET + self.special_position.y * cell_size + cell_size // 2

            # Hiệu ứng nhịp tim (Pulsing)
            current_time = pygame.time.get_ticks()
            pulse = 1 + 0.15 * math.sin(current_time * 0.01) 
            radius = (cell_size // 2) * pulse

            # Hào quang
            pygame.draw.circle(screen, (255, 223, 0), (cx, cy), radius + 4, width=1) 
            pygame.draw.circle(screen, (255, 215, 0), (cx, cy), radius + 2, width=2)

            # Hình thoi (Diamond)
            size = radius
            points = [
                (cx, cy - size), # Đỉnh
                (cx + size, cy), # Phải
                (cx, cy + size), # Đáy
                (cx - size, cy)  # Trái
            ]
            
            # Nền đỏ đậm
            pygame.draw.polygon(screen, (220, 20, 60), points) 
            # Viền vàng
            pygame.draw.polygon(screen, (255, 215, 0), points, width=2)
            # Điểm sáng
            pygame.draw.circle(screen, (255, 255, 255), (cx - size * 0.3, cy - size * 0.3), size * 0.25)

    def generate_random_pos(self, snake_body):
        """Sinh vị trí cho mồi thường"""
        occupied = set((int(b.x), int(b.y)) for b in snake_body)
        occupied = occupied.union(set((int(w.x), int(w.y)) for w in self.walls))
        
        if self.special_position:
            occupied.add((int(self.special_position.x), int(self.special_position.y)))

        free_cells = list(self.all_cells - occupied)
        if not free_cells: return Vector2(-1, -1)
        x, y = random.choice(free_cells)
        return Vector2(x, y)

    def spawn_special_food(self, snake_body):
        """Sinh vị trí cho mồi đặc biệt"""
        occupied = set((int(b.x), int(b.y)) for b in snake_body)
        occupied = occupied.union(set((int(w.x), int(w.y)) for w in self.walls))
        occupied.add((int(self.position.x), int(self.position.y)))

        free_cells = list(self.all_cells - occupied)
        if free_cells:
            x, y = random.choice(free_cells)
            self.special_position = Vector2(x, y)
        else:
            self.special_position = None