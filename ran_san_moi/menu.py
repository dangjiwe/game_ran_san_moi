#menu.py
import pygame
import sys
import constants
from menu_renderer import MenuRenderer

class Menu:
    def __init__(self, high_score_data):
        self.renderer = MenuRenderer() # Khởi tạo thợ vẽ
        self.is_active = True
        self.high_score_data = high_score_data 
        
        # Data Menu chính
        self.options = ["CHƠI MỚI", "CHƠI TIẾP", "ĐIỂM CAO", "HƯỚNG DẪN", "CÀI ĐẶT", "THOÁT"]
        self.selected_index = 0
        self.option_rects = [] # Lưu vị trí nút để bấm chuột
        
        # Các cờ màn hình
        self.show_high_score = False 
        self.show_settings = False
        self.show_tutorial = False
        self.show_mode_selection = False
        self.show_challenge_popup = False
        self.show_no_save_popup = False 
        
        # Data màn hình chọn chế độ
        self.mode_options = ["CƠ BẢN", "THỬ THÁCH"]
        self.mode_index = 0
        self.mode_rects = []
        
        # Nút và trạng thái chuột
        self.back_button_rect = None
        self.btn_vol_down = None
        self.btn_vol_up = None
        
        # Cờ game
        self.start_game_trigger = False

        # Âm thanh
        self.volume = 0.5 
        self.update_volume()
