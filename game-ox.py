import tkinter as tk


def has_won(board: list[str], mark: str) -> bool:
    winning_lines = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    )
    return any(all(board[cell] == mark for cell in line) for line in winning_lines)


def main() -> None:
    root = tk.Tk()
    root.title("เกม OX")
    root.resizable(False, False)

    board = [""] * 9
    current_player = "X"
    game_over = False
    status = tk.StringVar(value="ตาของผู้เล่น X")
    buttons: list[tk.Button] = []

    def reset_game() -> None:
        nonlocal current_player, game_over
        current_player = "X"
        game_over = False
        status.set("ตาของผู้เล่น X")
        for button in buttons:
            button.config(text="", state=tk.NORMAL, disabledforeground="black")
        for index in range(9):
            board[index] = ""

    def make_move(index: int) -> None:
        nonlocal current_player, game_over
        if game_over or board[index]:
            return

        board[index] = current_player
        buttons[index].config(
            text=current_player,
            state=tk.DISABLED,
            disabledforeground="#2563eb" if current_player == "X" else "#dc2626",
        )

        if has_won(board, current_player):
            status.set(f"ผู้เล่น {current_player} ชนะแล้ว!")
            game_over = True
            for button in buttons:
                button.config(state=tk.DISABLED)
            return

        if all(board):
            status.set("เสมอกัน!")
            game_over = True
            for button in buttons:
                button.config(state=tk.DISABLED)
            return

        current_player = "O" if current_player == "X" else "X"
        status.set(f"ตาของผู้เล่น {current_player}")

    tk.Label(root, textvariable=status, font=("Segoe UI", 16), pady=12).grid(
        row=0, column=0, columnspan=3
    )

    for index in range(9):
        button = tk.Button(
            root,
            text="",
            font=("Segoe UI", 28, "bold"),
            width=4,
            height=2,
            command=lambda cell=index: make_move(cell),
        )
        button.grid(row=index // 3 + 1, column=index % 3, padx=4, pady=4)
        buttons.append(button)

    tk.Button(root, text="เริ่มเกมใหม่", font=("Segoe UI", 12), command=reset_game).grid(
        row=4, column=0, columnspan=3, pady=(8, 12)
    )

    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.destroy()


if __name__ == "__main__":
    main()
