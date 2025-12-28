#food.py
import random
from pygame.math import Vector2
import pygame
from constants import *

class Food:
    def __init__(self, snake_body, walls=[]):
        self.walls = walls
        # Tạo danh sách cố định chứa tọa độ tất cả các ô trên bản đồ
        self.all_cells = set()
        for x in range(number_of_cells):
            for y in range(number_of_cells):
                self.all_cells.add((x, y))
        
# [THÊM 1] Khai báo biến đếm và cờ đặc biệt
        self.eat_counter = 0  # Đếm xem đã spawn bao nhiêu con mồi
        self.is_special = False  # Cờ mồi đặc biệt

        self.position = self.generate_random_pos(snake_body)

    def draw(self, screen):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, 
                                OFFSET + self.position.y * cell_size, 
                                cell_size, cell_size)
        # Logic vẽ
        if self.is_special:
            # Import biến ảnh special_food_surface từ constants hoặc vẽ màu đỏ nếu chưa có ảnh
            from constants import special_food_surface 
            if special_food_surface:
                screen.blit(special_food_surface, food_rect)
            else:
                pygame.draw.rect(screen, (255, 0, 0), food_rect) 
        else:
            from constants import food_surface # Import tại chỗ hoặc đầu file đều được
            screen.blit(food_surface, food_rect)

    def generate_random_pos(self, snake_body):
        # [THÊM 2] Logic đếm 5 lần thường ra 1 lần xịn
        # Hàm này chạy MỖI KHI TẠO MỒI MỚI (bao gồm cả lần đầu tiên)
        
        if self.eat_counter >= 5:
            # Nếu bộ đếm đã đủ 5 -> Ra mồi xịn
            self.is_special = True
            self.eat_counter = 0 # Reset bộ đếm về 0 để bắt đầu vòng lặp mới
        else:
            # Chưa đủ 5 -> Ra mồi thường
            self.is_special = False
            self.eat_counter += 1 # Tăng bộ đếm lên
        occupied_by_snake = set((int(block.x), int(block.y)) for block in snake_body)
        occupied_by_walls = set((int(w.x), int(w.y)) for w in self.walls)
        # Tạo tập hợp các ô rắn đang nằm đè lên
        # Cần ép kiểu Vector2 về tuple (x, y) vì set không chứa được Vector2
        #occupied_cells = set((int(block.x), int(block.y)) for block in snake_body)
        all_occupied = occupied_by_snake.union(occupied_by_walls)
        # Phép toán hiệu của tập hợp: Lấy (Tất cả ô) TRỪ ĐI (Ô rắn đang đứng)
        free_cells = list(self.all_cells - all_occupied)
        
        if not free_cells:
            # Trường hợp thắng game (kín màn hình), tạm thời trả về vị trí ẩn
            return Vector2(-1, -1) 


        # Chọn ngẫu nhiên 1 ô trong số các ô trống
        x, y = random.choice(free_cells)
        return Vector2(x, y)