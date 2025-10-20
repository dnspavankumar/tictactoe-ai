import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        master.title("Tic-Tac-Toe")

        # Center the window
        master.update_idletasks()
        width = master.winfo_width()
        height = master.winfo_height()
        x = (master.winfo_screenwidth() // 2) - (width // 2)
        y = (master.winfo_screenheight() // 2) - (height // 2)
        master.geometry(f'{width}x{height}+{x}+{y}')

        # Center the grid content
        for i in range(3):
            master.grid_rowconfigure(i, weight=1)
            master.grid_columnconfigure(i, weight=1)
        master.grid_rowconfigure(3, weight=1) # For status label
        master.grid_rowconfigure(4, weight=1) # For restart button

        self.board = [0] * 9  # 0: empty, 1: X, -1: O
        self.current_player = 1  # 1 for X, -1 for O
        self.is_game_active = True

        self.winning_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]

        self.buttons = []
        for i in range(9):
            button = tk.Button(master, text="", font=('Arial', 60, 'bold'), width=4, height=2, 
                               relief="raised", borderwidth=3, bg='lightgray',
                               command=lambda i=i: self.handle_click(i))
            button.grid(row=i // 3, column=i % 3, sticky="nsew", padx=2, pady=2)
            self.buttons.append(button)

        self.status_label = tk.Label(master, text="X's turn", font=('Arial', 20, 'bold'), pady=10)
        self.status_label.grid(row=3, column=0, columnspan=3)

        self.restart_button = tk.Button(master, text="Restart", font=('Arial', 15, 'bold'),
                                        command=self.restart_game, padx=10, pady=5)
        self.restart_button.grid(row=4, column=0, columnspan=3, pady=10)

    def handle_click(self, index):
        if self.board[index] == 0 and self.is_game_active:
            self.make_move(index, self.current_player)
            if self.is_game_active:
                self.check_game_result()
                if self.is_game_active:
                    self.ai_move()
                    self.check_game_result()

    def make_move(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text='X' if player == 1 else 'O')

    def check_game_result(self):
        winner = self.check_win()
        if winner:
            self.status_label.config(text=f"{ 'X' if winner == 1 else 'O'} wins!")
            self.is_game_active = False
        elif 0 not in self.board:
            self.status_label.config(text="It's a draw!")
            self.is_game_active = False
        else:
            self.current_player *= -1
            self.status_label.config(text=f"{ 'X' if self.current_player == 1 else 'O'}'s turn")

    def check_win(self):
        for condition in self.winning_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != 0:
                return self.board[condition[0]]
        return 0

    def ai_move(self):
        best_score = float('inf')
        best_move = -1

        for i in range(9):
            if self.board[i] == 0:
                self.board[i] = -1  # AI makes a move (O)
                score = self.minimax(self.board, 0, float('-inf'), float('inf'), True)
                self.board[i] = 0  # Undo the move

                if score < best_score:
                    best_score = score
                    best_move = i
        
        if best_move != -1:
            self.make_move(best_move, -1)

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        score = self.evaluate(board)

        if score == 10: return score - depth
        if score == -10: return score + depth
        if 0 not in board: return 0

        if is_maximizing:
            best = float('-inf')
            for i in range(9):
                if board[i] == 0:
                    board[i] = 1
                    best = max(best, self.minimax(board, depth + 1, alpha, beta, False))
                    alpha = max(alpha, best)
                    board[i] = 0
                    if beta <= alpha:
                        break
            return best
        else:
            best = float('inf')
            for i in range(9):
                if board[i] == 0:
                    board[i] = -1
                    best = min(best, self.minimax(board, depth + 1, alpha, beta, True))
                    beta = min(beta, best)
                    board[i] = 0
                    if beta <= alpha:
                        break
            return best

    def evaluate(self, board):
        for condition in self.winning_conditions:
            if board[condition[0]] == board[condition[1]] == board[condition[2]] != 0:
                return 10 if board[condition[0]] == 1 else -10
        return 0

    def restart_game(self):
        self.board = [0] * 9
        self.current_player = 1
        self.is_game_active = True
        for button in self.buttons:
            button.config(text="")
        self.status_label.config(text="X's turn")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()