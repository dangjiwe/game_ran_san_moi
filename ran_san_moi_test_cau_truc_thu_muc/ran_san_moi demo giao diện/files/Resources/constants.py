# files/Resources/constants.py

import pygame
import os 
import sys 
from pygame.math import Vector2

# --- HÀM XỬ LÝ PATH (QUAN TRỌNG CHO EXE) ---
def resource_path(relative_path, sub_dir):
    try:
        base_path = sys._MEIPASS # Path tạm khi chạy exe
    except Exception:
        # Path khi chạy code thường: Lùi về thư mục 'files'
        base_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

    return os.path.join(base_path, sub_dir, relative_path)
# -------------------------------------------

# Path gốc dùng để lưu file JSON (luôn nằm ngoài exe)
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
PROJECT_ROOT = os.path.dirname(BASE_DIR) 

# Màu sắc
GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)
YELLOW = (255, 200, 0)
BLACK = (0, 0, 0) 
HEAD_COLOR = (255, 60, 60) 

# Cấu hình
cell_size = 25
number_of_cells = 20
OFFSET = 75
HEAD_SCALE_FACTOR = 2.5
HEAD_SIZE = int(cell_size * HEAD_SCALE_FACTOR)
screen_width = 2 * OFFSET + cell_size * number_of_cells
screen_height = 2 * OFFSET + cell_size * number_of_cells

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height)) 
pygame.display.set_caption("Ran_San_Moi")
SCREEN_UPDATE = pygame.USEREVENT

# --- TẢI FONT (CẬP NHẬT ĐƯỜNG DẪN EXTRA) ---
try:
    # Đường dẫn: Extra/Text/font_game.ttf
    font_path = resource_path("font_game.ttf", sub_dir=os.path.join("Extra", "Text"))
    font = pygame.font.Font(font_path, 40)
except Exception as e:
    print(f"Lỗi font: {e}. Dùng mặc định.")
    font = pygame.font.SysFont('Arial', 40)

# --- TẢI ẢNH ---
try:
    food_path = resource_path("food.png", sub_dir="CDNImage") 
    food_surface = pygame.image.load(food_path)
    food_surface = pygame.transform.scale(food_surface, (cell_size, cell_size)) 
except:
    food_surface = pygame.Surface((cell_size, cell_size))
    food_surface.fill(DARK_GREEN) 
    
try:
    head_path = resource_path("dauran.png", sub_dir="CDNImage")
    snake_head_surface = pygame.image.load(head_path).convert_alpha()
    snake_head_surface = pygame.transform.scale(snake_head_surface, (HEAD_SIZE, HEAD_SIZE))
    pygame.display.set_icon(snake_head_surface)
except:
    snake_head_surface = pygame.Surface((HEAD_SIZE, HEAD_SIZE))
    snake_head_surface.fill(HEAD_COLOR)