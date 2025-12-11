#nằm trong constants.py
import pygame
import os
from settings import (
    BASE_DIR, cell_size, HEAD_SIZE, 
    DARK_GREEN, HEAD_COLOR, screen_width, screen_height
)
# Cần import display để đảm bảo pygame đã init trước khi load ảnh
import display 

# --- TẢI ÂM THANH ---
MUSIC_LOADED = False
eat_sound = None

try:
    music_path = os.path.join(BASE_DIR, "nhac_nen.wav")
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        MUSIC_LOADED = True
    
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

# Background Gameplay
bg_surface = None

# --- TẢI ẢNH NỀN MENU & LOADING ---
menu_bg_surface = None
loading_bg_surface = None

try:
    # Menu BG
    menu_bg_path = os.path.join(BASE_DIR, "menu_bg.jpg")
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