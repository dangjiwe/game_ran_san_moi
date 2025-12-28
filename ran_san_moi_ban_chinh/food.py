# File: food.py
import random
import pygame
from pygame.math import Vector2
from constants import cell_size, number_of_cells, OFFSET

class Food:
    def __init__(self, snake_body, walls=[]):
        self.walls = walls
        
        # Tạo tập hợp tất cả các ô trên bản đồ
        self.all_cells = set()
        for x in range(number_of_cells):
            for y in range(number_of_cells):
                self.all_cells.add((x, y))
        # Vị trí mồi đặc biệt (ban đầu là None - chưa xuất hiện)
        self.special_position = None         

        
        # Vị trí mồi thường (luôn có)
        self.position = self.generate_random_pos(snake_body)
        
        self.eat_counter = 0     # Đếm số lần ăn mồi thường

    def draw(self, screen):
        # 1. Vẽ mồi thường (Luôn vẽ)
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, 
                                OFFSET + self.position.y * cell_size, 
                                cell_size, cell_size)
        
        from constants import food_surface
        screen.blit(food_surface, food_rect)

        # 2. Vẽ mồi đặc biệt (Chỉ vẽ nếu nó đang tồn tại - khác None)
        if self.special_position:
            special_rect = pygame.Rect(OFFSET + self.special_position.x * cell_size, 
                                       OFFSET + self.special_position.y * cell_size, 
                                       cell_size, cell_size)
            
            from constants import special_food_surface
            if special_food_surface:
                screen.blit(special_food_surface, special_rect)
            else:
                # Vẽ màu đỏ nếu không có ảnh
                pygame.draw.rect(screen, (255, 0, 0), special_rect)

    def generate_random_pos(self, snake_body):
        """Sinh vị trí cho mồi thường"""
        occupied = set((int(b.x), int(b.y)) for b in snake_body)
        occupied = occupied.union(set((int(w.x), int(w.y)) for w in self.walls))
        
        # Nếu đang có mồi đặc biệt thì mồi thường không được đè lên nó
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
        
        # Mồi đặc biệt không được đè lên mồi thường đang có
        occupied.add((int(self.position.x), int(self.position.y)))

        free_cells = list(self.all_cells - occupied)
        if free_cells:
            x, y = random.choice(free_cells)
            self.special_position = Vector2(x, y)
        else:
            self.special_position = None