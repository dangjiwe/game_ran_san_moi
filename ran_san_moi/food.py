import random
from pygame.math import Vector2
import pygame
from constants import cell_size, number_of_cells, OFFSET, food_surface, screen

class Food:
    def __init__(self, snake_body):
        # Tạo danh sách cố định chứa tọa độ tất cả các ô trên bản đồ
        self.all_cells = set()
        for x in range(number_of_cells):
            for y in range(number_of_cells):
                self.all_cells.add((x, y))
        
        self.position = self.generate_random_pos(snake_body)

    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, 
                                OFFSET + self.position.y * cell_size, 
                                cell_size, cell_size)
        screen.blit(food_surface, food_rect)

    def generate_random_pos(self, snake_body):
        # Tạo tập hợp các ô rắn đang nằm đè lên
        # Cần ép kiểu Vector2 về tuple (x, y) vì set không chứa được Vector2
        occupied_cells = set((int(block.x), int(block.y)) for block in snake_body)
        
        # Phép toán hiệu của tập hợp: Lấy (Tất cả ô) TRỪ ĐI (Ô rắn đang đứng)
        free_cells = list(self.all_cells - occupied_cells)
        
        if not free_cells:
            # Trường hợp thắng game (kín màn hình), tạm thời trả về vị trí ẩn
            return Vector2(-1, -1) 
            
        # Chọn ngẫu nhiên 1 ô trong số các ô trống
        x, y = random.choice(free_cells)
        return Vector2(x, y)