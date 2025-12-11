# files/Resources/highscore.py
import json
import os
from constants import PROJECT_ROOT

class HighScoreManager:
    def __init__(self):
        self.save_dir = os.path.join(PROJECT_ROOT, "save")
        self.hs_file = os.path.join(self.save_dir, "high_score.json")
        self.save_game_file = os.path.join(self.save_dir, "saved_game.json")
        
        if not os.path.exists(self.save_dir):
            try: os.makedirs(self.save_dir)
            except: pass

    def load(self):
        if not os.path.exists(self.hs_file): return 0
        try:
            with open(self.hs_file, 'r', encoding='utf-8') as f:
                return json.load(f).get('high_score', 0)
        except: return 0

    def save(self, score):
        try:
            with open(self.hs_file, 'w', encoding='utf-8') as f:
                json.dump({'high_score': score}, f, indent=4)
        except: pass

    def save_game_state(self, game_data):
        try:
            with open(self.save_game_file, 'w', encoding='utf-8') as f:
                json.dump(game_data, f, indent=4)
            print("----> Da luu game!")
        except Exception as e:
            print(f"Loi luu: {e}")

    def load_game_state(self):
        if not os.path.exists(self.save_game_file):
            return None 
        try:
            with open(self.save_game_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return None

    # --- HÀM XÓA DỮ LIỆU ---
    def clear_saved_game(self):
        """Làm sạch nội dung file saved_game.json"""
        try:
            with open(self.save_game_file, 'w', encoding='utf-8') as f:
                json.dump({}, f) # Ghi đè bằng dấu {}
            print("----> Da xoa sach du lieu save!")
        except: pass