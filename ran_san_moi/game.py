import pygame
import json
import os
from collections import deque
from pygame.math import Vector2

from maps import LEVELS, SPAWN_POINTS
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
        self.walls = []
        self.current_map_name = "Kinh điển"
        self.current_spawn_pos = (10, 10)
        
        # Load map lần đầu
        self.load_map(self.current_map_name)

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
        
        # Đường dẫn file save (nằm cùng thư mục với game.py)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.save_file = os.path.join(base_dir, "saved_game.json")

    def load_map(self, map_name):
        self.walls = []
        self.current_map_name = map_name
        
        # 1. Lấy tường
        map_data = LEVELS.get(map_name, LEVELS["Kinh điển"])
        for row_idx, row in enumerate(map_data):
            for col_idx, char in enumerate(row):
                if char == '#':
                    self.walls.append(Vector2(col_idx, row_idx))

        # 2. Lấy điểm sinh ra
        self.current_spawn_pos = SPAWN_POINTS.get(map_name, (7, 4))

    # --- HÀM MỚI: LƯU GAME ---
    def save_current_game(self):
        # Chỉ lưu nếu rắn còn sống
        if not self.game_running: 
            return

        data = {
            "map": self.current_map_name,
            "snake_body": [[int(v.x), int(v.y)] for v in self.snake.body], # Lưu list tọa độ
            "direction": [int(self.snake.direction.x), int(self.snake.direction.y)],
            "food_pos": [int(self.food.position.x), int(self.food.position.y)],
            "score": len(self.snake.body) - 3
        }
        
        try:
            with open(self.save_file, 'w') as f:
                json.dump(data, f)
            print("Đã lưu game thành công!")
        except Exception as e:
            print(f"Lỗi khi lưu game: {e}")

    # --- HÀM MỚI: TẢI GAME ---
    def load_saved_game(self):
        if not os.path.exists(self.save_file):
            return False
            
        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)
            
            # 1. Khôi phục Map
            self.load_map(data.get("map", "Kinh điển"))
            
            # 2. Khôi phục Rắn
            body_data = data.get("snake_body", [])
            if body_data:
                self.snake.body = deque([Vector2(p[0], p[1]) for p in body_data])
            
            dir_data = data.get("direction", [1, 0])
            self.snake.direction = Vector2(dir_data[0], dir_data[1])
            
            # 3. Khôi phục Mồi
            food_data = data.get("food_pos", None)
            if food_data:
                self.food.position = Vector2(food_data[0], food_data[1])
                # Cập nhật tường cho food (để lần sau nó random ko bị lỗi)
                self.food.walls = self.walls 
            
            # 4. Các trạng thái khác
            self.game_running = True
            self.start_countdown() # Đếm ngược 3-2-1 cho người chơi chuẩn bị
            return True
            
        except Exception as e:
            print(f"Lỗi khi tải game: {e}")
            return False

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
            self.check_wall_collision() 
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
        # So sánh tọa độ int để tránh lỗi float
        head = self.snake.body[0]
        food = self.food.position
        if int(head.x) == int(food.x) and int(head.y) == int(food.y):
            # Truyền tường vào để Food né ra
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_block()
            if eat_sound:
                eat_sound.play()

    def check_wall_collision(self):
        head = self.snake.body[0]
        for wall in self.walls:
            if int(head.x) == int(wall.x) and int(head.y) == int(wall.y):
                self.game_over()

    def check_self_collision(self):
        body_list = list(self.snake.body)
        # Kiểm tra đầu có trùng với bất kỳ đốt nào trong thân không
        head = body_list[0]
        for block in body_list[1:]:
             if int(head.x) == int(block.x) and int(head.y) == int(block.y):
                self.game_over()

    def game_over(self):
        # Khi thua thì xóa file save để không cho chơi tiếp ván thua này
        if os.path.exists(self.save_file):
            try:
                os.remove(self.save_file)
            except:
                pass
                
        current_score = len(self.snake.body) - 3
        if current_score > self.high_score:
            self.high_score = current_score
            self.hs_manager.save(self.high_score)
        self.game_running = False 

    def reset_game(self):
        self.load_map(self.current_map_name) 
        self.snake.reset(self.current_spawn_pos) 
        self.food = Food(self.snake.body, self.walls)
        self.game_running = True
        self.countdown_active = False
        self.high_score = self.hs_manager.load()