#test tạo nút
import tkinter as tk

# Tạo cửa sổ chính
window = tk.Tk()
window.title("Cửa sổ Bắt đầu")
window.geometry("300x200")  # Kích thước cửa sổ

# Hàm xử lý khi bấm nút
def bat_dau():
    print("Chương trình đã bắt đầu!")

# Tạo nút Bắt đầu
nut_bat_dau = tk.Button(window, text="Bắt đầu", command=bat_dau, font=("Arial", 14))
nut_bat_dau.pack(pady=50)

# Chạy vòng lặp giao diện
window.mainloop()
