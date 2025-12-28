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
from constants import (cell_size, number_of_cells, OFFSET, eat_sound, game_over_sound)
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
        # [THÊM] Biến lưu thời điểm mồi đặc biệt xuất hiện để tính 5s
        self.special_spawn_time = 0
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
        #khai báo biến lưu vị trí mồi đặc biệt
        special_pos_data = None
        if self.food.special_position:
            special_pos_data = [int(self.food.special_position.x), int(self.food.special_position.y)]
        # Lưu cả trạng thái game VÀ Skin
        data = {
            "map": self.current_map_name,
            "snake_body": [[int(v.x), int(v.y)] for v in self.snake.body],
            "direction": [int(self.snake.direction.x), int(self.snake.direction.y)],
            "food_pos": [int(self.food.position.x), int(self.food.position.y)],
            # [SỬA] Lưu biến score thực tế thay vì tính theo độ dài
            "score": self.score,
            "food_eat_counter": self.food.eat_counter,
            
            # Lưu vị trí mồi đặc biệt và thời gian đã trôi qua (để load lại tính tiếp)
            "special_food_pos": special_pos_data,
            # Lưu thời gian còn lại (đơn giản hóa thì khi load game cho nó reset 5s cũng được)
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
            #mồi#######################################################################
            food_data = data.get("food_pos", None)
            if food_data:
                self.food.position = Vector2(food_data[0], food_data[1])
                self.food.walls = self.walls 
            # [THÊM] Load mồi đặc biệt
            special_data = data.get("special_food_pos", None)
            if special_data:
                self.food.special_position = Vector2(special_data[0], special_data[1])
                # Nếu load lại game mà có mồi đặc biệt, reset thời gian 5s tính từ lúc load
                self.special_spawn_time = pygame.time.get_ticks()
            else:
                self.food.special_position = None
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
# [THÊM] Kiểm tra thời gian tồn tại của mồi đặc biệt (5 giây = 5000ms)
            if self.food.special_position:
                current_time = pygame.time.get_ticks()
                if current_time - self.special_spawn_time > 5000: # Sau 5 giây
                    self.food.special_position = None # Biến mất
                    
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
        head = self.snake.body[0]

        # --- 1. XỬ LÝ MỒI THƯỜNG (Luôn kiểm tra) ---
        if int(head.x) == int(self.food.position.x) and int(head.y) == int(self.food.position.y):
            # A. Xử lý rắn và điểm
            self.score += 1
            self.snake.add_block() # Mồi thường -> Rắn DÀI RA
            if eat_sound: eat_sound.play()
            
            # B. Xử lý Logic sinh mồi đặc biệt
            self.food.eat_counter += 1 # Đếm số lần ăn
            
            if self.food.eat_counter >= 5:
                # Đủ 5 lần -> Gọi hàm sinh mồi đặc biệt (đã viết bên food.py)
                self.food.spawn_special_food(self.snake.body)
                # Ghi lại thời gian bắt đầu để đếm ngược 5 giây
                self.special_spawn_time = pygame.time.get_ticks() 
                # Reset bộ đếm về 0
                self.food.eat_counter = 0 
            
            # C. Sinh lại mồi thường ở vị trí mới
            self.food.position = self.food.generate_random_pos(self.snake.body)


        # --- 2. XỬ LÝ MỒI ĐẶC BIỆT (Chỉ kiểm tra khi nó đang tồn tại) ---
        if self.food.special_position:
            if int(head.x) == int(self.food.special_position.x) and int(head.y) == int(self.food.special_position.y):
                # A. Xử lý điểm
                self.score += 3 # Mồi xịn cộng 3 điểm
                if eat_sound: eat_sound.play() # Có thể thay bằng sound khác cho vui
                
                # B. QUAN TRỌNG: KHÔNG gọi self.snake.add_block() 
                # -> Rắn KHÔNG dài ra theo yêu cầu
                
                # C. Ăn xong thì xóa mồi đặc biệt đi
                self.food.special_position = None


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
        # 1. Xử lý âm thanh
        if self.game_running: # Chỉ chạy logic này 1 lần khi vừa chết
            
            # Tạm dừng nhạc nền
            pygame.mixer.music.pause() 
            
            if game_over_sound:
                game_over_sound.play()
                
                # Lấy độ dài file âm thanh (tính bằng giây) -> đổi ra mili giây
                sound_length_ms = int(game_over_sound.get_length() * 1000)
                
                # Đặt hẹn giờ: Sau khi hết tiếng (sound_length_ms), gửi tín hiệu USEREVENT + 1
                # Số 1 ở cuối nghĩa là chỉ chạy 1 lần (loops=1)
                pygame.time.set_timer(pygame.USEREVENT + 1, sound_length_ms, 1)
        """# 1. Phát âm thanh ngay khi chết
        if self.game_running and game_over_sound: 
            game_over_sound.play()"""
            #xử lý lưu điểm
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
        pygame.mixer.music.unpause()
        self.load_map(self.current_map_name) 
        self.snake.reset(self.current_spawn_pos) 
        self.food = Food(self.snake.body, self.walls)
        # [THÊM] Reset điểm
        self.score = 0
        self.game_running = True; self.countdown_active = False; self.high_score = self.hs_manager.load()