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
from display import screen

from constants import (
    cell_size, number_of_cells, OFFSET, 
    eat_sound, game_over_sound, 
    countdown_sound, eat_special_sound, highscore_sound 
)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.walls = []
        
        # [MỚI] Biến để nhớ map người chơi đã chọn (Cối xay, Hộp...)
        self.gameplay_map_name = "Kinh điển" 
        self.current_map_name = "Kinh điển"
        self.current_spawn_pos = (10, 10)
        
        self.load_map(self.current_map_name)

        self.food = Food(self.snake.body, self.walls)
        self.game_running = True 
        self.score = 0
        self.special_spawn_time = 0
        self.hs_manager = HighScoreManager()
        self.renderer = GameRenderer()
        
        self.high_score = self.hs_manager.load()
        self.record_broken = False
        
        self.pause_button_rect = None 
        self.back_button_rect = None
        self.countdown_active = False
        self.countdown_value = 3
        self.last_countdown_time = 0
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.save_file = os.path.join(base_dir, "saved_game.json")
        
        self.load_skin_only()

    # [SỬA] Thêm tham số is_gameplay để phân biệt load map chơi hay load map nền
    def load_map(self, map_name, is_gameplay=True):
        self.walls = []
        self.current_map_name = map_name
        
        # Nếu đây là lần load map để chơi thật, hãy lưu lại tên map đó
        if is_gameplay:
            self.gameplay_map_name = map_name
            
        map_data = LEVELS.get(map_name, LEVELS["Kinh điển"])
        for row_idx, row in enumerate(map_data):
            for col_idx, char in enumerate(row):
                if char == '#':
                    self.walls.append(Vector2(col_idx, row_idx))
        self.current_spawn_pos = SPAWN_POINTS.get(map_name, (7, 4))

    def save_current_game(self):
        # 1. Chuẩn bị dữ liệu
        self.hs_manager.save(self.high_score)
        special_pos_data = None
        if self.food.special_position:
            special_pos_data = [int(self.food.special_position.x), int(self.food.special_position.y)]
        
        data = {
            "map": self.gameplay_map_name, 
            "snake_body": [[int(v.x), int(v.y)] for v in self.snake.body],
            "direction": [int(self.snake.direction.x), int(self.snake.direction.y)],
            "food_pos": [int(self.food.position.x), int(self.food.position.y)],
            "score": self.score,
            "food_eat_counter": self.food.eat_counter,
            "special_food_pos": special_pos_data,
            "skin_id": self.snake.skin_id,
            "game_running_status": self.game_running,
            "record_broken": self.record_broken
        }
        
        # 2. Thực hiện lưu file (Có in thông báo lỗi)
        try:
            with open(self.save_file, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"----> ĐÃ LƯU GAME THÀNH CÔNG TẠI: {self.save_file}")
        except Exception as e:
            print(f"----> LỖI NGHIÊM TRỌNG KHI LƯU GAME: {e}")

    def load_skin_only(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                self.snake.set_skin(data.get("skin_id", 0))
            except: pass

    def load_saved_game(self):
        if not os.path.exists(self.save_file): return False
        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)
            
            if not data.get("game_running_status", True):
                return False

            # Load map từ file save (Mặc định is_gameplay=True)
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
            
            special_data = data.get("special_food_pos", None)
            if special_data:
                self.food.special_position = Vector2(special_data[0], special_data[1])
                self.special_spawn_time = pygame.time.get_ticks()
            else:
                self.food.special_position = None
            
            self.score = data.get("score", 0)
            self.food.eat_counter = data.get("food_eat_counter", 0)
            
            self.snake.set_skin(data.get("skin_id", 0))
            
            self.game_running = True
            self.record_broken = data.get("record_broken", False)
            self.start_countdown()
            return True
        except: return False

    def start_countdown(self):
        self.countdown_active = True
        self.countdown_value = 3
        self.last_countdown_time = pygame.time.get_ticks()
        if countdown_sound: 
            countdown_sound.play()

    def update(self):
        if self.countdown_active:
            if pygame.time.get_ticks() - self.last_countdown_time >= 1000:
                self.countdown_value -= 1
                self.last_countdown_time = pygame.time.get_ticks()
                if self.countdown_value == 0: 
                    self.countdown_active = False
            return 
        
        if self.game_running:
            self.snake.move_snake(); self.check_eat_food(); self.check_wall_collision(); self.check_self_collision()

            if self.food.special_position:
                current_time = pygame.time.get_ticks()
                if current_time - self.special_spawn_time > 5000: 
                    self.food.special_position = None 
                    
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
        
        if not self.game_running: 
            self.renderer.draw_game_over(self.score)
        
        self.renderer.draw_score(self.score, self.high_score, self.record_broken)
        
        if self.countdown_active: self.renderer.draw_countdown(self.countdown_value)

    def check_eat_food(self):
        head = self.snake.body[0]

        # 1. Ăn mồi thường
        if int(head.x) == int(self.food.position.x) and int(head.y) == int(self.food.position.y):
            self.score += 1
            
            # [MỚI] Cập nhật Điểm cao ngay lập tức để hiển thị
            if self.score > self.high_score:
                self.high_score = self.score
                if not self.record_broken:
                    self.record_broken = True # Đánh dấu đã phá
                    if highscore_sound: 
                        highscore_sound.play() # Phát nhạc TADA!

            self.snake.add_block()
            if eat_sound: eat_sound.play()
            
            self.food.eat_counter += 1
            if self.food.eat_counter >= 5:
                self.food.spawn_special_food(self.snake.body)
                self.special_spawn_time = pygame.time.get_ticks() 
                self.food.eat_counter = 0 
            
            self.food.position = self.food.generate_random_pos(self.snake.body)

        # 2. Ăn mồi đặc biệt
        if self.food.special_position:
            if int(head.x) == int(self.food.special_position.x) and int(head.y) == int(self.food.special_position.y):
                self.score += 3
                
                # [MỚI] Cập nhật Điểm cao ngay lập tức
                if self.score > self.high_score:
                    self.high_score = self.score
                    if not self.record_broken:
                        self.record_broken = True
                        if highscore_sound: highscore_sound.play()

                if eat_special_sound: 
                    eat_special_sound.play()
                elif eat_sound: 
                    eat_sound.play() 
                self.food.special_position = None

    def check_wall_collision(self):
        head = self.snake.body[0]
        for wall in self.walls:
            if int(head.x) == int(wall.x) and int(head.y) == int(wall.y): self.game_over()
            
    def check_self_collision(self):
        head = list(self.snake.body)[0]
        for block in list(self.snake.body)[1:]:
             if int(head.x) == int(block.x) and int(head.y) == int(block.y): self.game_over()

    def game_over(self):
        if self.game_running: 
            pygame.mixer.music.pause() 
            if game_over_sound:
                game_over_sound.play()
                sound_length_ms = int(game_over_sound.get_length() * 1000)
                pygame.time.set_timer(pygame.USEREVENT + 1, sound_length_ms, 1)
            
            # Chuyển về Kinh điển để hiển thị nền sạch
            self.load_map("Kinh điển", is_gameplay=False)
        
        # Xóa file save game dở dang (vì đã thua rồi)
        if os.path.exists(self.save_file):
            try: os.remove(self.save_file)
            except: pass
            
        # [SỬA LỖI QUAN TRỌNG]
        # Luôn lưu điểm cao xuống file (Bỏ điều kiện if score > high_score đi)
        # Vì self.high_score đã được cập nhật liên tục lúc đang chơi rồi.
        try:
            self.hs_manager.save(self.high_score)
            print(f"----> (GAME OVER) ĐÃ LƯU KỶ LỤC: {self.high_score}")
        except Exception as e:
            print(f"----> LỖI LƯU ĐIỂM: {e}")
        
        self.game_running = False

    def reset_game(self):
        pygame.mixer.music.unpause()
        
        # [SỬA] Load lại cái map mà người chơi đã chọn ban đầu (gameplay_map_name)
        # Thay vì load map hiện tại (đang là Kinh điển do Game Over)
        self.load_map(self.gameplay_map_name) 
        
        self.snake.reset(self.current_spawn_pos) 
        self.food = Food(self.snake.body, self.walls)
        self.score = 0
        self.record_broken = False
        file_hs = self.hs_manager.load()
        self.high_score = max(self.high_score, file_hs)
        
        self.starting_high_score = self.high_score
        self.game_running = True; self.countdown_active = False;