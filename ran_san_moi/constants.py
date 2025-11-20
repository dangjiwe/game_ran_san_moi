# constants.py

import pygame
import os 
from pygame.math import Vector2

# --- BỔ SUNG KHẮC PHỤC LỖI PATH ---
# Lấy đường dẫn tuyệt đối của thư mục chứa file constants.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ------------------------------------

# Màu sắc
GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)
YELLOW = (255, 200, 0)
BLACK = (0, 0, 0) 
HEAD_COLOR = (255, 60, 60) 

# Cấu hình lưới
cell_size = 25
number_of_cells = 20
OFFSET = 75

# Cấu hình Đầu Rắn
HEAD_SCALE_FACTOR = 2.5
HEAD_SIZE = int(cell_size * HEAD_SCALE_FACTOR)

# Kích thước Màn hình
screen_width = 2 * OFFSET + cell_size * number_of_cells
screen_height = 2 * OFFSET + cell_size * number_of_cells

# Khởi tạo Pygame và Cửa sổ
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height)) 
pygame.display.set_caption("Ran_San_Moi")

# Định nghĩa Event cho chuyển động
SCREEN_UPDATE = pygame.USEREVENT

# --- BỔ SUNG FONT CHỮ ---
# Khởi tạo font để hiển thị Game Over
try:
    font = pygame.font.Font(None, 40) # Font mặc định của Pygame, cỡ 40
except:
    font = pygame.font.SysFont('Arial', 40)
# -------------------------

# Tải và Xử lý bề mặt (Surface)
try:
    # Bề mặt Thức ăn
    # SỬ DỤNG os.path.join VÀ BASE_DIR ĐỂ TẠO ĐƯỜNG DẪN TUYỆT ĐỐI
    food_path = os.path.join(BASE_DIR, "food.png")
    food_surface = pygame.image.load(food_path)
    food_surface = pygame.transform.scale(food_surface, (cell_size, cell_size)) 
except pygame.error:
    print("Lỗi: Không tìm thấy file 'food.png'. Sử dụng màu mặc định.")
    food_surface = pygame.Surface((cell_size, cell_size))
    food_surface.fill(DARK_GREEN) 
    
try:
    # Bề mặt Đầu Rắn
    # SỬ DỤNG os.path.join VÀ BASE_DIR ĐỂ TẠO ĐƯỜNG DẪN TUYỆT ĐỐI
    head_path = os.path.join(BASE_DIR, "dauran.png")
    snake_head_surface = pygame.image.load(head_path).convert_alpha()
    snake_head_surface = pygame.transform.scale(snake_head_surface, (HEAD_SIZE, HEAD_SIZE))
except pygame.error:
    print("Lỗi: Không tìm thấy file 'dauran.png'. Sử dụng màu mặc định.")
    snake_head_surface = pygame.Surface((HEAD_SIZE, HEAD_SIZE))
    snake_head_surface.fill(HEAD_COLOR)