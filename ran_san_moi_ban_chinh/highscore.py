# files/highscore.py

import json
import os
from constants import PROJECT_ROOT

class HighScoreManager:
    def __init__(self):
        # Lấy đường dẫn của thư mục chứa file code này (thư mục hiện tại)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Đặt file high_score.json nằm ngay cùng thư mục đó
        self.file_path = os.path.join(base_dir, "high_score.json")
        
        # Nếu bạn vẫn muốn gom vào thư mục 'save' cho gọn (tùy chọn), 
        # hãy bỏ comment 3 dòng dưới, còn không thì cứ để file nằm ngoài:
        
        # self.save_dir = os.path.join(base_dir, "save")
        # if not os.path.exists(self.save_dir):
        #     os.makedirs(self.save_dir)
        # self.file_path = os.path.join(self.save_dir, "high_score.json")
        # Định nghĩa đường dẫn file save
        #self.save_dir = os.path.join(PROJECT_ROOT, "save")
        #self.file_path = os.path.join(self.save_dir, "high_score.json")
        
        # Đảm bảo thư mục 'save' luôn tồn tại
        #if not os.path.exists(self.save_dir):
        #    os.makedirs(self.save_dir)

    def load(self):
        """Đọc điểm từ file. Trả về 0 nếu file lỗi hoặc chưa có."""
        if not os.path.exists(self.file_path):
            return 0
        
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            return data.get('high_score', 0)
        except (json.JSONDecodeError, KeyError):
            return 0

    def save(self, score):
        """Lưu điểm số xuống file."""
        data = {'high_score': score}
        try:
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Lỗi khi lưu điểm: {e}")