#nằm trong constants.py
import pygame
from settings import screen_width, screen_height

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