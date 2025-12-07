import os
import sys
import time
import subprocess

# --- PHẦN TỰ ĐỘNG DÒ TÌM ĐƯỜNG DẪN ---
# 1. Lấy đường dẫn của chính file auto_run.py này
thu_muc_chua_file = os.path.dirname(os.path.abspath(__file__))

# 2. Tên file bạn muốn chạy
ten_file = "main.py"

# 3. Nối lại thành đường dẫn đầy đủ (Ví dụ: C:\Users\...\Hoc_lam_giao_dien.py)
duong_dan_day_du = os.path.join(thu_muc_chua_file, ten_file)
# -------------------------------------

print(f"--- Dang tim file tai: {duong_dan_day_du} ---")

# Kiểm tra xem file có tồn tại thật không
if not os.path.exists(duong_dan_day_du):
    print("LOI: Van khong tim thay file!")
    print(f"Ban hay chac chan file '{ten_file}' nam CUNG THU MUC voi file nay.")
    input("Bam Enter de thoat...")
    sys.exit()

print("Tim thay file! Bat dau chay...")
print("Luu y: Ban cu sua code roi Luu (Ctrl+S), giao dien se tu reload.")

# Khởi động lần đầu
process = subprocess.Popen([sys.executable, duong_dan_day_du])
last_mtime = os.stat(duong_dan_day_du).st_mtime

try:
    while True:
        time.sleep(1) 
        try:
            # Kiểm tra thay đổi dựa trên đường dẫn đầy đủ
            current_mtime = os.stat(duong_dan_day_du).st_mtime
            if current_mtime != last_mtime:
                print("\n[Thay doi] -> Khoi dong lai...")
                process.terminate()
                
                try:
                     process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                     process.kill() 

                process = subprocess.Popen([sys.executable, duong_dan_day_du])
                last_mtime = current_mtime
        except FileNotFoundError:
            pass
except KeyboardInterrupt:
    process.terminate()
    print("\nDa dung chuong trinh.")