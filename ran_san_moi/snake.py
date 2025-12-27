import pygame
from pygame.math import Vector2
from collections import deque
from constants import cell_size, number_of_cells, OFFSET, BLUE, HEAD_SIZE, screen, snake_head_surface

class Snake:
    def __init__(self):
        # Mặc định ban đầu (sẽ bị reset ngay khi vào game nên không quan trọng lắm)
        self.body = deque([Vector2(7, 4), Vector2(6, 4), Vector2(5, 4)])
        self.direction = Vector2(1, 0)
        self.new_block = False 
        self.can_move = True  

        self.head_surfaces = {
            (0, -1): pygame.transform.rotate(snake_head_surface, 0),
            (0, 1):  pygame.transform.rotate(snake_head_surface, 180),
            (-1, 0): pygame.transform.rotate(snake_head_surface, 90),
            (1, 0):  pygame.transform.rotate(snake_head_surface, -90)
        }

    def draw(self):
        # 1. VẼ THÂN RẮN
        for index, segment in enumerate(list(self.body)[1:]): 
            x = OFFSET + segment.x * cell_size
            y = OFFSET + segment.y * cell_size
            
            gap = 1 
            outer_rect = pygame.Rect(x + gap, y + gap, cell_size - 2*gap, cell_size - 2*gap)
            pygame.draw.rect(screen, (0, 100, 200), outer_rect, border_radius=6) 
            
            inner_gap = 5 
            inner_rect = pygame.Rect(x + inner_gap, y + inner_gap, cell_size - 2*inner_gap, cell_size - 2*inner_gap)
            pygame.draw.rect(screen, (100, 200, 255), inner_rect, border_radius=3) 

        # 2. VẼ ĐẦU RẮN
        head_pos = self.body[0]
        offset_adjust = (HEAD_SIZE - cell_size) / 2
        
        head_rect = pygame.Rect(
            OFFSET + head_pos.x * cell_size - offset_adjust, 
            OFFSET + head_pos.y * cell_size - offset_adjust, 
            HEAD_SIZE, HEAD_SIZE
        )
        
        direction_key = (int(self.direction.x), int(self.direction.y))
        rotated_head = self.head_surfaces.get(direction_key, snake_head_surface)
        screen.blit(rotated_head, head_rect)

    def move_snake(self):
        current_head = self.body[0]
        
        # Logic xuyên tường
        x_new = (current_head.x + self.direction.x) % number_of_cells
        y_new = (current_head.y + self.direction.y) % number_of_cells
        
        new_head = Vector2(x_new, y_new)
        self.body.appendleft(new_head)
        
        if not self.new_block:
            self.body.pop()
        else:
            self.new_block = False
        
        self.can_move = True 

    def add_block(self):
        self.new_block = True
        
    def reset(self, start_pos=None):
        """
        Reset rắn về vị trí chỉ định.
        start_pos: tuple (x, y) ví dụ (3, 5)
        """
        if start_pos is None:
            start_x, start_y = 7, 4 # Mặc định nếu không truyền gì
        else:
            start_x, start_y = start_pos

        # Tạo rắn dài 3 đốt, hướng sang phải
        self.body = deque([
            Vector2(start_x, start_y),     # Đầu
            Vector2(start_x - 1, start_y), # Thân 1
            Vector2(start_x - 2, start_y)  # Đuôi
        ])
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.can_move = True