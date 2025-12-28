#game.py
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
from constants import (cell_size, number_of_cells, OFFSET, eat_sound)
from display import screen

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
# [THÊM] Biến điểm số riêng, không phụ thuộc độ dài rắn nữa
        self.score = 0
        self.hs_manager = HighScoreManager()
        self.renderer = GameRenderer()
        
        self.high_score = self.hs_manager.load()
        
        self.pause_button_rect = None 
        self.back_button_rect = None
        self.countdown_active = False
        self.countdown_value = 3
        self.last_countdown_time = 0
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.save_file = os.path.join(base_dir, "saved_game.json")
        
        # Tự động tải skin từ file save (nếu có) ngay khi mở game
        self.load_skin_only()

    def load_map(self, map_name):
        self.walls = []
        self.current_map_name = map_name
        map_data = LEVELS.get(map_name, LEVELS["Kinh điển"])
        for row_idx, row in enumerate(map_data):
            for col_idx, char in enumerate(row):
                if char == '#':
                    self.walls.append(Vector2(col_idx, row_idx))
        self.current_spawn_pos = SPAWN_POINTS.get(map_name, (7, 4))
########################################################################
    def save_current_game(self):
        # Lưu cả trạng thái game VÀ Skin
        data = {
            "map": self.current_map_name,
            "snake_body": [[int(v.x), int(v.y)] for v in self.snake.body],
            "direction": [int(self.snake.direction.x), int(self.snake.direction.y)],
            "food_pos": [int(self.food.position.x), int(self.food.position.y)],
            # [SỬA] Lưu biến score thực tế thay vì tính theo độ dài
            "score": self.score,
            #"score": len(self.snake.body) - 3,
            "skin_id": self.snake.skin_id, # <--- Lưu Skin
            "game_running_status": self.game_running # Lưu trạng thái sống/chết
        }
        try:
            with open(self.save_file, 'w') as f:
                json.dump(data, f)
        except Exception: pass

    def load_skin_only(self):
        """Chỉ đọc skin từ file save để áp dụng cho Menu, không load game dở"""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                self.snake.set_skin(data.get("skin_id", 0))
            except: pass
########################################################################
    def load_saved_game(self):
        if not os.path.exists(self.save_file): return False
        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)
            
            # Kiểm tra nếu save cũ rắn đã chết thì không load để chơi tiếp
            if not data.get("game_running_status", True):
                return False

            self.load_map(data.get("map", "Kinh điển"))
            
            body_data = data.get("snake_body", [])
            if body_data:
                self.snake.body = deque([Vector2(p[0], p[1]) for p in body_data])
            
            dir_data = data.get("direction", [1, 0])
            self.snake.direction = Vector2(dir_data[0], dir_data[1])
            
            food_data = data.get("food_pos", None)
            if food_data:
                self.food.position = Vector2(food_data[0], food_data[1])
                self.food.walls = self.walls 
            # [SỬA] Load điểm số
            self.score = data.get("score", 0)
# [THÊM] Khôi phục trạng thái cục mồi
            self.food.eat_counter = data.get("food_eat_counter", 0)
            self.food.is_special = data.get("food_is_special", False)
            # Load Skin
            self.snake.set_skin(data.get("skin_id", 0))
            
            self.game_running = True
            self.start_countdown()
            return True
        except: return False

    # ... (Giữ nguyên các hàm start_countdown, update, draw_elements, check..., game_over)
    # Copy các hàm còn lại từ file cũ sang đây (chúng không thay đổi)
    def start_countdown(self):
        self.countdown_active = True; self.countdown_value = 3; self.last_countdown_time = pygame.time.get_ticks()
    def update(self):
        if self.countdown_active:
            if pygame.time.get_ticks() - self.last_countdown_time >= 1000:
                self.countdown_value -= 1; self.last_countdown_time = pygame.time.get_ticks()
                if self.countdown_value == 0: self.countdown_active = False
            return 
        if self.game_running:
            self.snake.move_snake(); self.check_eat_food(); self.check_wall_collision(); self.check_self_collision()

########################################################################
    def draw_elements(self, screen, is_paused):
        self.renderer.draw_grass(); self.renderer.draw_wall(self.walls)
        if self.game_running or is_paused:
            btn_y = OFFSET + (cell_size * number_of_cells) + 15
            pause_txt = "TẠM DỪNG" if not is_paused else "TIẾP TỤC"
            self.pause_button_rect = self.renderer.draw_button(pause_txt, OFFSET, btn_y)
            self.back_button_rect = self.renderer.draw_button("QUAY LẠI", OFFSET + self.pause_button_rect.width + 20, btn_y)

        if self.game_running and not is_paused:
            self.food.draw(screen); self.snake.draw()
        elif is_paused: self.renderer.draw_paused_msg()
        if not self.game_running: self.renderer.draw_game_over()
        #current_score = len(self.snake.body) - 3
        # [SỬA] Dùng biến self.score để hiển thị thay vì tính toán
        self.renderer.draw_score(self.score, self.high_score)
        #self.renderer.draw_score(current_score, self.high_score)
        if self.countdown_active: self.renderer.draw_countdown(self.countdown_value)




    def check_eat_food(self):
        if int(self.snake.body[0].x) == int(self.food.position.x) and int(self.snake.body[0].y) == int(self.food.position.y):

# [SỬA] Kiểm tra loại mồi để cộng điểm
            if self.food.is_special:
                self.score += 3  # Mồi xịn cộng 3 điểm
                # Có thể thêm âm thanh riêng: special_eat_sound.play()
            else:
                self.score += 1  # Mồi thường cộng 1 điểm
            self.food.position = self.food.generate_random_pos(self.snake.body); self.snake.add_block()
            if eat_sound: eat_sound.play()


    def check_wall_collision(self):
        head = self.snake.body[0]
        for wall in self.walls:
            if int(head.x) == int(wall.x) and int(head.y) == int(wall.y): self.game_over()
    def check_self_collision(self):
        head = list(self.snake.body)[0]
        for block in list(self.snake.body)[1:]:
             if int(head.x) == int(block.x) and int(head.y) == int(block.y): self.game_over()
###################
#sửa cách tính điểm trong hàm game_over và reset_game
    def game_over(self):
        if os.path.exists(self.save_file):
            try: os.remove(self.save_file)
            except: pass
            # [SỬA] So sánh trực tiếp
        if self.score > self.high_score: 
            self.high_score = self.score
            self.hs_manager.save(self.high_score)
        '''
        current_score = len(self.snake.body) - 3
        if current_score > self.high_score: self.high_score = current_score; self.hs_manager.save(self.high_score)'''
        self.game_running = False 
    def reset_game(self):
        self.load_map(self.current_map_name) 
        self.snake.reset(self.current_spawn_pos) 
        self.food = Food(self.snake.body, self.walls)
        # [THÊM] Reset điểm
        self.score = 0
        self.game_running = True; self.countdown_active = False; self.high_score = self.hs_manager.load()