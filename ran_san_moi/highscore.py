import json
import os

class HighScoreManager:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(base_dir, "high_score.json")

    def load(self):
        """
        Trả về Dictionary: {'Kinh điển': 10, 'Hộp': 5, ...}
        """
        if not os.path.exists(self.file_path):
            return {}
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if 'high_score' in data and isinstance(data['high_score'], int):
                return {"Kinh điển": data['high_score']}
                
            return data
        except:
            return {}

    def save(self, scores_dict):
        """Lưu toàn bộ dictionary điểm xuống file"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(scores_dict, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Lỗi lưu điểm: {e}")