# files/Resources/constants.py
import pygame
import os 
import sys 

def resource_path(relative_path, sub_dir):
    try: base_path = sys._MEIPASS 
    except Exception: base_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    return os.path.join(base_path, sub_dir, relative_path)

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
PROJECT_ROOT = os.path.dirname(BASE_DIR) 

# --- MÀU SẮC ---
GRASS_LIGHT = (170, 215, 81)  
GRASS_DARK  = (162, 209, 73)
BORDER_COLOR = (87, 138, 52) 
GREEN = (173, 204, 96)
YELLOW = (255, 200, 0)
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255) # <--- QUAN TRỌNG: ĐÃ THÊM MÀU TRẮNG
HEAD_COLOR = (255, 60, 60) 
DARK_GREEN = (43, 51, 24) 

cell_size = 25       
number_of_cells = 20 
OFFSET = 75          
HEAD_SCALE_FACTOR = 2.5
HEAD_SIZE = int(cell_size * HEAD_SCALE_FACTOR)
screen_width = 2 * OFFSET + cell_size * number_of_cells
screen_height = 2 * OFFSET + cell_size * number_of_cells

try: pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=128)
except Exception: pass
pygame.init() 
screen = pygame.display.set_mode((screen_width, screen_height)) 
pygame.display.set_caption("Ran_San_Moi")
SCREEN_UPDATE = pygame.USEREVENT

# --- TẢI TÀI NGUYÊN ---
MUSIC_LOADED = False
eat_sound = None
try:
    music_path = resource_path("nhac_nen.wav", sub_dir=os.path.join("Extra", "Sound_DLC"))
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        MUSIC_LOADED = True
    eat_path = resource_path("eat.wav", sub_dir=os.path.join("Extra", "Sound_DLC"))
    if os.path.exists(eat_path):
        eat_sound = pygame.mixer.Sound(eat_path)
        eat_sound.set_volume(1.0)
except Exception: pass

try:
    font_path = resource_path("font_game.ttf", sub_dir=os.path.join("Extra", "Text"))
    font = pygame.font.Font(font_path, 40)
except: font = pygame.font.SysFont('Arial', 40)

try:
    food_path = resource_path("food.png", sub_dir="CDNImage") 
    food_surface = pygame.image.load(food_path)
    food_surface = pygame.transform.scale(food_surface, (cell_size, cell_size)) 
except:
    food_surface = pygame.Surface((cell_size, cell_size)); food_surface.fill(DARK_GREEN) 
    
try:
    head_path = resource_path("dauran.png", sub_dir="CDNImage")
    snake_head_surface = pygame.image.load(head_path).convert_alpha()
    snake_head_surface = pygame.transform.scale(snake_head_surface, (HEAD_SIZE, HEAD_SIZE))
    pygame.display.set_icon(snake_head_surface)
except:
    snake_head_surface = pygame.Surface((HEAD_SIZE, HEAD_SIZE)); snake_head_surface.fill(HEAD_COLOR)

bg_surface = None
menu_bg_surface = None
loading_bg_surface = None

try:
    menu_bg_path = resource_path("menu_bg.jpg", sub_dir="CDNImage")
    if os.path.exists(menu_bg_path):
        img = pygame.image.load(menu_bg_path)
        menu_bg_surface = pygame.transform.scale(img, (screen_width, screen_height))
        
    loading_path = resource_path("loading_bg.png", sub_dir="CDNImage")
    if os.path.exists(loading_path):
        img = pygame.image.load(loading_path)
        loading_bg_surface = pygame.transform.scale(img, (screen_width, screen_height))
except Exception: pass