# 🐍 Rắn Săn Mồi

![Python](https://img.shields.io/badge/Language-Python_3-blue?style=flat-square&logo=python)
![Lib](https://img.shields.io/badge/Library-Pygame-green?style=flat-square&logo=pygame)
![Version](https://img.shields.io/badge/Version-1.0.0-orange?style=flat-square)

Một phiên bản hiện đại của trò chơi cổ điển, tập trung vào trải nghiệm mượt mà, đồ họa vẽ bằng thuật toán và hệ thống lưu trữ thông minh.

---

## ✨ Tính Năng Nổi Bật

* **Đồ họa Procedural:** Táo 3D và Rắn được vẽ trực tiếp bằng Code giúp hình ảnh sắc nét ở mọi độ phân giải.
* **Hệ thống Kỷ Lục:** Tự động lưu điểm cao và thông báo phá kỷ lục ngay lập tức trong màn chơi.
* **Mồi Đặc Biệt:** Xuất hiện ngẫu nhiên các viên Ruby lấp lánh mang lại điểm thưởng gấp 3 lần.
* **Cửa Hàng Skin:** Tùy biến màu sắc rắn với nhiều giao diện đẹp mắt như Vàng Kim, Băng Giá, Hắc Ám...
* **Bản Đồ Đa Dạng:** 6 màn chơi với địa hình khác nhau: Kinh điển, Hộp kín, Đường hầm, Cối xay, Đường ray và Chung cư.
* **Cơ Chế Thông Minh:** Tự động tăng tốc độ rắn theo điểm số và tự động lưu màn chơi khi thoát đột ngột.

---

## 🕹️ Điều Khiển

| Phím | Chức Năng |
| :--- | :--- |
| **W / A / S / D** | Di chuyển Rắn |
| **⬆️ ⬇️ ⬅️ ➡️** | Di chuyển Rắn (Cách 2) |
| **Space / Enter** | Chọn / Chơi lại |
| **ESC** |Quay lại|

---

## 📂 Cấu Trúc Dự Án

```text
GAME_RAN_SAN_MOI/
├── ran_san_moi/
│   ├── Resources/         # Tài nguyên Âm thanh, Hình ảnh, Font
│   ├── main.py            # Điểm khởi chạy game
│   ├── game.py            # Xử lý logic chính
│   ├── snake.py           # Class Rắn
│   ├── food.py            # Class Thức ăn
│   └── ...
└── README.md              # Tài liệu dự án
🚀 Cài Đặt & Chạy Game
Cài đặt thư viện:

pip install pygame

Chạy game:

cd ran_san_moi
python main.py

👨‍💻 Thông Tin
Nhóm: 5

Môn học: Lập trình Python và Úng dụng

Dự án mã nguồn mở phục vụ mục đích học tập.
