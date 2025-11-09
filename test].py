import pygame

# 1. Khởi tạo Pygame
pygame.init()

# 2. Định nghĩa các hằng số (Kích thước, Màu sắc)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 3. Tạo cửa sổ game
# Chúng ta tạo một cửa sổ 600x600 pixels
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Rắn Săn Mồi - Nhóm [Tên Nhóm]")

# 4. Vòng lặp chính của game (Game Loop)
# Đây là nơi mọi thứ diễn ra. Game sẽ chạy liên tục cho đến khi người dùng tắt nó.
running = True
while running:
    
    # === XỬ LÝ SỰ KIỆN (INPUT) ===
    # Kiểm tra xem người dùng có làm gì không (nhấn phím, click chuột...)
    for event in pygame.event.get():
        # Nếu người dùng nhấn nút 'X' (Thoát)
        if event.type == pygame.QUIT:
            running = False

    # === CẬP NHẬT LOGIC GAME (UPDATE) ===
    # (Tuần 2, 3, 4 sẽ code ở đây)
    # Ví dụ: Di chuyển rắn, kiểm tra ăn mồi, kiểm tra thua...
    
    # === VẼ LẠI MÀN HÌNH (RENDER) ===
    # 1. Xóa màn hình cũ bằng cách tô màu đen
    screen.fill(BLACK)
    
    # 2. Vẽ các đối tượng mới
    # (Tuần 1-4 sẽ code ở đây)
    # Ví dụ: Vẽ rắn, vẽ mồi...
    
    # 3. Cập nhật màn hình để hiển thị những gì đã vẽ
    pygame.display.flip()

# 5. Thoát game
# Khi vòng lặp 'while running' kết thúc, chúng ta thoát pygame
pygame.quit()