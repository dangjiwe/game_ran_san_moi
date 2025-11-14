import pygame, sys, random
from pygame.math import Vector2

pygame.init()

GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)
YELLOW = (255, 200, 0)
BLACK = (0, 0, 0) 

cell_size = 25
number_of_cells = 20
OFFSET = 75

HEAD_SCALE_FACTOR = 2.5
HEAD_SIZE = int(cell_size * HEAD_SCALE_FACTOR)
HEAD_COLOR = (255, 60, 60) 

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)

    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, 
            cell_size, cell_size)
        screen.blit(food_surface, food_rect)

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells-1)
        y = random.randint(0, number_of_cells-1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position
class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1, 0)

    def draw(self):
   
        for index, segment in enumerate(self.body[1:]): 
            segment_rect = (OFFSET + segment.x * cell_size, 
                            OFFSET + segment.y * cell_size, 
                            cell_size, cell_size)
        
            if index % 2 == 0:
                color = YELLOW
            else:
                color = BLACK
                
            pygame.draw.rect(screen, color, segment_rect, 0, 7)

        head_segment = self.body[0]
        
        offset_adjust = (HEAD_SIZE - cell_size) // 2 
        
        head_rect = pygame.Rect(OFFSET + head_segment.x * cell_size - offset_adjust, 
                                OFFSET + head_segment.y * cell_size - offset_adjust, 
                                HEAD_SIZE, HEAD_SIZE)
        
     
        rotated_head = self.rotate_head_image()
        screen.blit(rotated_head, head_rect)

    def rotate_head_image(self):
        angle = 0
        if self.direction == Vector2(1, 0):  
            angle = 270
        elif self.direction == Vector2(-1, 0): 
            angle = 90
        elif self.direction == Vector2(0, -1): 
            angle = 0
        elif self.direction == Vector2(0, 1):  
            angle = 180
        
        return pygame.transform.rotate(snake_head_surface, angle)
    

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)

    def draw(self):
        self.food.draw()
        self.snake.draw()

screen_width = 2*OFFSET + cell_size*number_of_cells
screen_height = 2*OFFSET + cell_size*number_of_cells
screen = pygame.display.set_mode((screen_width, screen_height)) 
pygame.display.set_caption("Ran_San_Moi_Static")

try:
    food_surface = pygame.image.load("food.png")
    food_surface = pygame.transform.scale(food_surface, (cell_size, cell_size)) 
except pygame.error:
    print("Lỗi: Không tìm thấy file 'food.png'. Sử dụng màu mặc định.")
    food_surface = pygame.Surface((cell_size, cell_size))
    food_surface.fill(DARK_GREEN) 
    
try:
    snake_head_surface = pygame.image.load("dauran.png").convert_alpha()
    snake_head_surface = pygame.transform.scale(snake_head_surface, (HEAD_SIZE, HEAD_SIZE))
except pygame.error:
    print("Lỗi: Không tìm thấy file 'dauran.png'. Sử dụng màu mặc định.")
    snake_head_surface = pygame.Surface((HEAD_SIZE, HEAD_SIZE))
    snake_head_surface.fill(HEAD_COLOR) 

game = Game()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
   
    screen.fill(GREEN)
    
   
    pygame.draw.rect(screen, DARK_GREEN, 
        (OFFSET-5, OFFSET-5, cell_size*number_of_cells+10, cell_size*number_of_cells+10), 5)
        
    game.draw()
    
    
    pygame.display.update()
