# files/Resources/snake.py

import pygame
from pygame.math import Vector2
from constants import cell_size, OFFSET, YELLOW, BLUE, BLACK, HEAD_SIZE, screen, snake_head_surface

class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)
        self.new_block = False 

    def draw(self):
        # 1. Vẽ Thân Rắn (trừ đầu)
        for index, segment in enumerate(self.body[1:]): 
            segment_rect = (OFFSET + segment.x * cell_size, 
                            OFFSET + segment.y * cell_size, 
                            cell_size, cell_size)
            
            if index % 2 == 0:
                color = BLUE
            else:
                color = BLUE
            
            pygame.draw.rect(screen, color, segment_rect, 0, 7)

        # 2. Vẽ Đầu Rắn
        head_segment = self.body[0]
        offset_adjust = (HEAD_SIZE - cell_size) / 2
        
        head_rect = (OFFSET + head_segment.x * cell_size - offset_adjust, 
                     OFFSET + head_segment.y * cell_size - offset_adjust, 
                     HEAD_SIZE, HEAD_SIZE)
        
        rotated_head = self.rotate_head()
        
        screen.blit(rotated_head, head_rect)

    def rotate_head(self):
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
        self.new_block = False