#thêm đoạn này để  có tiếng bấm nút
    def play_click(self):
        if constants.click_sound:
            constants.click_sound.play()

    def update_volume(self):
        try: pygame.mixer.music.set_volume(self.volume)
        except: pass
        if constants.eat_sound: constants.eat_sound.set_volume(self.volume)
        # --- CẬP NHẬT VOLUME CHO TIẾNG CLICK ---
        if constants.click_sound: constants.click_sound.set_volume(self.volume)

    def handle_input(self, event, game_object):
        # 1. Xử lý đóng Popup
        if self.show_challenge_popup or self.show_no_save_popup:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                ###############################################
                self.play_click() # <--- Kêu khi đóng popup
                self.show_challenge_popup = False
                self.show_no_save_popup = False 
            return

        # 2. Xử lý màn hình phụ (Hướng dẫn / Điểm cao)
        if self.show_tutorial or self.show_high_score:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
                self.play_click() # <--- Kêu khi nhấn ESC
                self.show_tutorial = False; self.show_high_score = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button_rect and self.back_button_rect.collidepoint(event.pos): 
                    self.play_click() # <--- Kêu khi nhấn ESC
                    self.show_tutorial = False; self.show_high_score = False
            return

        # 3. Xử lý Cài đặt
        if self.show_settings:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.show_settings = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button_rect and self.back_button_rect.collidepoint(event.pos):
                    self.show_settings = False
                elif self.btn_vol_down and self.btn_vol_down.collidepoint(event.pos):
                    self.play_click() # <--- Kêu khi giảm âm lượng
                    self.volume = max(0.0, self.volume - 0.1); self.update_volume()
                elif self.btn_vol_up and self.btn_vol_up.collidepoint(event.pos):
                    self.play_click() # <--- Kêu khi tăng âm lượng
                    self.volume = min(1.0, self.volume + 0.1); self.update_volume()
            return

        # 4. Xử lý Chọn chế độ
        if self.show_mode_selection:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: self.show_mode_selection = False 
                elif event.key == pygame.K_DOWN: self.mode_index = (self.mode_index + 1) % len(self.mode_options)
                elif event.key == pygame.K_UP: self.mode_index = (self.mode_index - 1) % len(self.mode_options)
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]: 
                    self.play_click() # <--- Kêu khi chọn bằng phím
                    self.execute_mode_choice(game_object)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for index, rect in enumerate(self.mode_rects):
                    if rect.collidepoint(event.pos): 
                        self.play_click() # <--- Kêu khi chọn bằng chuột
                        self.mode_index = index; self.execute_mode_choice(game_object); break
                if self.back_button_rect and self.back_button_rect.collidepoint(event.pos): 
                    self.show_mode_selection = False
            
            elif event.type == pygame.MOUSEMOTION:
                for index, rect in enumerate(self.mode_rects):
                    if rect.collidepoint(event.pos): self.mode_index = index; break
            return 

        # 5. Xử lý Menu Chính
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN: self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_UP: self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE]: 
                self.play_click() # <--- Kêu khi nhấn Enter/Space
                self.execute_option(game_object)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for index, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos): 
                    self.play_click() # <--- Kêu khi click menu chính
                    self.selected_index = index; self.execute_option(game_object); break
        
        elif event.type == pygame.MOUSEMOTION:
            for index, rect in enumerate(self.option_rects):
                 if rect.collidepoint(event.pos): self.selected_index = index; break

    def execute_option(self, game_object):
        sel = self.options[self.selected_index]
        if sel == "CHƠI MỚI": 
            self.show_mode_selection = True; self.mode_index = 0
        elif sel == "CHƠI TIẾP":
            if len(game_object.snake.body) > 3 or game_object.snake.body[0].x != 6: self.is_active = False
            else:
                success = game_object.load_saved_game()
                if success: self.is_active = False
                else: self.show_no_save_popup = True 
        elif sel == "ĐIỂM CAO": self.show_high_score = True
        elif sel == "HƯỚNG DẪN": self.show_tutorial = True
        elif sel == "CÀI ĐẶT": self.show_settings = True
        elif sel == "THOÁT": 
            if game_object.game_running: game_object.save_current_game()
            pygame.quit(); sys.exit()

    def execute_mode_choice(self, game_object):
        choice = self.mode_options[self.mode_index]
        if choice == "CƠ BẢN": 
            game_object.reset_game()
            self.show_mode_selection = False
            self.is_active = False 
            self.start_game_trigger = True 
        elif choice == "THỬ THÁCH": 
            self.show_challenge_popup = True

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        hover_hand = False # Biến kiểm tra để đổi con trỏ chuột

        # 1. Vẽ Popup (Đè lên trên cùng nếu có)
        if self.show_challenge_popup:
            # Vẽ nền chế độ trước
            self.renderer.draw_mode_selection(self.mode_index, self.mode_options, mouse_pos)
            self.renderer.draw_popup("CHẾ ĐỘ THỬ THÁCH", "ĐANG PHÁT TRIỂN...", "(Sẽ sớm ra mắt)")
            pygame.display.update(); return
            
        if self.show_no_save_popup:
            self.renderer.draw_main_menu(self.selected_index, self.options, mouse_pos)
            self.renderer.draw_popup("KHÔNG CÓ DỮ LIỆU!", "Bạn chưa lưu game nào.")
            pygame.display.update(); return

        # 2. Vẽ màn hình Điểm cao
        if self.show_high_score:
            self.back_button_rect = self.renderer.draw_high_score(self.high_score_data)
            if self.back_button_rect.collidepoint(mouse_pos): hover_hand = True
            
        # 3. Vẽ màn hình Cài đặt
        elif self.show_settings:
            self.btn_vol_down, self.btn_vol_up, self.back_button_rect = self.renderer.draw_settings(self.volume, mouse_pos)
            if (self.back_button_rect.collidepoint(mouse_pos) or 
                self.btn_vol_down.collidepoint(mouse_pos) or 
                self.btn_vol_up.collidepoint(mouse_pos)):
                hover_hand = True
            
        # 4. Vẽ màn hình Hướng dẫn
        elif self.show_tutorial:
            self.back_button_rect = self.renderer.draw_tutorial()
            if self.back_button_rect.collidepoint(mouse_pos): hover_hand = True
            
        # 5. Vẽ màn hình Chọn chế độ
        elif self.show_mode_selection:
            self.mode_rects, self.back_button_rect = self.renderer.draw_mode_selection(self.mode_index, self.mode_options, mouse_pos)
            # Kiểm tra hover nút back
            if self.back_button_rect.collidepoint(mouse_pos): hover_hand = True
            # Kiểm tra hover các nút chế độ
            for rect in self.mode_rects:
                if rect.collidepoint(mouse_pos): hover_hand = True

        # 6. Vẽ Menu Chính
        else:
            self.option_rects = self.renderer.draw_main_menu(self.selected_index, self.options, mouse_pos)
            for rect in self.option_rects:
                if rect.collidepoint(mouse_pos): hover_hand = True

        # Đổi con trỏ chuột
        if hover_hand: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.update()