import pygame
from pygame.math import Vector2
from collections import deque
from constants import cell_size, OFFSET, HEAD_SIZE, screen, SKINS, BLACK, WHITE

class Snake:
    def __init__(self):
        # Vị trí mặc định
        self.body = deque([Vector2(7, 4), Vector2(6, 4), Vector2(5, 4)])
        self.direction = Vector2(1, 0)
        self.new_block = False 
        self.can_move = True  

        # --- MÀU SẮC ---
        self.skin_id = 0 
        self.update_skin_colors()

    def update_skin_colors(self):
        """Cập nhật màu dựa trên skin_id"""
        skin = SKINS[self.skin_id]
        self.outer_color = skin["outer"]
        self.inner_color = skin["inner"]

    def set_skin(self, index):
        if 0 <= index < len(SKINS):
            self.skin_id = index
            self.update_skin_colors()

    def draw(self):
        # 1. VẼ THÂN RẮN
        # Vẽ toàn bộ thân rắn từ đốt thứ 2 trở đi
        for index, segment in enumerate(list(self.body)[1:]): 
            x = OFFSET + segment.x * cell_size
            y = OFFSET + segment.y * cell_size
            
            # Vẽ khối hộp bo tròn đơn giản
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, self.outer_color, rect, border_radius=4)
            
            # Vẽ tâm nhỏ bên trong để tạo chi tiết (tùy chọn, nếu muốn phẳng lì thì bỏ dòng này)
            inner_rect = pygame.Rect(x + 4, y + 4, cell_size - 8, cell_size - 8)
            pygame.draw.rect(screen, self.inner_color, inner_rect, border_radius=2)

        # 2. VẼ ĐẦU RẮN (TỐI GIẢN)
        self.draw_minimal_head()

    def draw_minimal_head(self):
        head = self.body[0]
        x = OFFSET + head.x * cell_size
        y = OFFSET + head.y * cell_size
        
        # A. Vẽ hộp đầu (Giống hệt thân nhưng không có tâm sáng để dễ phân biệt)
        head_rect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(screen, self.outer_color, head_rect, border_radius=4)

        # B. Vẽ 2 mắt (Chấm đen đơn giản để định hướng)
        # Tính toán vị trí mắt theo hướng đi
        eye_size = 4
        eye_offset = 6 # Khoảng cách từ tâm ra mắt
        
        center_x = x + cell_size // 2
        center_y = y + cell_size // 2
        
        # Vector vuông góc để xác định trái/phải
        perp = Vector2(-self.direction.y, self.direction.x)
        
        # Đẩy mắt về phía trước một chút
        front_x = center_x + self.direction.x * 6
        front_y = center_y + self.direction.y * 6
        
        # Tọa độ 2 mắt
        eye1_x = front_x + perp.x * 6
        eye1_y = front_y + perp.y * 6
        
        eye2_x = front_x - perp.x * 6
        eye2_y = front_y - perp.y * 6
        
        # Vẽ 2 chấm mắt đen
        pygame.draw.circle(screen, BLACK, (int(eye1_x), int(eye1_y)), eye_size)
        pygame.draw.circle(screen, BLACK, (int(eye2_x), int(eye2_y)), eye_size)

    def move_snake(self):
        from constants import number_of_cells 
        current_head = self.body[0]
        # Xuyên tường
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
        if start_pos is None: start_x, start_y = 7, 4
        else: start_x, start_y = start_pos
        self.body = deque([Vector2(start_x, start_y), Vector2(start_x - 1, start_y), Vector2(start_x - 2, start_y)])
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.can_move = True