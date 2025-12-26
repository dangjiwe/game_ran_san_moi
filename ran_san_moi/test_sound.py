import pygame
import os
import time

# Khởi tạo âm thanh
pygame.mixer.init()

print("--- BẮT ĐẦU TEST ÂM THANH ---")

# 1. LẤY ĐƯỜNG DẪN CHÍNH XÁC CỦA FILE NÀY
# Dòng này giúp tìm ra thư mục chứa file test_sound.py
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Thư mục chứa code: {current_dir}")

# 2. Tạo đường dẫn tới file click.mp3
# Nó sẽ nối thư mục trên với tên file
sound_path = os.path.join(current_dir, "click.mp3")
print(f"Đang tìm file tại: {sound_path}")

# 3. Kiểm tra và phát
if os.path.exists(sound_path):
    print("--> ĐÃ TÌM THẤY FILE! Đang thử phát...")
    try:
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(1.0)
        sound.play()
        
        # Chờ 2 giây để nghe
        time.sleep(2)
        print("--> Đã phát xong. Bạn có nghe thấy tiếng không?")
    except Exception as e:
        print(f"--> TÌM THẤY NHƯNG LỖI ĐỌC FILE: {e}")
        print("Gợi ý: File mp3 có thể bị lỗi codec, hãy thử đổi sang file .wav")
else:
    print("--> VẪN KHÔNG TÌM THẤY FILE.")
    print("Lý do: File click.mp3 không nằm cùng thư mục với file test_sound.py")

print("--- KẾT THÚC ---")