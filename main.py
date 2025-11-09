import tkinter as tk
import random

# ====== Cấu hình cơ bản ======
WIDTH = 400
HEIGHT = 400
SPEED = 150  # tốc độ di chuyển (ms)
CELL_SIZE = 20

# ====== Cửa sổ chính ======
window = tk.Tk()
window.title("Rắn săn mồi")
window.resizable(False, False)

# ====== Canvas để vẽ game ======
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# ====== Biến toàn cục ======
snake = [(100, 100), (80, 100), (60, 100)]
snake_dir = "Right"
food = None
running = False

# ====== Tạo nút Bắt đầu ======
def start_game():
    global running, snake, snake_dir, food
    if not running:
        running = True
        snake = [(100, 100), (80, 100), (60, 100)]
        snake_dir = "Right"
        canvas.delete("all")
        create_food()
        move_snake()

btn_start = tk.Button(window, text="Bắt đầu", font=("Arial", 12), command=start_game)
btn_start.pack(pady=5)

# ====== Hàm tạo thức ăn ======
def create_food():
    global food
    x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    food = (x, y)
    canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill="red", tags="food")

# ====== Hàm di chuyển rắn ======
def move_snake():
    global snake, food, running

    if not running:
        return

    head_x, head_y = snake[0]
    if snake_dir == "Up":
        head_y -= CELL_SIZE
    elif snake_dir == "Down":
        head_y += CELL_SIZE
    elif snake_dir == "Left":
        head_x -= CELL_SIZE
    elif snake_dir == "Right":
        head_x += CELL_SIZE

    new_head = (head_x, head_y)

    # Kiểm tra va chạm tường hoặc thân
    if (
        head_x < 0 or head_y < 0 or
        head_x >= WIDTH or head_y >= HEIGHT or
        new_head in snake
    ):
        game_over()
        return

    snake.insert(0, new_head)

    # Ăn thức ăn
    if new_head == food:
        canvas.delete("food")
        create_food()
    else:
        snake.pop()

    # Vẽ lại rắn
    canvas.delete("snake")
    for (x, y) in snake:
        canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill="lime", tags="snake")

    window.after(SPEED, move_snake)

# ====== Xử lý phím di chuyển ======
def change_dir(event):
    global snake_dir
    key = event.keysym
    opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
    if key in ["Up", "Down", "Left", "Right"] and opposites[key] != snake_dir:
        snake_dir = key

window.bind("<KeyPress>", change_dir)

# ====== Game Over ======
def game_over():
    global running
    running = False
    canvas.create_text(WIDTH/2, HEIGHT/2, text="GAME OVER", fill="white", font=("Arial", 24, "bold"))

window.mainloop()
