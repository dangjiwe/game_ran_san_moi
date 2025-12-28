#assets.py nằm trong import của constants.py
import pygame
import os
from settings import *
'''(
    BASE_DIR, cell_size, HEAD_SIZE, 
    DARK_GREEN, HEAD_COLOR, screen_width, screen_height
)'''
# Cần import display để đảm bảo pygame đã init trước khi load ảnh
import display 
pygame.mixer.init()
# --- TẢI ÂM THANH ---
MUSIC_LOADED = False
eat_sound = None
click_sound = None

try:
    music_path = os.path.join(BASE_DIR, "nhac_nen.mp3")
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        MUSIC_LOADED = True
    
    eat_path = os.path.join(BASE_DIR, "eat.wav")
    if os.path.exists(eat_path):
        eat_sound = pygame.mixer.Sound(eat_path)
        eat_sound.set_volume(1.0)
except Exception as e:
    print(f"Loi am thanh nhạc nen hoac an: {e}")

# 3. Tiếng bấm nút (click.wav) <--- THÊM ĐOẠN NÀY
try:
    click_path = os.path.join(BASE_DIR, "click.wav")
    # Backup: Nếu không có wav thì tìm mp3
    if not os.path.exists(click_path):
        click_path = os.path.join(BASE_DIR, "click.mp3")

    if os.path.exists(click_path):
        click_sound = pygame.mixer.Sound(click_path)
        click_sound.set_volume(1.0)
        print("--> DA TAI THANH CONG CLICK SOUND") # In dòng này để check
    else:
        print("--> KHONG TIM THAY FILE CLICK (WAV HOAC MP3)")
except Exception as e:
    print(f"Loi tai click sound: {e}")
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

    # 2. Thức ăn đặc biệt (MỚI THÊM VÀO ĐÂY)
try:
    # Bạn hãy lưu một hình ảnh tên là "special_food.png" vào cùng thư mục
    sp_food_path = os.path.join(BASE_DIR, "special_food.png")
    special_food_surface = pygame.image.load(sp_food_path)
    special_food_surface = pygame.transform.scale(special_food_surface, (cell_size, cell_size))
    print("--> DA TAI THANH CONG SPECIAL FOOD SURFACE") # In dòng này để check
except:
    # Nếu không tìm thấy ảnh, tạo một ô vuông màu Vàng (Gold)
    special_food_surface = pygame.Surface((cell_size, cell_size))
    special_food_surface.fill((255, 215, 0)) # Màu Vàng Gold
    print("--> KHONG TIM THAY FILE SPECIAL FOOD, SU DUNG HINH DUNG THAY THE")
    
try:
    head_path = os.path.join(BASE_DIR, "dauran.png")
    snake_head_surface = pygame.image.load(head_path).convert_alpha()
    snake_head_surface = pygame.transform.scale(snake_head_surface, (HEAD_SIZE, HEAD_SIZE))
    pygame.display.set_icon(snake_head_surface)
except:
    snake_head_surface = pygame.Surface((HEAD_SIZE, HEAD_SIZE))
    snake_head_surface.fill(HEAD_COLOR)

# Background Gameplay
bg_surface = None

# --- TẢI ẢNH NỀN MENU & LOADING ---
menu_bg_surface = None
loading_bg_surface = None

try:
    # Menu BG
    menu_bg_path = os.path.join(BASE_DIR, "menu_bg.png")
    if os.path.exists(menu_bg_path):
        img = pygame.image.load(menu_bg_path)
        menu_bg_surface = pygame.transform.scale(img, (screen_width, screen_height))
    
    # Loading BG
    loading_path = os.path.join(BASE_DIR, "loading_bg.png")
    if os.path.exists(loading_path):
        img = pygame.image.load(loading_path)
        loading_bg_surface = pygame.transform.scale(img, (screen_width, screen_height))
        
except Exception as e:
    print(f"Loi tai anh nen: {e}")

# Load âm thanh Game Over
try:
    # Đảm bảo đường dẫn đúng: Thư mục Sounds -> file game_over.wav
    game_over_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "game_over.wav"))
    #game_over_sound = pygame.mixer.Sound(os.path.join("game_over.wav"))
    game_over_sound.set_volume(0.5) # Chỉnh âm lượng (0.0 đến 1.0)
except Exception as e:
    print(f"Loi load am thanh game over: {e}")
    game_over_sound = None # Nếu lỗi thì gán bằng None để game không bị crash