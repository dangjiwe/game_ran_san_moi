import pygame
from pygame.math import Vector2
from collections import deque
from constants import cell_size, OFFSET, BLUE, HEAD_SIZE, screen, snake_head_surface

class Snake:
    def __init__(self):
        self.body = deque([Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)])
        self.direction = Vector2(1, 0)
        self.new_block = False 
        self.can_move = True  # Biến cờ cho phép nhận nút điều khiển

        self.head_surfaces = {
            (0, -1): pygame.transform.rotate(snake_head_surface, 0),
            (0, 1):  pygame.transform.rotate(snake_head_surface, 180),
            (-1, 0): pygame.transform.rotate(snake_head_surface, 90),
            (1, 0):  pygame.transform.rotate(snake_head_surface, -90)
        }

    def draw(self):
        # 1. VẼ THÂN RẮN (Body)
        # Lặp qua các đốt (bỏ đốt đầu tiên là đầu rắn)
        for index, segment in enumerate(list(self.body)[1:]): 
            # Tính tọa độ
            x = OFFSET + segment.x * cell_size
            y = OFFSET + segment.y * cell_size
            
            # --- TẠO HIỆU ỨNG ĐỐT RẮN ---
            
            # Bước 1: Vẽ phần nền tối hơn (tạo viền)
            # Thu nhỏ 1 pixel mỗi bên để tạo khe hở giữa các đốt
            gap = 1 
            outer_rect = pygame.Rect(x + gap, y + gap, cell_size - 2*gap, cell_size - 2*gap)
            pygame.draw.rect(screen, (0, 100, 200), outer_rect, border_radius=6) # Màu xanh đậm
            
            # Bước 2: Vẽ phần tâm sáng hơn (tạo độ nổi)
            # Thu nhỏ tiếp 4 pixel nữa để vẽ phần tâm
            inner_gap = 5 
            inner_rect = pygame.Rect(x + inner_gap, y + inner_gap, cell_size - 2*inner_gap, cell_size - 2*inner_gap)
            pygame.draw.rect(screen, (100, 200, 255), inner_rect, border_radius=3) # Màu xanh nhạt

        # 2. VẼ ĐẦU RẮN (Head) - Giữ nguyên logic cũ
        head_pos = self.body[0]
        offset_adjust = (HEAD_SIZE - cell_size) / 2
        
        head_rect = pygame.Rect(
            OFFSET + head_pos.x * cell_size - offset_adjust, 
            OFFSET + head_pos.y * cell_size - offset_adjust, 
            HEAD_SIZE, HEAD_SIZE
        )
        
        # Lấy hình ảnh từ cache
        direction_key = (int(self.direction.x), int(self.direction.y))
        rotated_head = self.head_surfaces.get(direction_key, snake_head_surface)
        
        screen.blit(rotated_head, head_rect)

    def move_snake(self):
        current_head = self.body[0]
        new_head = current_head + self.direction
        
        self.body.appendleft(new_head)
        
        if not self.new_block:
            self.body.pop()
        else:
            self.new_block = False
        
        self.can_move = True # Sau khi rắn đã nhúc nhích xong, mới cho phép nhận lệnh phím tiếp theo

    def add_block(self):
        self.new_block = True
        
    def reset(self):
        self.body = deque([Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)])
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.can_move = True # Reset lại cờ