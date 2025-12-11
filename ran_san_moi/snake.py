# snake.py

import pygame
from pygame.math import Vector2
from constants import cell_size, OFFSET, YELLOW, BLACK, HEAD_SIZE, screen, snake_head_surface, number_of_cells

class Snake:
    def __init__(self):
        # Vị trí spawn
        self.body = [Vector2(10, 10), Vector2(9, 10), Vector2(8, 10)]
        self.direction = Vector2(1, 0)
        self.next_direction = Vector2(1, 0) 
        self.new_block = False 

    def draw(self):
        # 1. Vẽ Thân Rắn (trừ đầu)
        for index, segment in enumerate(self.body[1:]): 
            segment_rect = (OFFSET + segment.x * cell_size, 
                            OFFSET + segment.y * cell_size, 
                            cell_size, cell_size)
            
            # Màu xen kẽ giữa các đoạn thân
            if index % 2 == 0:
                color = YELLOW
            else:
                color = BLACK
            # Vẽ phân đoạn thân rắn với bo góc
            pygame.draw.rect(screen, color, segment_rect, 0, 7)

        # 2. Vẽ Đầu Rắn
        head_segment = self.body[0]
        
        # --- KHẮC PHỤC LỖI: Căn chỉnh đầu rắn lớn hơn cell_size ---
        offset_adjust = (HEAD_SIZE - cell_size) // 2 
        
        head_rect = pygame.Rect(OFFSET + head_segment.x * cell_size - offset_adjust, 
                                 OFFSET + head_segment.y * cell_size - offset_adjust, 
                                 HEAD_SIZE, HEAD_SIZE)
        # -------------------------------------------------------------
        
        # Xoay và vẽ hình ảnh đầu rắn
        rotated_head = self.rotate_head_image()
        screen.blit(rotated_head, head_rect)

    def rotate_head_image(self):
        # Sửa lại góc xoay
        angle = 0
        if self.direction == Vector2(1, 0):    # Phải
            angle = 270
        elif self.direction == Vector2(-1, 0): # Trái
            angle = 90
        elif self.direction == Vector2(0, -1): # Lên
            angle = 0
        elif self.direction == Vector2(0, 1):   # Xuống
            angle = 180
        
        return pygame.transform.rotate(snake_head_surface, angle)
        
    def move_snake(self):
        # NOTE: self.direction đã được cập nhật bằng self.next_direction trong game.update() (Sửa Lỗi 1)
        
        if self.new_block:
            body_copy = self.body[:] 
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        
        new_head = body_copy[0] + self.direction
        
        # --- SỬA LỖI 4: Xử lý xuyên tường (wrap-around) ngay sau khi tính toán new_head ---
        # Sẽ không còn giật lag 1 frame vì tọa độ mới đã được tính toán
        
        # Xuyên ngang (Trái sang Phải / Phải sang Trái)
        if new_head.x >= number_of_cells:
            new_head.x = 0
        elif new_head.x < 0:
            new_head.x = number_of_cells - 1
            
        # Xuyên dọc (Trên xuống Dưới / Dưới lên Trên)
        if new_head.y >= number_of_cells:
            new_head.y = 0
        elif new_head.y < 0:
            new_head.y = number_of_cells - 1
            
        # -----------------------------------------------------------------------------------
        
        body_copy.insert(0, new_head)
        
        self.body = body_copy
        
    def add_block(self):
        self.new_block = True
        
    def check_self_bite(self):
        return self.body[0] in self.body[1:]
        
    def reset(self):
        # Đặt lại vị trí ban đầu
        self.body = [Vector2(10, 10), Vector2(9, 10), Vector2(8, 10)]
        self.direction = Vector2(1, 0)
        self.next_direction = Vector2(1, 0) 
        self.new_block = False