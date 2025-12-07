# files/Resources/constants.py

import pygame
import os 
import sys 

# ==========================================
# 1. HÀM XỬ LÝ ĐƯỜNG DẪN
# ==========================================
def resource_path(relative_path, sub_dir):
    try:
        base_path = sys._MEIPASS 
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    return os.path.join(base_path, sub_dir, relative_path)

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
PROJECT_ROOT = os.path.dirname(BASE_DIR) 

# ==========================================
# 2. CẤU HÌNH & MÀU SẮC (ĐẶT LÊN ĐẦU)
# ==========================================
# Phải định nghĩa các biến này trước khi khởi tạo màn hình

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
# Fix độ trễ âm thanh
try:
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=128)
except Exception: pass

pygame.init() 

# Tạo màn hình (Lúc này screen_width đã được định nghĩa ở trên -> Không lỗi)
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
    music_path = resource_path("nhac_nen.wav", sub_dir=os.path.join("Extra", "Sound_DLC"))
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        MUSIC_LOADED = True
    
    # Âm thanh ăn mồi
    eat_path = resource_path("eat.wav", sub_dir=os.path.join("Extra", "Sound_DLC"))
    if os.path.exists(eat_path):
        eat_sound = pygame.mixer.Sound(eat_path)
        eat_sound.set_volume(1.0)
except Exception as e:
    print(f"Loi am thanh: {e}")

# --- TẢI FONT ---
try:
    font_path = resource_path("font_game.ttf", sub_dir=os.path.join("Extra", "Text"))
    font = pygame.font.Font(font_path, 40)
except:
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

# Background (để None vì vẽ bằng code)
bg_surface = None


# --- TẢI ẢNH NỀN MENU (MỚI) ---
menu_bg_surface = None

try:
    # Tên file ảnh bạn vừa chép vào
    menu_bg_path = resource_path("menu_bg.jpg", sub_dir="CDNImage")
    
    if os.path.exists(menu_bg_path):
        img = pygame.image.load(menu_bg_path)
        # Co giãn ảnh cho vừa khít màn hình
        menu_bg_surface = pygame.transform.scale(img, (screen_width, screen_height))
        print("----> Da tai hinh nen Menu!")
    else:
        print("----> Khong tim thay menu_bg.png, dung mau nen mac dinh.")
        
except Exception as e:
    print(f"Loi tai nen Menu: {e}")


    # --- TẢI ẢNH NỀN LOADING (MỚI) ---
loading_bg_surface = None

try:
    # Tên file ảnh bạn vừa chép vào
    loading_path = resource_path("loading_bg.png", sub_dir="CDNImage")
    
    if os.path.exists(loading_path):
        img = pygame.image.load(loading_path)
        # Co giãn ảnh cho vừa khít màn hình
        loading_bg_surface = pygame.transform.scale(img, (screen_width, screen_height))
        print("----> Da tai hinh nen Loading!")
    else:
        print("----> Khong tim thay loading_bg.jpg, dung mau nen mac dinh.")
        
except Exception as e:
    print(f"Loi tai nen Loading: {e}")