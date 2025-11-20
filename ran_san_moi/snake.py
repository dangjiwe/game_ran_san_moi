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
        self.new_block = False # Biến cờ: True nếu rắn vừa ăn mồi (và cần dài thêm)

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
        
    # --- BỔ SUNG: CHỨC NĂNG DI CHUYỂN ---
    def move_snake(self):
        # 1. Sao chép thân rắn hiện tại
        if self.new_block:
            # Nếu ăn mồi (new_block=True), giữ nguyên đuôi, chỉ thêm đầu mới
            body_copy = self.body[:] 
            self.new_block = False # Đặt lại cờ sau khi thêm khối
        else:
            # Nếu không ăn mồi, xóa phần đuôi (body[:-1])
            body_copy = self.body[:-1]
        
        # 2. Tính toán vị trí đầu mới
        new_head = body_copy[0] + self.direction
        
        # 3. Thêm đầu mới vào vị trí đầu danh sách
        body_copy.insert(0, new_head)
        
        # 4. Cập nhật thân rắn
        self.body = body_copy
        
    def add_block(self):
        # Được gọi khi rắn ăn mồi
        self.new_block = True
        
    # --- BỔ SUNG: CHỨC NĂNG TỰ CẮN THÂN ---
    def check_self_bite(self):
        # Kiểm tra xem đầu rắn (self.body[0]) có trùng với bất kỳ đoạn thân nào (self.body[1:]) không
        return self.body[0] in self.body[1:]
        
    # --- BỔ SUNG: CHỨC NĂNG RESET ---
    def reset(self):
        # Đặt lại vị trí ban đầu và hướng
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)
        self.new_block = False