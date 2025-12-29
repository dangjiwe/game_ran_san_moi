# constants.py - Import tất cả từ các file con
from settings import *
from display import *
from assets import *
# --- HỆ THỐNG SKIN (MÀU RẮN) ---
# Cấu trúc: "Tên": (Màu viền, Màu tâm)
SKINS = [
    {"name": "Xanh Biển", "outer": (0, 100, 200), "inner": (100, 200, 255)}, # Mặc định
    {"name": "Lục Bảo",   "outer": (0, 180, 0),   "inner": (100, 255, 100)},
    {"name": "Dung Nham", "outer": (200, 50, 0),  "inner": (255, 150, 50)},
    {"name": "Tím Mộng",  "outer": (120, 0, 200), "inner": (200, 100, 255)},
    {"name": "Vàng Kim",  "outer": (200, 160, 0), "inner": (255, 220, 50)},
    {"name": "Hắc Ám",    "outer": (40, 40, 40),  "inner": (120, 120, 120)},
    {"name": "Hồng Phấn", "outer": (200, 0, 100), "inner": (255, 150, 200)},
    {"name": "Băng Giá",  "outer": (0, 150, 150), "inner": (150, 255, 255)},
]