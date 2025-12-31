import pygame
import os
from settings import *

pygame.mixer.init()

# --- CẤU HÌNH ĐƯỜNG DẪN MỚI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RES_DIR = os.path.join(BASE_DIR, "Resources")

SOUND_DIR = os.path.join(RES_DIR, "sound")
IMG_DIR = os.path.join(RES_DIR, "images")
FONT_DIR = os.path.join(RES_DIR, "fonts")

# --- ÂM THANH (SOUND EFFECTS) ---
eat_sound = None
click_sound = None
game_over_sound = None
countdown_sound = None 
eat_special_sound = None
highscore_sound = None

# Hàm hỗ trợ load âm thanh cho gọn
def load_sound(filename):
    path = os.path.join(SOUND_DIR, filename)
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    # Thử tìm đuôi mở rộng khác nếu cần (ví dụ .mp3 thay vì .wav)
    if filename.endswith(".wav"):
        alt_path = path.replace(".wav", ".mp3")
        if os.path.exists(alt_path):
            return pygame.mixer.Sound(alt_path)
    return None

try:
    eat_sound = load_sound("eat.wav")
    if eat_sound: eat_sound.set_volume(1.0)
except: pass

try:
    click_sound = load_sound("click.wav")
    if click_sound: click_sound.set_volume(1.0)
except: pass

try:
    game_over_sound = load_sound("game_over.wav")
    if game_over_sound: game_over_sound.set_volume(0.5)
except: pass

try:
    countdown_sound = load_sound("countdown.wav")
    if countdown_sound: countdown_sound.set_volume(0.3)
except: pass

try:
    eat_special_sound = load_sound("eat_special.wav")
    if eat_special_sound: eat_special_sound.set_volume(1.0)
except: pass

try:
    highscore_sound = load_sound("highscore.wav")
    if highscore_sound: highscore_sound.set_volume(1.0)
except: pass

# --- QUẢN LÝ NHẠC NỀN ---
MENU_MUSIC_PATH = os.path.join(SOUND_DIR, "nhac_nen.mp3")
GAME_MUSIC_PATH = os.path.join(SOUND_DIR, "nhac_game.mp3")

if not os.path.exists(GAME_MUSIC_PATH):
    GAME_MUSIC_PATH = MENU_MUSIC_PATH # Dùng tạm nếu chưa có nhạc game

# --- TẢI FONT & ẢNH ---
# Font
font_path = os.path.join(FONT_DIR, "font_game.ttf")
try:
    font = pygame.font.Font(font_path, 40)
except:
    font = pygame.font.SysFont('Arial', 40)

# Icon đầu rắn (dùng làm icon cửa sổ)
try:
    head_path = os.path.join(IMG_DIR, "icon.png")
    if os.path.exists(head_path):
        snake_head_surface = pygame.image.load(head_path).convert_alpha()
        snake_head_surface = pygame.transform.scale(snake_head_surface, (HEAD_SIZE, HEAD_SIZE))
        pygame.display.set_icon(snake_head_surface)
except: pass

# Hình nền
bg_surface = None
menu_bg_surface = None
loading_bg_surface = None

try:
    menu_bg_path = os.path.join(IMG_DIR, "menu_bg.png")
    if os.path.exists(menu_bg_path):
        img = pygame.image.load(menu_bg_path)
        menu_bg_surface = pygame.transform.scale(img, (screen_width, screen_height))
    
    loading_path = os.path.join(IMG_DIR, "loading_bg.png")
    if os.path.exists(loading_path):
        img = pygame.image.load(loading_path)
        loading_bg_surface = pygame.transform.scale(img, (screen_width, screen_height))
except Exception as e:
    print(f"Lỗi tải ảnh nền: {e}")

def stop_all_sfx():
    """Hàm này dùng để tắt ngay lập tức các hiệu ứng âm thanh dài"""
    try:
        if countdown_sound: 
            countdown_sound.stop()
        if game_over_sound: 
            game_over_sound.stop()
        if highscore_sound: 
            highscore_sound.stop()
        if eat_sound:
            eat_sound.stop()
        if eat_special_sound:
            eat_special_sound.stop()
        
    except Exception as e:
        print(f"Lỗi khi dừng âm thanh: {e}")

# Ảnh thức ăn cũ (để giữ tương thích code, dù không dùng)
food_surface = None
special_food_surface = None