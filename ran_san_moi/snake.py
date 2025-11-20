# snake.py

import pygame
from pygame.math import Vector2
from constants import cell_size, OFFSET, YELLOW, BLACK, HEAD_SIZE, screen, snake_head_surface

class Snake:
    def __init__(self):
        # Khởi tạo thân Rắn với 3 phân đoạn
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        # Hướng đi ban đầu: sang phải
        self.direction = Vector2(1, 0)

    def draw(self):
        # 1. Vẽ Thân Rắn (trừ đầu)
        for index, segment in enumerate(self.body[1:]): 
            segment_rect = (OFFSET + segment.x * cell_size, 
                            OFFSET + segment.y * cell_size, 
                            cell_size, cell_size)
            
            # Thay đổi màu xen kẽ
            if index % 2 == 0:
                color = YELLOW
            else:
                color = BLACK
            # Vẽ phân đoạn thân rắn với bo góc
            pygame.draw.rect(screen, color, segment_rect, 0, 7)

        # 2. Vẽ Đầu Rắn
        head_segment = self.body[0]
        
        # Điều chỉnh offset để căn giữa đầu lớn hơn
        offset_adjust = (HEAD_SIZE - cell_size) // 2 
        
        head_rect = pygame.Rect(OFFSET + head_segment.x * cell_size - offset_adjust, 
                                 OFFSET + head_segment.y * cell_size - offset_adjust, 
                                 HEAD_SIZE, HEAD_SIZE)
        
        # Xoay và vẽ hình ảnh đầu rắn
        rotated_head = self.rotate_head_image()
        screen.blit(rotated_head, head_rect)

    def rotate_head_image(self):
        # Xác định góc xoay dựa trên hướng đi
        angle = 0
        if self.direction == Vector2(1, 0):    # Phải
            angle = 270
        elif self.direction == Vector2(-1, 0): # Trái
            angle = 90
        elif self.direction == Vector2(0, -1): # Lên
            angle = 0
        elif self.direction == Vector2(0, 1):   # Xuống
            angle = 180
        
        # Trả về bề mặt đầu rắn đã xoay
        return pygame.transform.rotate(snake_head_surface, angle)