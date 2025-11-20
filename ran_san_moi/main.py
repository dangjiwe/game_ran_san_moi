# main.py

import pygame
import sys
from game import Game
# Tệp constants.py đã thực hiện pygame.init(), thiết lập màn hình và tải ảnh.

# Khởi tạo đối tượng Game
game = Game()

while True:
    # Xử lý input từ người dùng
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Vẽ tất cả các thành phần trò chơi
    game.draw_elements()
    
    # Cập nhật màn hình
    pygame.display.update()