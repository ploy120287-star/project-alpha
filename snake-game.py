import random
import tkinter as tk


CELL_SIZE = 24
GRID_WIDTH = 25
GRID_HEIGHT = 18
CANVAS_WIDTH = CELL_SIZE * GRID_WIDTH
CANVAS_HEIGHT = CELL_SIZE * GRID_HEIGHT
MOVE_DELAY = 120


def main() -> None:
    root = tk.Tk()
    root.title("Snake Game")
    root.resizable(False, False)

    score = 0
    snake: list[tuple[int, int]] = []
    direction = (1, 0)
    next_direction = (1, 0)
    food = (0, 0)
    game_over = False
    after_id: str | None = None

    score_label = tk.Label(root, text="คะแนน: 0", font=("Segoe UI", 14))
    score_label.pack(pady=(10, 4))

    canvas = tk.Canvas(
        root,
        width=CANVAS_WIDTH,
        height=CANVAS_HEIGHT,
        bg="#111827",
        highlightthickness=0,
    )
    canvas.pack(padx=10)

    status_label = tk.Label(
        root,
        text="ใช้ปุ่มลูกศรเพื่อควบคุมงู",
        font=("Segoe UI", 11),
        pady=6,
    )
    status_label.pack()

    def place_food() -> tuple[int, int]:
        empty_cells = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in snake
        ]
        return random.choice(empty_cells) if empty_cells else (-1, -1)

    def draw() -> None:
        canvas.delete("all")
        food_x, food_y = food
        if food_x >= 0:
            padding = 4
            canvas.create_oval(
                food_x * CELL_SIZE + padding,
                food_y * CELL_SIZE + padding,
                (food_x + 1) * CELL_SIZE - padding,
                (food_y + 1) * CELL_SIZE - padding,
                fill="#ef4444",
                outline="",
            )

        for index, (x, y) in enumerate(snake):
            padding = 2
            color = "#22c55e" if index == 0 else "#16a34a"
            canvas.create_rectangle(
                x * CELL_SIZE + padding,
                y * CELL_SIZE + padding,
                (x + 1) * CELL_SIZE - padding,
                (y + 1) * CELL_SIZE - padding,
                fill=color,
                outline="",
            )

    def end_game(message: str) -> None:
        nonlocal game_over
        game_over = True
        status_label.config(text=message)
        canvas.create_text(
            CANVAS_WIDTH // 2,
            CANVAS_HEIGHT // 2,
            text=message,
            fill="white",
            font=("Segoe UI", 22, "bold"),
        )

    def game_loop() -> None:
        nonlocal direction, next_direction, food, score, after_id
        after_id = None
        if game_over:
            return

        direction = next_direction
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])
        eating = new_head == food
        body_to_check = snake if eating else snake[:-1]

        if (
            not 0 <= new_head[0] < GRID_WIDTH
            or not 0 <= new_head[1] < GRID_HEIGHT
            or new_head in body_to_check
        ):
            end_game("จบเกม! กดเริ่มใหม่เพื่อเล่นอีกครั้ง")
            return

        snake.insert(0, new_head)
        if eating:
            score += 1
            score_label.config(text=f"คะแนน: {score}")
            food = place_food()
            if food == (-1, -1):
                draw()
                end_game("ชนะแล้ว! คุณเก็บอาหารครบทุกช่อง")
                return
        else:
            snake.pop()

        draw()
        after_id = root.after(MOVE_DELAY, game_loop)

    def change_direction(event: tk.Event) -> None:
        nonlocal next_direction
        directions = {
            "Up": (0, -1),
            "Down": (0, 1),
            "Left": (-1, 0),
            "Right": (1, 0),
        }
        requested = directions.get(event.keysym)
        if requested and requested != (-direction[0], -direction[1]):
            next_direction = requested

    def restart_game() -> None:
        nonlocal score, snake, direction, next_direction, food, game_over, after_id
        if after_id is not None:
            root.after_cancel(after_id)
            after_id = None

        score = 0
        snake = [
            (GRID_WIDTH // 2, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2),
        ]
        direction = (1, 0)
        next_direction = (1, 0)
        food = place_food()
        game_over = False
        score_label.config(text="คะแนน: 0")
        status_label.config(text="ใช้ปุ่มลูกศรเพื่อควบคุมงู")
        draw()
        after_id = root.after(MOVE_DELAY, game_loop)

    root.bind_all("<KeyPress>", change_direction)
    tk.Button(
        root,
        text="เริ่มเกมใหม่",
        font=("Segoe UI", 11),
        command=restart_game,
    ).pack(pady=(0, 10))

    restart_game()
    root.mainloop()


if __name__ == "__main__":
    main()
