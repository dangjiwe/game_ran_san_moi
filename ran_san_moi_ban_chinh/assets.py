# assets.py
import pygame
import os
from settings import *
import display 

pygame.mixer.init()

# --- ÂM THANH (SOUND EFFECTS) ---
eat_sound = None
click_sound = None
game_over_sound = None
countdown_sound = None 
eat_special_sound = None
highscore_sound = None

# Tải Sound Effect (Giữ nguyên như cũ)
try:
    eat_path = os.path.join(BASE_DIR, "eat.wav")
    if os.path.exists(eat_path):
        eat_sound = pygame.mixer.Sound(eat_path)
        eat_sound.set_volume(1.0)
except Exception: pass

try:
    click_path = os.path.join(BASE_DIR, "click.wav")
    if not os.path.exists(click_path): click_path = os.path.join(BASE_DIR, "click.mp3")
    if os.path.exists(click_path):
        click_sound = pygame.mixer.Sound(click_path)
        click_sound.set_volume(1.0)
except Exception: pass

try:
    game_over_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "game_over.wav"))
    game_over_sound.set_volume(0.5) 
except Exception: game_over_sound = None 

try:
    count_path = os.path.join(BASE_DIR, "countdown.wav") 
    if not os.path.exists(count_path): count_path = os.path.join(BASE_DIR, "countdown.mp3")
    if os.path.exists(count_path):
        countdown_sound = pygame.mixer.Sound(count_path)
        countdown_sound.set_volume(0.3) 

    eat_sp_path = os.path.join(BASE_DIR, "eat_special.wav")
    if os.path.exists(eat_sp_path):
        eat_special_sound = pygame.mixer.Sound(eat_sp_path)
        eat_special_sound.set_volume(1.0)
except Exception: pass

# --- [MỚI] QUẢN LÝ NHẠC NỀN (MUSIC) ---
# Thay vì load luôn, ta chỉ lưu đường dẫn
MENU_MUSIC_PATH = None
GAME_MUSIC_PATH = None

try:
    # 1. Nhạc nền Menu (File cũ: nhac_nen.mp3)
    path1 = os.path.join(BASE_DIR, "nhac_nen.mp3")
    if os.path.exists(path1):
        MENU_MUSIC_PATH = path1
        
    # 2. Nhạc nền Game (File mới: nhac_game.mp3)
    # Bạn hãy tạo file nhac_game.mp3 hoặc .wav
    path2 = os.path.join(BASE_DIR, "nhac_game.mp3")
    if os.path.exists(path2):
        GAME_MUSIC_PATH = path2
    else:
        # Nếu không có file nhạc game riêng, dùng tạm nhạc menu
        GAME_MUSIC_PATH = MENU_MUSIC_PATH
        
except Exception as e:
    print(f"Lỗi tìm đường dẫn nhạc: {e}")


# --- TẢI FONT & ẢNH (GIỮ NGUYÊN KHÔNG ĐỔI) ---
try:
    font_path = os.path.join(BASE_DIR, "font_game.ttf")
    font = pygame.font.Font(font_path, 40)
except:
    font = pygame.font.SysFont('Arial', 40)

try:
    food_path = os.path.join(BASE_DIR, "food.png")
    food_surface = pygame.image.load(food_path)
    food_surface = pygame.transform.scale(food_surface, (cell_size, cell_size)) 
except:
    food_surface = pygame.Surface((cell_size, cell_size))
    food_surface.fill(DARK_GREEN) 

try:
    sp_food_path = os.path.join(BASE_DIR, "special_food.png")
    special_food_surface = pygame.image.load(sp_food_path)
    special_food_surface = pygame.transform.scale(special_food_surface, (cell_size, cell_size))
except:
    special_food_surface = pygame.Surface((cell_size, cell_size))
    special_food_surface.fill((255, 215, 0)) 
    
try:
    head_path = os.path.join(BASE_DIR, "dauran.png")
    snake_head_surface = pygame.image.load(head_path).convert_alpha()
    snake_head_surface = pygame.transform.scale(snake_head_surface, (HEAD_SIZE, HEAD_SIZE))
    pygame.display.set_icon(snake_head_surface)
except:
    snake_head_surface = pygame.Surface((HEAD_SIZE, HEAD_SIZE))
    snake_head_surface.fill(HEAD_COLOR)

bg_surface = None
menu_bg_surface = None
loading_bg_surface = None

try:
    menu_bg_path = os.path.join(BASE_DIR, "menu_bg.png")
    if os.path.exists(menu_bg_path):
        img = pygame.image.load(menu_bg_path)
        menu_bg_surface = pygame.transform.scale(img, (screen_width, screen_height))
    
    loading_path = os.path.join(BASE_DIR, "loading_bg.png")
    if os.path.exists(loading_path):
        img = pygame.image.load(loading_path)
        loading_bg_surface = pygame.transform.scale(img, (screen_width, screen_height))
except Exception as e:
    print(f"Loi tai anh nen: {e}")

try:
    hs_path = os.path.join(BASE_DIR, "highscore.wav")
    if not os.path.exists(hs_path): hs_path = os.path.join(BASE_DIR, "highscore.mp3")
    
    if os.path.exists(hs_path):
        highscore_sound = pygame.mixer.Sound(hs_path)
        highscore_sound.set_volume(1.0) # Âm lượng to rõ
except Exception: pass