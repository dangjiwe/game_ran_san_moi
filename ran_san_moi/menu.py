import pygame
import sys
import constants
from menu_renderer import MenuRenderer

class Menu:
    def __init__(self, high_score_data):
        self.renderer = MenuRenderer() 
        self.is_active = True
        self.high_score_data = high_score_data 
        
        # Data Menu chính
        self.options = ["CHƠI MỚI", "CHƠI TIẾP", "ĐIỂM CAO", "HƯỚNG DẪN", "CÀI ĐẶT", "THOÁT"]
        self.selected_index = 0
        self.option_rects = [] 
        
        # --- CÁC MÀN HÌNH PHỤ ---
        self.show_high_score = False 
        self.show_settings = False
        self.show_tutorial = False
        self.show_no_save_popup = False 
        
        # --- MÀN HÌNH CHỌN MAP (Mới) ---
        self.map_names = ["Kinh điển", "Hộp", "Đường hầm", "Cối xay", "Đường ray", "Chung cư"]
        self.map_index = 0
        self.show_map_selection = False 
        self.map_rects = []

        # Nút và trạng thái chuột
        self.back_button_rect = None
        self.btn_vol_down = None
        self.btn_vol_up = None
        
        # Âm thanh
        self.volume = 1.0 
        self.update_volume()

    def play_click(self):
        if constants.click_sound:
            constants.click_sound.play()

    def update_volume(self):
        try: pygame.mixer.music.set_volume(self.volume)
        except: pass
        if constants.eat_sound: constants.eat_sound.set_volume(self.volume)
        if constants.click_sound: constants.click_sound.set_volume(self.volume)

    def handle_input(self, event, game_object):
        # 1. Xử lý đóng Popup (Chỉ còn popup báo lỗi không có save)
        if self.show_no_save_popup:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.play_click()
                self.show_no_save_popup = False 
            return

        # 2. Xử lý màn hình phụ (Hướng dẫn / Điểm cao)
        if self.show_tutorial or self.show_high_score:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
                self.play_click(); self.show_tutorial = False; self.show_high_score = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button_rect and self.back_button_rect.collidepoint(event.pos): 
                    self.play_click(); self.show_tutorial = False; self.show_high_score = False
            return

        # 3. Xử lý Cài đặt
        if self.show_settings:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.show_settings = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button_rect and self.back_button_rect.collidepoint(event.pos):
                    self.show_settings = False
                elif self.btn_vol_down and self.btn_vol_down.collidepoint(event.pos):
                    self.play_click(); self.volume = max(0.0, self.volume - 0.1); self.update_volume()
                elif self.btn_vol_up and self.btn_vol_up.collidepoint(event.pos):
                    self.play_click(); self.volume = min(1.0, self.volume + 0.1); self.update_volume()
            return

        # 4. Xử lý CHỌN MAP (Thay thế cho chọn Mode cũ)
        if self.show_map_selection:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    self.show_map_selection = False 
                elif event.key == pygame.K_RIGHT: 
                    self.map_index = min(self.map_index + 1, len(self.map_names) - 1)
                elif event.key == pygame.K_LEFT: 
                    self.map_index = max(self.map_index - 1, 0)
                elif event.key == pygame.K_DOWN: 
                    self.map_index = min(self.map_index + 2, len(self.map_names) - 1)
                elif event.key == pygame.K_UP: 
                    self.map_index = max(self.map_index - 2, 0)
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]: 
                    self.play_click(); self.start_game_with_map(game_object)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for index, rect in enumerate(self.map_rects):
                    if rect.collidepoint(event.pos): 
                        self.play_click(); self.map_index = index
                        self.start_game_with_map(game_object)
                        break
                if self.back_button_rect and self.back_button_rect.collidepoint(event.pos): 
                    self.show_map_selection = False
            
            elif event.type == pygame.MOUSEMOTION:
                for index, rect in enumerate(self.map_rects):
                    if rect.collidepoint(event.pos): self.map_index = index; break
            return 

        # 5. Xử lý Menu Chính
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN: self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_UP: self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE]: 
                self.play_click(); self.execute_option(game_object)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for index, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos): 
                    self.play_click(); self.selected_index = index; self.execute_option(game_object); break
        
        elif event.type == pygame.MOUSEMOTION:
            for index, rect in enumerate(self.option_rects):
                 if rect.collidepoint(event.pos): self.selected_index = index; break

    def execute_option(self, game_object):
        sel = self.options[self.selected_index]
        if sel == "CHƠI MỚI": 
            self.show_map_selection = True; self.map_index = 0
            
        elif sel == "CHƠI TIẾP":
            # Logic thông minh: Rắn dài > 3 thì ưu tiên chơi tiếp RAM, không thì load file
            if len(game_object.snake.body) > 3: 
                self.is_active = False
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

    def start_game_with_map(self, game_object):
        selected_map = self.map_names[self.map_index]
        game_object.load_map(selected_map)
        game_object.reset_game()
        self.show_map_selection = False
        self.is_active = False

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        hover_hand = False 

        if self.show_no_save_popup:
            self.renderer.draw_main_menu(self.selected_index, self.options, mouse_pos)
            self.renderer.draw_popup("KHÔNG CÓ DỮ LIỆU!", "Bạn chưa lưu game nào.")
            pygame.display.update(); return

        if self.show_high_score:
            self.back_button_rect = self.renderer.draw_high_score(self.high_score_data)
            if self.back_button_rect.collidepoint(mouse_pos): hover_hand = True
            
        elif self.show_settings:
            self.btn_vol_down, self.btn_vol_up, self.back_button_rect = self.renderer.draw_settings(self.volume, mouse_pos)
            if (self.back_button_rect.collidepoint(mouse_pos) or 
                self.btn_vol_down.collidepoint(mouse_pos) or 
                self.btn_vol_up.collidepoint(mouse_pos)):
                hover_hand = True
            
        elif self.show_tutorial:
            self.back_button_rect = self.renderer.draw_tutorial()
            if self.back_button_rect.collidepoint(mouse_pos): hover_hand = True
            
        # Vẽ màn hình Chọn Map (Đã xóa Chọn Mode cũ)
        elif self.show_map_selection:
            self.map_rects, self.back_button_rect = self.renderer.draw_map_selection(self.map_index, self.map_names, mouse_pos)
            if self.back_button_rect.collidepoint(mouse_pos): hover_hand = True
            for rect in self.map_rects:
                if rect.collidepoint(mouse_pos): hover_hand = True

        else:
            self.option_rects = self.renderer.draw_main_menu(self.selected_index, self.options, mouse_pos)
            for rect in self.option_rects:
                if rect.collidepoint(mouse_pos): hover_hand = True

        if hover_hand: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.update()