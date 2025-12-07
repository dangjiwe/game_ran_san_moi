import pygame
import os

# ==========================================
# 1. HÀM XỬ LÝ ĐƯỜNG DẪN
# ==========================================
# Lấy đường dẫn của file hiện tại để làm gốc
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

# --- THÊM DÒNG NÀY VÀO ĐỂ SỬA LỖI ---
PROJECT_ROOT = BASE_DIR 
# ------------------------------------
# ==========================================
# 2. CẤU HÌNH & MÀU SẮC
# ==========================================

# Màu sắc
GRASS_LIGHT = (170, 215, 81)  
GRASS_DARK  = (162, 209, 73)
BORDER_COLOR = (87, 138, 52) 
GREEN = (173, 204, 96)
YELLOW = (255, 200, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0) 
HEAD_COLOR = (255, 60, 60) 
DARK_GREEN = (43, 51, 24) 

# Kích thước lưới
cell_size = 25       
number_of_cells = 20 
OFFSET = 75          

HEAD_SCALE_FACTOR = 2.5
HEAD_SIZE = int(cell_size * HEAD_SCALE_FACTOR)

# Kích thước màn hình
screen_width = 2 * OFFSET + cell_size * number_of_cells
screen_height = 2 * OFFSET + cell_size * number_of_cells

# ==========================================
# 3. KHỞI TẠO PYGAME & MÀN HÌNH
# ==========================================
# Cấu hình âm thanh trước khi init để giảm độ trễ
try:
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=128)
except Exception: 
    pass

pygame.init() 

# Tạo màn hình
screen = pygame.display.set_mode((screen_width, screen_height)) 
pygame.display.set_caption("Ran_San_Moi")
SCREEN_UPDATE = pygame.USEREVENT

# ==========================================
# 4. TẢI TÀI NGUYÊN (FONTS, ẢNH, NHẠC)
# ==========================================

# --- TẢI ÂM THANH ---
MUSIC_LOADED = False
eat_sound = None

try:
    # Nhạc nền
    music_path = os.path.join(BASE_DIR, "nhac_nen.wav")
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        MUSIC_LOADED = True
    
    # Âm thanh ăn mồi
    eat_path = os.path.join(BASE_DIR, "eat.wav")
    if os.path.exists(eat_path):
        eat_sound = pygame.mixer.Sound(eat_path)
        eat_sound.set_volume(1.0)
except Exception as e:
    print(f"Loi am thanh: {e}")

# --- TẢI FONT ---
try:
    font_path = os.path.join(BASE_DIR, "font_game.ttf")
    font = pygame.font.Font(font_path, 40)
except:
    font = pygame.font.SysFont('Arial', 40)

# --- TẢI ẢNH GAMEPLAY ---
try:
    food_path = os.path.join(BASE_DIR, "food.png")
    food_surface = pygame.image.load(food_path)
    food_surface = pygame.transform.scale(food_surface, (cell_size, cell_size)) 
except:
    food_surface = pygame.Surface((cell_size, cell_size))
    food_surface.fill(DARK_GREEN) 
    
try:
    head_path = os.path.join(BASE_DIR, "dauran.png")
    snake_head_surface = pygame.image.load(head_path).convert_alpha()
    snake_head_surface = pygame.transform.scale(snake_head_surface, (HEAD_SIZE, HEAD_SIZE))
    pygame.display.set_icon(snake_head_surface)
except:
    snake_head_surface = pygame.Surface((HEAD_SIZE, HEAD_SIZE))
    snake_head_surface.fill(HEAD_COLOR)

# Background Gameplay (Mặc định None để vẽ bằng code màu)
bg_surface = None

# --- TẢI ẢNH NỀN MENU ---
menu_bg_surface = None
try:
    menu_bg_path = os.path.join(BASE_DIR, "menu_bg.jpg")
    if os.path.exists(menu_bg_path):
        img = pygame.image.load(menu_bg_path)
        menu_bg_surface = pygame.transform.scale(img, (screen_width, screen_height))
        print("----> Da tai hinh nen Menu!")
    else:
        print("----> Khong tim thay menu_bg.jpg")
except Exception as e:
    print(f"Loi tai nen Menu: {e}")

# --- TẢI ẢNH NỀN LOADING ---
loading_bg_surface = None
try:
    loading_path = os.path.join(BASE_DIR, "loading_bg.png")
    if os.path.exists(loading_path):
        img = pygame.image.load(loading_path)
        loading_bg_surface = pygame.transform.scale(img, (screen_width, screen_height))
        print("----> Da tai hinh nen Loading!")
    else:
        print("----> Khong tim thay loading_bg.png")
except Exception as e:
    print(f"Loi tai nen Loading: {e}")