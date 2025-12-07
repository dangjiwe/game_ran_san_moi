#files/Resources/menu.py
import pygame
import sys
from constants import screen, screen_width, screen_height, font, DARK_GREEN, GRASS_LIGHT, BLACK, WHITE, menu_bg_surface

class Menu:
    def __init__(self, high_score_data):
        self.is_active = True
        self.selected_index = 0
        self.high_score_data = high_score_data 
        
        self.options = ["CHƠI MỚI", "CHƠI TIẾP", "ĐIỂM CAO", "HƯỚNG DẪN", "CÀI ĐẶT", "THOÁT"]
        self.option_rects = [] # Lưu vị trí các nút để check chuột
        
        # Biến cờ màn hình phụ
        self.show_high_score = False 
        self.show_settings = False
        self.show_tutorial = False
        self.show_mode_selection = False
        self.show_challenge_popup = False
        self.show_no_save_popup = False 
        
        self.mode_options = ["CƠ BẢN", "THỬ THÁCH"]
        self.mode_index = 0
        self.mode_rects = []
        
        self.back_button_rect = None
        
        # === [QUAN TRỌNG] BIẾN CỜ ĐỂ BÁO MAIN.PY BẮT ĐẦU GAME ===
        self.start_game_trigger = False 
        # ========================================================

    # --- HÀM VẼ NÚT (CHỈ VẼ, KHÔNG XỬ LÝ LOGIC) ---
    def draw_button(self, text, x, y, width=300, height=60, is_selected=False):
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (x, y)
        
        # Kiểm tra Hover để đổi màu (Chỉ đổi màu, không đổi con trỏ ở đây)
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse_pos)
        
        # Ưu tiên: Nếu được chọn bằng phím HOẶC chuột đang đè lên
        is_active = is_selected or is_hovered
        
        if is_active:
            bg_color = (200, 230, 100); text_color = BLACK
        else:
            bg_color = (60, 80, 40); text_color = WHITE
            
        # Vẽ bóng
        shadow_rect = rect.copy(); shadow_rect.x += 5; shadow_rect.y += 5
        pygame.draw.rect(screen, (30, 30, 30), shadow_rect, border_radius=15)
        # Vẽ nút
        pygame.draw.rect(screen, bg_color, rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, rect, 3, border_radius=15)
        
        # Vẽ tam giác nếu dùng phím
        if is_selected and not is_hovered:
             tri_points = [(rect.left-20, rect.centery-10), (rect.left-20, rect.centery+10), (rect.left-5, rect.centery)]
             pygame.draw.polygon(screen, BLACK, tri_points)
        
        text_surf = font.render(text, True, text_color)
        screen.blit(text_surf, text_surf.get_rect(center=rect.center))
        
        return rect # Trả về khung hình để dùng cho việc khác

    # --- HÀM CẬP NHẬT CON TRỎ CHUỘT (GỌI 1 LẦN CUỐI CÙNG) ---
    def update_cursor(self):
        mouse_pos = pygame.mouse.get_pos()
        should_hand = False
        
        # Gom tất cả các nút hiện có trên màn hình vào 1 danh sách để kiểm tra
        active_rects = []
        
        if self.show_mode_selection:
            active_rects = self.mode_rects + ([self.back_button_rect] if self.back_button_rect else [])
        elif self.show_tutorial:
            if self.back_button_rect: active_rects = [self.back_button_rect]
        elif not (self.show_high_score or self.show_settings or self.show_challenge_popup or self.show_no_save_popup):
            active_rects = self.option_rects

        # Kiểm tra xem chuột có chạm vào nút nào không
        for rect in active_rects:
            if rect and rect.collidepoint(mouse_pos):
                should_hand = True
                break
        
        if should_hand: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw(self):
        if menu_bg_surface: screen.blit(menu_bg_surface, (0, 0))
        else: screen.fill(GRASS_LIGHT)

        # Vẽ các màn hình phụ
        if self.show_high_score: 
            self.draw_sub_screen("ĐIỂM CAO", str(self.high_score_data))
            # (Không cần update cursor ở đây vì màn hình này không có nút bấm)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            pygame.display.update(); return

        if self.show_settings: 
            self.draw_sub_screen("CÀI ĐẶT", "Tính năng đang phát triển")
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            pygame.display.update(); return

        if self.show_tutorial: 
            self.draw_tutorial_screen()
            self.update_cursor() # Cập nhật chuột
            pygame.display.update(); return
        
        if self.show_mode_selection: 
            self.draw_mode_selection_screen()
            if self.show_challenge_popup: self.draw_challenge_msg()
            self.update_cursor() # Cập nhật chuột
            pygame.display.update(); return

        # Vẽ Menu Chính
        title = font.render("RẮN SĂN MỒI", True, BLACK)
        t_shadow = font.render("RẮN SĂN MỒI", True, (200, 200, 200))
        t_rect = title.get_rect(center=(screen_width//2, screen_height//8))
        screen.blit(t_shadow, (t_rect.x+3, t_rect.y+3))
        screen.blit(title, t_rect)

        self.option_rects = []
        start_y = screen_height // 4 + 20
        for i, opt in enumerate(self.options):
            is_selected = (i == self.selected_index)
            # Gọi hàm vẽ đơn giản
            rect = self.draw_button(opt, screen_width//2, start_y + i * 70, is_selected=is_selected)
            self.option_rects.append(rect)
        
        if self.show_no_save_popup: self.draw_no_save_msg()
        
        self.update_cursor() # Cập nhật chuột lần cuối
        pygame.display.update()

    def handle_input(self, event, game_object):
        # ... (Phần logic popup giữ nguyên) ...
        if self.show_challenge_popup or self.show_no_save_popup:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.show_challenge_popup = False; self.show_no_save_popup = False 
            return

        # ... (Phần logic tutorial/settings giữ nguyên) ...
        if self.show_tutorial:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: self.show_tutorial = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button_rect and self.back_button_rect.collidepoint(event.pos): self.show_tutorial = False
            return
        if self.show_high_score or self.show_settings:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: self.show_high_score = False; self.show_settings = False
            return

        # Xử lý Chọn Chế Độ
        if self.show_mode_selection:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: self.show_mode_selection = False 
                elif event.key == pygame.K_DOWN: self.mode_index = (self.mode_index + 1) % len(self.mode_options)
                elif event.key == pygame.K_UP: self.mode_index = (self.mode_index - 1) % len(self.mode_options)
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]: self.execute_mode_choice(game_object)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for index, rect in enumerate(self.mode_rects):
                    if rect.collidepoint(event.pos): self.mode_index = index; self.execute_mode_choice(game_object); break
                if self.back_button_rect and self.back_button_rect.collidepoint(event.pos): self.show_mode_selection = False
            elif event.type == pygame.MOUSEMOTION:
                for index, rect in enumerate(self.mode_rects):
                    if rect.collidepoint(event.pos): self.mode_index = index; break
            return 

        # Xử lý Menu Chính
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN: self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_UP: self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE]: self.execute_option(game_object)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for index, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos): self.selected_index = index; self.execute_option(game_object); break
        elif event.type == pygame.MOUSEMOTION:
            for index, rect in enumerate(self.option_rects):
                 if rect.collidepoint(event.pos): self.selected_index = index; break

    def execute_option(self, game_object):
        sel = self.options[self.selected_index]
        if sel == "CHƠI MỚI": 
            self.show_mode_selection = True; self.mode_index = 0
        elif sel == "CHƠI TIẾP":
            if len(game_object.snake.body) > 3 or game_object.snake.body[0].x != 6: 
                self.is_active = False # -> Vào game luôn (Pause)
            else:
                success = game_object.load_saved_game()
                if success: 
                    self.is_active = False # -> Vào game (Load file)
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
            self.is_active = False
            self.show_mode_selection = False
            # === [QUAN TRỌNG] BẬT CỜ ĐỂ MAIN.PY BIẾT ===
            self.start_game_trigger = True 
            # ============================================
        elif choice == "THỬ THÁCH": self.show_challenge_popup = True

    # ... (Các hàm draw_no_save, draw_sub_screen, draw_challenge giữ nguyên nhưng nhớ dùng draw_button trong draw_mode_selection) ...
    def draw_no_save_msg(self):
        overlay = pygame.Surface((screen_width, screen_height)); overlay.set_alpha(150); overlay.fill(BLACK)
        screen.blit(overlay, (0,0))
        box = pygame.Rect(0, 0, 500, 250); box.center = (screen_width//2, screen_height//2)
        pygame.draw.rect(screen, WHITE, box, border_radius=20); pygame.draw.rect(screen, BLACK, box, 5, border_radius=20)
        msg1 = font.render("KHÔNG CÓ DỮ LIỆU!", True, (255, 0, 0)); msg2 = font.render("Bạn chưa lưu game nào.", True, BLACK)
        msg3 = font.render("Nhấn phím bất kỳ để đóng", True, (100, 100, 100)); msg3 = pygame.transform.scale(msg3, (int(msg3.get_width()*0.7), int(msg3.get_height()*0.7)))
        screen.blit(msg1, msg1.get_rect(center=(screen_width//2, screen_height//2 - 40)))
        screen.blit(msg2, msg2.get_rect(center=(screen_width//2, screen_height//2 + 20)))
        screen.blit(msg3, msg3.get_rect(center=(screen_width//2, screen_height//2 + 80)))

    def draw_challenge_msg(self):
        overlay = pygame.Surface((screen_width, screen_height)); overlay.set_alpha(150); overlay.fill(BLACK)
        screen.blit(overlay, (0,0))
        box = pygame.Rect(0, 0, 500, 300); box.center = (screen_width//2, screen_height//2)
        pygame.draw.rect(screen, WHITE, box, border_radius=20); pygame.draw.rect(screen, BLACK, box, 5, border_radius=20)
        msg1 = font.render("CHẾ ĐỘ THỬ THÁCH", True, (255, 0, 0)); msg2 = font.render("ĐANG PHÁT TRIỂN...", True, BLACK)
        msg3 = font.render("(Sẽ sớm ra mắt)", True, DARK_GREEN); msg4 = font.render("Nhấn phím bất kỳ để đóng", True, (100, 100, 100)); msg4 = pygame.transform.scale(msg4, (int(msg4.get_width()*0.7), int(msg4.get_height()*0.7)))
        screen.blit(msg1, msg1.get_rect(center=(screen_width//2, screen_height//2 - 60))); screen.blit(msg2, msg2.get_rect(center=(screen_width//2, screen_height//2)))
        screen.blit(msg3, msg3.get_rect(center=(screen_width//2, screen_height//2 + 50))); screen.blit(msg4, msg4.get_rect(center=(screen_width//2, screen_height//2 + 120)))

    def draw_sub_screen(self, title, msg):
        if menu_bg_surface: screen.blit(menu_bg_surface, (0,0))
        else: screen.fill(GRASS_LIGHT)
        s = pygame.Surface((screen_width - 80, screen_height - 80)); s.set_alpha(220); s.fill(WHITE)
        screen.blit(s, (40, 40)); pygame.draw.rect(screen, BLACK, (40, 40, screen_width-80, screen_height-80), 4)
        t_surf = font.render(title, True, BLACK); m_surf = font.render(msg, True, (255, 0, 0)); es = font.render("Nhấn ESC để quay lại", True, DARK_GREEN)
        screen.blit(t_surf, t_surf.get_rect(center=(screen_width//2, screen_height//4))); screen.blit(m_surf, m_surf.get_rect(center=(screen_width//2, screen_height//2))); screen.blit(es, es.get_rect(center=(screen_width//2, screen_height*3/4)))

    def draw_mode_selection_screen(self):
        title = font.render("CHỌN CHẾ ĐỘ", True, BLACK); screen.blit(title, title.get_rect(center=(screen_width//2, screen_height//4)))
        self.mode_rects = []
        start_y = screen_height // 2
        for i, opt in enumerate(self.mode_options):
            is_selected = (i == self.mode_index)
            # Dùng hàm draw_button
            rect = self.draw_button(opt, screen_width//2, start_y + i * 100, width=300, height=60, is_selected=is_selected)
            self.mode_rects.append(rect)
        # Dùng hàm draw_button cho nút quay lại luôn
        self.back_button_rect = self.draw_button("QUAY LẠI", screen_width//2, screen_height - 60, width=200, height=50)
        pygame.display.update()

    def draw_tutorial_screen(self):
        if menu_bg_surface: screen.blit(menu_bg_surface, (0,0))
        else: screen.fill(GRASS_LIGHT)
        overlay = pygame.Surface((screen_width - 40, screen_height - 40)); overlay.set_alpha(230); overlay.fill((255, 255, 255))
        screen.blit(overlay, (20, 20)); pygame.draw.rect(screen, BLACK, (20, 20, screen_width-40, screen_height-40), 4)
        title = font.render("HƯỚNG DẪN CHƠI", True, (255, 0, 0)); screen.blit(title, title.get_rect(center=(screen_width//2, 70)))
        lines = ["1. Dùng 4 phím MŨI TÊN để di chuyển.", "2. Ăn mồi để ghi điểm và lớn lên.", "3. Không được đâm vào tường.", "4. Không được đâm vào thân mình.", "5. Nhấn SPACE để chơi lại khi thua.", "6. Nhấn ESC để Tạm dừng / Quay lại."]
        start_y = 130
        for line in lines:
            line_surf = font.render(line, True, BLACK)
            if line_surf.get_width() > screen_width - 60:
                scaled_w = screen_width - 60; scaled_h = int(line_surf.get_height() * (scaled_w / line_surf.get_width())); line_surf = pygame.transform.scale(line_surf, (scaled_w, scaled_h))
            screen.blit(line_surf, (40, start_y)); start_y += 50 
        self.back_button_rect = self.draw_button("QUAY LẠI", screen_width//2, screen_height - 60, width=200, height=50)
        pygame.display.update()