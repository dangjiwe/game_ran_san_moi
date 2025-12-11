#nằm trong constants.py
import os

# --- ĐƯỜNG DẪN ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = BASE_DIR 

# --- MÀU SẮC ---
GRASS_LIGHT = (170, 215, 81)  
GRASS_DARK  = (162, 209, 73)
BORDER_COLOR = (87, 138, 52) 
GREEN = (173, 204, 96)
YELLOW = (255, 200, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0) 
HEAD_COLOR = (255, 60, 60) 
DARK_GREEN = (43, 51, 24) 

# --- KÍCH THƯỚC GAME ---
cell_size = 25       
number_of_cells = 20 
OFFSET = 75          

HEAD_SCALE_FACTOR = 2.5
HEAD_SIZE = int(cell_size * HEAD_SCALE_FACTOR)

screen_width = 2 * OFFSET + cell_size * number_of_cells
screen_height = 2 * OFFSET + cell_size * number_of_cells