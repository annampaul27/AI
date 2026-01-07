import tkinter as tk
from tkinter import messagebox, simpledialog

PLAYER_X = "X"
PLAYER_O = "O"


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - Human / AI")
        self.root.resizable(False, False)

        # Colors & style
        self.bg_color = "#1e1e2f"
        self.grid_color = "#33334d"
        self.x_color = "#ff6b6b"
        self.o_color = "#4ecdc4"
        self.text_color = "#f7fff7"
        self.accent_color = "#ffe66d"

        self.root.configure(bg=self.bg_color)

        # Game / player state
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_over = False

        # Player meta
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        self.player1_symbol = PLAYER_X
        self.player2_symbol = PLAYER_O
        self.vs_ai = False  # False: Human vs Human, True: Human vs AI

        # Current player symbol
        self.current_player = PLAYER_X

        # Scores (scoreboard)
        self.score_x = 0
        self.score_o = 0
        self.score_draw = 0

        self._build_ui()
        self.show_start_dialog()

    # ---------- UI ----------
    def _build_ui(self):
        title_label = tk.Label(
            self.root,
            text="Tic Tac Toe",
            font=("Segoe UI", 20, "bold"),
            bg=self.bg_color,
            fg=self.accent_color,
            pady=10,
        )
        title_label.pack()

        # grid frame
        grid_frame = tk.Frame(self.root, bg=self.bg_color, padx=10, pady=10)
        grid_frame.pack()

        for r in range(3):
            for c in range(3):
                btn = tk.Button(
                    grid_frame,
                    text="",
                    font=("Segoe UI", 28, "bold"),
                    width=3,
                    height=1,
                    bg=self.grid_color,
                    fg=self.text_color,
                    activebackground="#444466",
                    activeforeground=self.text_color,
                    bd=0,
                    relief="flat",
                    command=lambda row=r, col=c: self.handle_click(row, col),
                )
                btn.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[r][c] = btn

        # status label
        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Segoe UI", 14),
            bg=self.bg_color,
            fg=self.text_color,
            pady=5,
        )
        self.status_label.pack()

        # scoreboard label
        self.score_label = tk.Label(
            self.root,
            text="X: 0 | O: 0 | Draws: 0",
            font=("Segoe UI", 12, "bold"),
            bg=self.bg_color,
            fg=self.accent_color,
            pady=5,
        )
        self.score_label.pack()

        # control buttons
        controls = tk.Frame(self.root, bg=self.bg_color)
        controls.pack(pady=(0, 10))

        replay_button = tk.Button(
            controls,
            text="Replay",
            font=("Segoe UI", 11, "bold"),
            bg=self.accent_color,
            fg="#000000",
            activebackground="#ffdd55",
            activeforeground="#000000",
            bd=0,
            padx=15,
            pady=5,
            command=self.reset_board_only,  # just replay same match
        )
        replay_button.grid(row=0, column=0, padx=5)

        play_ai_button = tk.Button(
            controls,
            text="Play vs AI",
            font=("Segoe UI", 11, "bold"),
            bg="#ffaf40",
            fg="#000000",
            activebackground="#ffbf60",
            activeforeground="#000000",
            bd=0,
            padx=15,
            pady=5,
            command=self.toggle_ai_mode,
        )
        play_ai_button.grid(row=0, column=1, padx=5)

        new_match_button = tk.Button(
            controls,
            text="New Match",
            font=("Segoe UI", 11, "bold"),
            bg="#ff7675",
            fg="#000000",
            activebackground="#ff9f9a",
            activeforeground="#000000",
            bd=0,
            padx=15,
            pady=5,
            command=self.new_match_with_dialog,
        )
        new_match_button.grid(row=0, column=2, padx=5)

    # ---------- Start / mode dialogs ----------
    def show_start_dialog(self):
        self.player1_name = simpledialog.askstring(
            "Player 1", "Enter Player 1 name:", initialvalue="Player 1", parent=self.root
        ) or "Player 1"

        mode = messagebox.askyesno(
            "Game Mode",
            "Play against AI?\n\nYes: Player 1 vs AI\nNo: Player 1 vs Player 2",
        )
        self.vs_ai = mode

        if not self.vs_ai:
            self.player2_name = simpledialog.askstring(
                "Player 2",
                "Enter Player 2 name:",
                initialvalue="Player 2",
                parent=self.root,
            ) or "Player 2"
        else:
            self.player2_name = "Computer"

        choice = messagebox.askyesno(
            "Symbol Choice",
            f"Should {self.player1_name} be X?\n\nYes: {self.player1_name} = X, {self.player2_name} = O\nNo: {self.player1_name} = O, {self.player2_name} = X",
        )

        if choice:
            self.player1_symbol = PLAYER_X
            self.player2_symbol = PLAYER_O
        else:
            self.player1_symbol = PLAYER_O
            self.player2_symbol = PLAYER_X

        self.current_player = PLAYER_X
        self.update_status()

        if self.vs_ai and self.get_current_player_name() == "Computer":
            self.root.after(300, self.ai_move)

    def toggle_ai_mode(self):
        # Toggle between vs human and vs AI, keep scores
        self.vs_ai = not self.vs_ai
        if self.vs_ai:
            self.player2_name = "Computer"
            messagebox.showinfo("Mode", "Switched to: Player vs AI")
        else:
            name = simpledialog.askstring(
                "Player 2", "Enter Player 2 name:", initialvalue="Player 2", parent=self.root
            ) or "Player 2"
            self.player2_name = name
            messagebox.showinfo("Mode", "Switched to: Player vs Player")
        self.reset_board_only()

    def new_match_with_dialog(self):
        # Reset scores and re-ask everything
        self.score_x = 0
        self.score_o = 0
        self.score_draw = 0
        self.update_scores_label()
        self.reset_board_only()
        self.show_start_dialog()

    # ---------- Helpers ----------
    def get_current_player_name(self):
        if self.current_player == self.player1_symbol:
            return self.player1_name
        else:
            return self.player2_name

    def update_status(self, extra=""):
        player_name = self.get_current_player_name()
        self.status_label.config(
            text=f"Turn: {player_name} ({self.current_player}) {extra}"
        )

    def update_scores_label(self):
        self.score_label.config(
            text=f"X: {self.score_x} | O: {self.score_o} | Draws: {self.score_draw}"
        )

    # ---------- Game actions ----------
    def handle_click(self, row, col):
        if self.game_over:
            return

        if self.vs_ai and self.get_current_player_name() == "Computer":
            return

        if self.board[row][col] is not None:
            return

        self.make_move(row, col, self.current_player)

        winner = self._check_winner()
        if winner:
            self.handle_winner(winner)
            return
        elif self._is_draw():
            self.handle_draw()
            return

        self._switch_player()
        self.update_status()

        if self.vs_ai and self.get_current_player_name() == "Computer" and not self.game_over:
            self.root.after(300, self.ai_move)

    def make_move(self, row, col, symbol):
        self.board[row][col] = symbol
        self._update_button(row, col)

    def _update_button(self, row, col):
        symbol = self.board[row][col]
        btn = self.buttons[row][col]
        btn.config(text=symbol)
        if symbol == PLAYER_X:
            btn.config(fg=self.x_color)
        else:
            btn.config(fg=self.o_color)

    def _switch_player(self):
        self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X

    def handle_winner(self, winner):
        self.game_over = True
        if winner == PLAYER_X:
            self.score_x += 1
        else:
            self.score_o += 1
        self.update_scores_label()

        winner_name = (
            self.player1_name if (winner == self.player1_symbol) else self.player2_name
        )
        msg = f"{winner_name} ({winner}) wins!"
        self.status_label.config(text=msg)
        messagebox.showinfo("Game Over", msg)

    def handle_draw(self):
        self.game_over = True
        self.score_draw += 1
        self.update_scores_label()
        self.status_label.config(text="It's a draw!")
        messagebox.showinfo("Game Over", "It's a draw!")

    def reset_board_only(self):
        # Replay: reset only the board, keep scores and mode
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.game_over = False
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text="", bg=self.grid_color, fg=self.text_color)
        self.current_player = PLAYER_X
        self.update_status()

        if self.vs_ai and self.get_current_player_name() == "Computer":
            self.root.after(300, self.ai_move)

    # ---------- Winner / draw checks ----------
    def _check_winner(self):
        b = self.board

        # rows
        for r in range(3):
            if b[r][0] and b[r][0] == b[r][1] == b[r][2]:
                self._highlight_winning_cells([(r, 0), (r, 1), (r, 2)])
                return b[r][0]

        # cols
        for c in range(3):
            if b[0][c] and b[0][c] == b[1][c] == b[2][c]:
                self._highlight_winning_cells([(0, c), (1, c), (2, c)])
                return b[0][c]

        # diagonals
        if b[0][0] and b[0][0] == b[1][1] == b[2][2]:
            self._highlight_winning_cells([(0, 0), (1, 1), (2, 2)])
            return b[0][0]

        if b[0][2] and b[0][2] == b[1][1] == b[2][0]:
            self._highlight_winning_cells([(0, 2), (1, 1), (2, 0)])
            return b[0][2]

        return None

    def _highlight_winning_cells(self, cells):
        for r, c in cells:
            self.buttons[r][c].config(bg="#2ecc71")

    def _is_draw(self):
        for r in range(3):
            for c in range(3):
                if self.board[r][c] is None:
                    return False
        return True

    # ---------- Minimax AI ----------
    def ai_move(self):
        if self.game_over:
            return

        ai_symbol = self.player2_symbol if self.get_current_player_name() == "Computer" else self.player1_symbol
        human_symbol = PLAYER_X if ai_symbol == PLAYER_O else PLAYER_O

        best_score = float("-inf")
        best_move = None

        for r in range(3):
            for c in range(3):
                if self.board[r][c] is None:
                    self.board[r][c] = ai_symbol
                    score = self.minimax(False, ai_symbol, human_symbol)
                    self.board[r][c] = None
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)

        if best_move is not None:
            r, c = best_move
            self.make_move(r, c, ai_symbol)

        winner = self._check_winner()
        if winner:
            self.handle_winner(winner)
            return
        elif self._is_draw():
            self.handle_draw()
            return

        self.current_player = human_symbol
        self.update_status()

    def minimax(self, is_maximizing, ai_symbol, human_symbol):
        winner = self._winner_for_minimax()
        if winner == ai_symbol:
            return 1
        elif winner == human_symbol:
            return -1
        elif self._is_draw():
            return 0

        if is_maximizing:
            best_score = float("-inf")
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] is None:
                        self.board[r][c] = ai_symbol
                        score = self.minimax(False, ai_symbol, human_symbol)
                        self.board[r][c] = None
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = float("inf")
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] is None:
                        self.board[r][c] = human_symbol
                        score = self.minimax(True, ai_symbol, human_symbol)
                        self.board[r][c] = None
                        best_score = min(best_score, score)
            return best_score

    def _winner_for_minimax(self):
        b = self.board

        for r in range(3):
            if b[r][0] and b[r][0] == b[r][1] == b[r][2]:
                return b[r][0]
        for c in range(3):
            if b[0][c] and b[0][c] == b[1][c] == b[2][c]:
                return b[0][c]
        if b[0][0] and b[0][0] == b[1][1] == b[2][2]:
            return b[0][0]
        if b[0][2] and b[0][2] == b[1][1] == b[2][0]:
            return b[0][2]
        return None


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
