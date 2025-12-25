import pygame
from maps import MAP_BOX
from snake import Snake
from food import Food
from highscore import HighScoreManager
from game_renderer import GameRenderer  
from constants import (
    cell_size, number_of_cells, OFFSET, eat_sound
)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.walls =[]
        for row_idx, row in enumerate(MAP_BOX):
            for col_idx, char in enumerate(row):
                if char == '#':
                    self.walls.append(pygame.math.Vector2(col_idx, row_idx))
        self.food = Food(self.snake.body, self.walls)
        self.game_running = True 

        self.hs_manager = HighScoreManager()
        self.renderer = GameRenderer()
        
        self.high_score = self.hs_manager.load()
        
        self.pause_button_rect = None 
        self.back_button_rect = None
        
        self.countdown_active = False
        self.countdown_value = 3
        self.last_countdown_time = 0

    def start_countdown(self):
        self.countdown_active = True
        self.countdown_value = 3
        self.last_countdown_time = pygame.time.get_ticks()

    def update(self):
        if self.countdown_active:
            if pygame.time.get_ticks() - self.last_countdown_time >= 1000:
                self.countdown_value -= 1
                self.last_countdown_time = pygame.time.get_ticks()
                if self.countdown_value == 0:
                    self.countdown_active = False
            return 

        if self.game_running:
            self.snake.move_snake()
            self.check_eat_food()
            self.check_wall_collision() # Xử lý xuyên tường
            self.check_self_collision()

    def draw_elements(self, is_paused):
        self.renderer.draw_grass()
        self.renderer.draw_wall(self.walls)
        if self.game_running or is_paused:
            grid_bottom = OFFSET + (cell_size * number_of_cells)
            btn_y = grid_bottom + 15
            pause_txt = "TẠM DỪNG" if not is_paused else "TIẾP TỤC"
            
            self.pause_button_rect = self.renderer.draw_button(pause_txt, OFFSET, btn_y)
            
            back_x = OFFSET + self.pause_button_rect.width + 20
            self.back_button_rect = self.renderer.draw_button("QUAY LẠI", back_x, btn_y)

        if self.game_running and not is_paused:
            self.food.draw()
            self.snake.draw()
        elif is_paused:
            self.renderer.draw_paused_msg()
            
        if not self.game_running:
            self.renderer.draw_game_over()
        
        current_score = len(self.snake.body) - 3
        self.renderer.draw_score(current_score, self.high_score)
        
        if self.countdown_active:
            self.renderer.draw_countdown(self.countdown_value)

    def check_eat_food(self):
        if self.food.position == self.snake.body[0]:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_block()
            if eat_sound:
                eat_sound.play()

    def check_wall_collision(self):
        """
        Xử lý xuyên tường: Nếu đi quá mép này sẽ xuất hiện ở mép kia.
        """
        head = self.snake.body[0]
        
        # Xuyên chiều ngang (Trái <-> Phải)
        if head.x < 0:
            head.x = number_of_cells - 1
        elif head.x >= number_of_cells:
            head.x = 0
        
        # Xuyên chiều dọc (Trên <-> Dưới)
        if head.y < 0:
            head.y = number_of_cells - 1
        elif head.y >= number_of_cells:
            head.y = 0
        
        for wall in self.walls:
            if int(head.x) == int(wall.x) and int(head.y) == int(wall.y):
                self.game_over()

    def check_self_collision(self):
        body_list = list(self.snake.body)
        if body_list[0] in body_list[1:]:
            self.game_over()

    def game_over(self):
        current_score = len(self.snake.body) - 3
        if current_score > self.high_score:
            self.high_score = current_score
            self.hs_manager.save(self.high_score)
        self.game_running = False 

    def reset_game(self):
        self.snake.reset()
        #self.food.position = self.food.generate_random_pos(self.snake.body)
        self.food = Food(self.snake.body, self.walls)
        self.game_running = True
        self.countdown_active = False
        self.high_score = self.hs_manager.load()