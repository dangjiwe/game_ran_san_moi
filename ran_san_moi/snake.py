# files/Resources/snake.py

import pygame
from pygame.math import Vector2
from constants import cell_size, OFFSET, YELLOW, BLACK, HEAD_SIZE, screen, snake_head_surface, number_of_cells

class Snake:
    def __init__(self):
        # Sửa Bug 3: Đặt vị trí spawn gần trung tâm hơn
        self.body = [Vector2(10, 10), Vector2(9, 10), Vector2(8, 10)]
        # Hướng đi ban đầu: sang phải
        self.direction = Vector2(1, 0)
        # Sửa Bug 3 & 4: next_direction để ngăn đổi hướng 180 độ đột ngột
        self.next_direction = Vector2(1, 0) 
        self.new_block = False 

    def draw(self):
        # 1. Vẽ Thân Rắn (trừ đầu)
        for index, segment in enumerate(self.body[1:]): 
            segment_rect = (OFFSET + segment.x * cell_size, 
                            OFFSET + segment.y * cell_size, 
                            cell_size, cell_size)
            
            if index % 2 == 0:
                color = YELLOW
            else:
                color = BLACK
            
            pygame.draw.rect(screen, color, segment_rect, 0, 7)

        # 2. Vẽ Đầu Rắn
        head_segment = self.body[0]
        offset_adjust = (HEAD_SIZE - cell_size) / 2
        
        head_rect = (OFFSET + head_segment.x * cell_size - offset_adjust, 
                     OFFSET + head_segment.y * cell_size - offset_adjust, 
                     HEAD_SIZE, HEAD_SIZE)
        
        rotated_head = self.rotate_head()
        
        screen.blit(rotated_head, head_rect)

    def rotate_head_image(self):
        # Sửa lại góc xoay cho đúng chuẩn: Lên=0, Trái=90, Xuống=180, Phải=270
        angle = 0
        if self.direction == Vector2(-1, 0): 
            angle = 90
        elif self.direction == Vector2(1, 0):
            angle = -90
        elif self.direction == Vector2(0, -1):
            angle = 0
        elif self.direction == Vector2(0, 1):
            angle = 180
        
        return pygame.transform.rotate(snake_head_surface, angle)
        
    def move_snake(self):
        # --- KHẮC PHỤC LỖI #4: Cập nhật hướng di chuyển chính bằng hướng chờ ---
        self.direction = self.next_direction 
        # ---------------------------------------------------------------------
        
        # Xử lý Bug 4: Đảm bảo new_block được xử lý đúng
        if self.new_block:
            body_copy = self.body[:] 
            self.new_block = False 
        else:
            body_copy = self.body[:-1]
        
        new_head = body_copy[0] + self.direction
        body_copy.insert(0, new_head)
        
        self.body = body_copy
        
    def add_block(self):
        self.new_block = True
        
    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)
        self.next_direction = Vector2(1, 0) # Reset next_direction
        self.new_block = False