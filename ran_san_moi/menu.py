import pygame
import sys
import constants
from menu_renderer import MenuRenderer

class Menu:
    def __init__(self, high_score_data):
        self.renderer = MenuRenderer() 
        self.is_active = True
        self.high_score_data = high_score_data 
        
        self.options = ["CHƠI MỚI", "CHƠI TIẾP", "ĐIỂM CAO", "HƯỚNG DẪN", "CÀI ĐẶT", "THOÁT"]
        self.selected_index = 0
        self.option_rects = [] 
        self.skin_button_rect = None # Nút đổi màu ở góc trái
        
        # Màn hình phụ
        self.show_high_score = False 
        self.show_settings = False
        self.show_tutorial = False
        self.show_no_save_popup = False 
        self.show_skin_shop = False # Cờ bật shop
        self.skin_rects = [] # Danh sách nút trong shop
        
        # Màn hình chọn Map
        self.map_names = ["Kinh điển", "Hộp", "Đường hầm", "Cối xay", "Đường ray", "Chung cư"]
        self.map_index = 0
        self.show_map_selection = False 
        self.map_rects = []

        self.back_button_rect = None
        self.btn_vol_down = None
        self.btn_vol_up = None
        
        self.volume = 1.0
        self.update_volume()

    def play_click(self):
        if constants.click_sound: constants.click_sound.play()

    def update_volume(self):
        # 1. Nhạc nền
        try: pygame.mixer.music.set_volume(self.volume)
        except: pass
        
        # 2. Âm thanh thường (Ăn mồi, Click): Theo 100% volume tổng
        if constants.eat_sound: 
            constants.eat_sound.set_volume(self.volume)
        if constants.click_sound: 
            constants.click_sound.set_volume(self.volume)
            
        # 3. Mồi đặc biệt: Ưu tiên to nhất (100% volume tổng)
        if constants.eat_special_sound:
            constants.eat_special_sound.set_volume(self.volume)
            
        # 4. Đếm ngược: Luôn nhỏ bằng 30% volume tổng (Để không bị chói tai)
        if constants.countdown_sound:
            # Ví dụ: Nếu tổng là 1.0 -> countdown là 0.3
            # Nếu tổng là 0.5 -> countdown là 0.15
            constants.countdown_sound.set_volume(self.volume * 0.3)

    def handle_input(self, event, game_object):
        if self.show_no_save_popup:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.play_click(); self.show_no_save_popup = False 
            return

        # --- XỬ LÝ SKIN SHOP (MỚI) ---
        if self.show_skin_shop:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
                self.play_click(); self.show_skin_shop = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button_rect and self.back_button_rect.collidepoint(event.pos): 
                    self.play_click(); self.show_skin_shop = False
                else:
                    # Kiểm tra click vào skin nào
                    for i, rect in enumerate(self.skin_rects):
                        if rect.collidepoint(event.pos):
                            self.play_click()
                            # Cập nhật skin ngay cho rắn
                            game_object.snake.set_skin(i)
                            # Lưu game ngay để nhớ skin này
                            game_object.save_current_game()
            return

        if self.show_tutorial or self.show_high_score:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
                self.play_click(); self.show_tutorial = False; self.show_high_score = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button_rect and self.back_button_rect.collidepoint(event.pos): 
                    self.play_click(); self.show_tutorial = False; self.show_high_score = False
            return

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

        if self.show_map_selection:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: self.show_map_selection = False 
                elif event.key == pygame.K_RIGHT: self.map_index = min(self.map_index + 1, len(self.map_names) - 1)
                elif event.key == pygame.K_LEFT: self.map_index = max(self.map_index - 1, 0)
                elif event.key == pygame.K_DOWN: self.map_index = min(self.map_index + 2, len(self.map_names) - 1)
                elif event.key == pygame.K_UP: self.map_index = max(self.map_index - 2, 0)
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]: 
                    self.play_click(); self.start_game_with_map(game_object)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for index, rect in enumerate(self.map_rects):
                    if rect.collidepoint(event.pos): 
                        self.play_click(); self.map_index = index; self.start_game_with_map(game_object); break
                if self.back_button_rect and self.back_button_rect.collidepoint(event.pos): 
                    self.show_map_selection = False
            elif event.type == pygame.MOUSEMOTION:
                for index, rect in enumerate(self.map_rects):
                    if rect.collidepoint(event.pos): self.map_index = index; break
            return 

        # Xử lý Menu Chính
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN: self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_UP: self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE]: 
                self.play_click(); self.execute_option(game_object)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for index, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos): 
                    self.play_click(); self.selected_index = index; self.execute_option(game_object); break
            
            # Kiểm tra click vào nút SKIN
            if self.skin_button_rect and self.skin_button_rect.collidepoint(event.pos):
                self.play_click()
                self.show_skin_shop = True

        elif event.type == pygame.MOUSEMOTION:
            for index, rect in enumerate(self.option_rects):
                 if rect.collidepoint(event.pos): self.selected_index = index; break

    def execute_option(self, game_object):
        sel = self.options[self.selected_index]
        if sel == "CHƠI MỚI": 
            self.show_map_selection = True; self.map_index = 0
        elif sel == "CHƠI TIẾP":
            if len(game_object.snake.body) > 3: self.is_active = False
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
        self.show_map_selection = False; self.is_active = False

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        hover_hand = False 

        if self.show_no_save_popup:
            self.renderer.draw_main_menu(self.selected_index, self.options, mouse_pos)
            self.renderer.draw_popup("KHÔNG CÓ DỮ LIỆU!", "Bạn chưa lưu game nào."); pygame.display.update(); return

        if self.show_skin_shop:
            pass

        if self.show_high_score:
            self.back_button_rect = self.renderer.draw_high_score(self.high_score_data)
            if self.back_button_rect.collidepoint(mouse_pos): hover_hand = True
        elif self.show_settings:
            self.btn_vol_down, self.btn_vol_up, self.back_button_rect = self.renderer.draw_settings(self.volume, mouse_pos)
            if (self.back_button_rect.collidepoint(mouse_pos) or self.btn_vol_down.collidepoint(mouse_pos) or self.btn_vol_up.collidepoint(mouse_pos)): hover_hand = True
        elif self.show_tutorial:
            self.back_button_rect = self.renderer.draw_tutorial()
            if self.back_button_rect.collidepoint(mouse_pos): hover_hand = True
        elif self.show_map_selection:
            self.map_rects, self.back_button_rect = self.renderer.draw_map_selection(self.map_index, self.map_names, mouse_pos)
            if self.back_button_rect.collidepoint(mouse_pos): hover_hand = True
            for rect in self.map_rects:
                if rect.collidepoint(mouse_pos): hover_hand = True
        elif self.show_skin_shop:
             # Cần lấy ID từ game. Nhưng menu không giữ biến game. 
             # Mẹo: Import SKINS từ constants và dùng biến tạm. 
             # Để chính xác, ta cần truyền current_skin_id vào draw. 
             # Sửa: Trong hàm draw của Menu, ta thêm tham số optional hoặc lấy từ biến global.
             # Cách tốt nhất: Sửa main.py truyền game.snake.skin_id vào menu.draw()
             pass 
        else:
            self.option_rects, self.skin_button_rect = self.renderer.draw_main_menu(self.selected_index, self.options, mouse_pos)
            for rect in self.option_rects:
                if rect.collidepoint(mouse_pos): hover_hand = True
            if self.skin_button_rect.collidepoint(mouse_pos): hover_hand = True

        if hover_hand: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.display.update()
    
    # Sửa lại hàm draw để nhận thêm tham số skin_id từ bên ngoài (Main)
    def draw_with_game_data(self, current_skin_id):
        # 1. Lấy vị trí chuột
        mouse_pos = pygame.mouse.get_pos()
        hover_hand = False 

        # 2. Vẽ Popup
        if self.show_no_save_popup:
            self.renderer.draw_main_menu(self.selected_index, self.options, mouse_pos)
            self.renderer.draw_popup("KHÔNG CÓ DỮ LIỆU!", "Bạn chưa lưu game nào.")
            pygame.display.update()
            return

        # 3. Vẽ Shop Skin
        if self.show_skin_shop:
            self.skin_rects, self.back_button_rect = self.renderer.draw_skin_shop(current_skin_id, mouse_pos)
            if self.back_button_rect.collidepoint(mouse_pos): hover_hand = True
            for rect in self.skin_rects:
                if rect.collidepoint(mouse_pos): hover_hand = True
            
        # 4. Vẽ Điểm cao (Đã sửa: Truyền mouse_pos)
        elif self.show_high_score:
            self.back_button_rect = self.renderer.draw_high_score(self.high_score_data, mouse_pos)
            if self.back_button_rect.collidepoint(mouse_pos): hover_hand = True
            
        # 5. Vẽ Cài đặt
        elif self.show_settings:
            self.btn_vol_down, self.btn_vol_up, self.back_button_rect = self.renderer.draw_settings(self.volume, mouse_pos)
            if (self.back_button_rect.collidepoint(mouse_pos) or 
                self.btn_vol_down.collidepoint(mouse_pos) or 
                self.btn_vol_up.collidepoint(mouse_pos)):
                hover_hand = True
            
        # 6. Vẽ Hướng dẫn (Đã sửa: Truyền mouse_pos)
        elif self.show_tutorial:
            self.back_button_rect = self.renderer.draw_tutorial(mouse_pos)
            if self.back_button_rect.collidepoint(mouse_pos): hover_hand = True
            
        # 7. Vẽ Chọn Map
        elif self.show_map_selection:
            self.map_rects, self.back_button_rect = self.renderer.draw_map_selection(self.map_index, self.map_names, mouse_pos)
            if self.back_button_rect.collidepoint(mouse_pos): hover_hand = True
            for rect in self.map_rects:
                if rect.collidepoint(mouse_pos): hover_hand = True

        # 8. Vẽ Menu Chính
        else:
            self.option_rects, self.skin_button_rect = self.renderer.draw_main_menu(self.selected_index, self.options, mouse_pos)
            for rect in self.option_rects:
                if rect.collidepoint(mouse_pos): hover_hand = True
            if self.skin_button_rect and self.skin_button_rect.collidepoint(mouse_pos): 
                hover_hand = True

        if hover_hand: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.update()