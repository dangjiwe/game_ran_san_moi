from snake import Snake
from food import Food
from highscore import HighScoreManager 
from pygame.math import Vector2
from constants import screen, GRASS_LIGHT, GRASS_DARK, BORDER_COLOR, DARK_GREEN, cell_size, number_of_cells, OFFSET, font, screen_width, screen_height, BLACK, bg_surface, eat_sound, WHITE
import pygame
import math

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.game_running = True 
        
        self.hs_manager = HighScoreManager()
        self.high_score = self.hs_manager.load()
        
        self.pause_button_rect = None 
        self.back_button_rect = None
        self.go_home_rect = None
        self.go_replay_rect = None
        self.countdown_active = False
        self.countdown_value = 3
        self.last_countdown_time = 0
        
        # Biến cờ chuột
        self.should_show_hand = False

    def save_current_game(self):
        data = {
            'snake_body': [[b.x, b.y] for b in self.snake.body],
            'snake_direction': [self.snake.direction.x, self.snake.direction.y],
            'food_position': [self.food.position.x, self.food.position.y],
            'current_score': len(self.snake.body) - 3,
            'high_score': self.high_score
        }
        self.hs_manager.save_game_state(data)

    def load_saved_game(self):
        data = self.hs_manager.load_game_state()
        if data and 'snake_body' in data and len(data['snake_body']) > 0:
            try:
                self.snake.body = [Vector2(pos[0], pos[1]) for pos in data['snake_body']]
                d = data['snake_direction']
                self.snake.direction = Vector2(d[0], d[1])
                f = data['food_position']
                self.food.position = Vector2(f[0], f[1])
                self.high_score = data.get('high_score', self.high_score)
                self.game_running = True 
                self.countdown_active = False
                print("----> Load thanh cong!")
                return True
            except:
                self.reset_game()
                return False
        else:
            print("----> File save rong!")
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
                if self.countdown_value == 0: self.countdown_active = False
            return 
        if self.game_running:
            self.snake.move_snake()
            self.check_eat_food()
            self.check_wall_collision()
            self.check_self_collision()

    def draw_elements(self, is_paused):
        # 1. Reset cờ
        self.should_show_hand = False

        self.draw_grass() 
        if self.game_running or is_paused:
            btn_y = screen_height - OFFSET + 15
            pause_txt = "TẠM DỪNG" if not is_paused else "TIẾP TỤC"
            self.pause_button_rect = self.draw_button(pause_txt, OFFSET, btn_y)
            back_x = OFFSET + self.pause_button_rect.width + 20
            self.back_button_rect = self.draw_button("QUAY LẠI", back_x, btn_y)

        if self.game_running and not is_paused:
            self.food.draw()
            self.snake.draw()
        elif is_paused:
            self.draw_paused_msg()
            
        if not self.game_running and not self.countdown_active:
            self.draw_game_over_ui()
        
        self.draw_score() 
        if self.countdown_active: self.draw_countdown()
        
        # 2. Áp dụng con trỏ cuối cùng
        self.apply_cursor()

    def apply_cursor(self):
        if self.should_show_hand:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw_grass(self):
        if bg_surface: screen.blit(bg_surface, (0, 0))
        else:
            screen.fill(BORDER_COLOR)
            for row in range(number_of_cells):
                for col in range(number_of_cells):
                    rect = pygame.Rect(OFFSET+col*cell_size, OFFSET+row*cell_size, cell_size, cell_size)
                    color = GRASS_LIGHT if (row+col)%2==0 else GRASS_DARK
                    pygame.draw.rect(screen, color, rect)

    def draw_button(self, text, x_offset, y_pos):
        text_surf = font.render(text, True, BLACK)
        button_w = text_surf.get_width() + 30
        button_h = text_surf.get_height() + 10
        rect = pygame.Rect(x_offset, y_pos, button_w, button_h)
        mouse_pos = pygame.mouse.get_pos()
        
        # Chỉ bật cờ, không đổi ngay
        if rect.collidepoint(mouse_pos):
            color = (220, 220, 220)
            self.should_show_hand = True
        else:
            color = (200, 200, 200)
            
        pygame.draw.rect(screen, color, rect, 0, 8) 
        pygame.draw.rect(screen, BLACK, rect, 2, 8)
        screen.blit(text_surf, text_surf.get_rect(center=rect.center))
        return rect

    def draw_game_over_ui(self):
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(150); overlay.fill(BLACK)
        screen.blit(overlay, (0,0))
        l1 = font.render("GAME OVER!", True, (255, 50, 50))
        cy = screen_height // 2
        screen.blit(l1, l1.get_rect(center=(screen_width//2, cy - 80)))

        self.go_replay_rect = pygame.Rect(0, 0, 80, 80)
        self.go_replay_rect.center = (screen_width//2 + 60, cy + 20)
        self.draw_circle_button(self.go_replay_rect, "replay")

        self.go_home_rect = pygame.Rect(0, 0, 80, 80)
        self.go_home_rect.center = (screen_width//2 - 60, cy + 20)
        self.draw_circle_button(self.go_home_rect, "home")

        tips = font.render("Bấm để chọn", True, WHITE)
        tips = pygame.transform.scale(tips, (int(tips.get_width()*0.7), int(tips.get_height()*0.7)))
        screen.blit(tips, tips.get_rect(center=(screen_width//2, cy + 90)))

    def draw_circle_button(self, rect, icon_type):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)
        
        if is_hover: 
            self.should_show_hand = True
            color = (200, 255, 200)
        else:
            color = (255, 255, 255)

        pygame.draw.circle(screen, color, rect.center, 40)
        pygame.draw.circle(screen, BLACK, rect.center, 40, 3)
        cx, cy = rect.center
        if icon_type == "home":
            pygame.draw.polygon(screen, BLACK, [(cx, cy-20), (cx-15, cy-5), (cx+15, cy-5)])
            pygame.draw.rect(screen, BLACK, (cx-10, cy-5, 20, 20))
            pygame.draw.rect(screen, WHITE, (cx-3, cy+5, 6, 10))
        elif icon_type == "replay":
            rect_arc = pygame.Rect(cx-15, cy-15, 30, 30)
            pygame.draw.arc(screen, BLACK, rect_arc, 0, 1.5*3.14, 3)
            pygame.draw.polygon(screen, BLACK, [(cx+10, cy-5), (cx+20, cy), (cx+10, cy+5)])

    # ... (Các hàm còn lại như draw_countdown, draw_score... giữ nguyên) ...
    def draw_countdown(self):
        txt = str(self.countdown_value)
        try: big_font = pygame.font.Font(font, 150) 
        except: big_font = pygame.font.SysFont('Arial', 150)
        surf = big_font.render(txt, True, WHITE)
        outline = big_font.render(txt, True, BLACK)
        rect = surf.get_rect(center=(screen_width//2, screen_height//2))
        screen.blit(outline, (rect.x+2, rect.y+2))
        screen.blit(surf, rect)

    def draw_paused_msg(self):
        surf = font.render("TẠM DỪNG", True, (0, 0, 255))
        grid_center = (OFFSET + (cell_size * number_of_cells)//2)
        screen.blit(surf, surf.get_rect(center=(grid_center, grid_center)))

    def draw_score(self):
        score = len(self.snake.body) - 3
        s_surf = font.render(f"ĐIỂM: {score}", True, DARK_GREEN)
        screen.blit(s_surf, (screen_width - OFFSET - s_surf.get_width(), OFFSET - 50))
        h_surf = font.render(f"ĐIỂM CAO NHẤT: {self.high_score}", True, DARK_GREEN)
        screen.blit(h_surf, (OFFSET, OFFSET - 50))

    def check_eat_food(self):
        if self.food.position == self.snake.body[0]:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_block()
            if eat_sound: eat_sound.play()

    def check_wall_collision(self):
        head = self.snake.body[0]
        if not (0 <= head.x < number_of_cells and 0 <= head.y < number_of_cells):
            self.game_over()

    def check_self_collision(self):
        if self.snake.body[0] in self.snake.body[1:]:
            self.game_over()

    def game_over(self):
        current_score = len(self.snake.body) - 3
        if current_score > self.high_score:
            self.high_score = current_score
            self.hs_manager.save(self.high_score)
        self.hs_manager.clear_saved_game()
        self.game_running = False 

    def reset_game(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.game_running = True
        self.countdown_active = False
        self.high_score = self.hs_manager.load()