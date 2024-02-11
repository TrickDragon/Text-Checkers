import json

class SimpleCheckers:
    def __init__(self):
        # Load high scores at the start
        self.high_scores = self.load_high_scores()

    def create_board(self):
        """Initialize the game board."""
        board = [[" " for _ in range(4)] for _ in range(4)]
        board[0][1], board[0][3] = "X", "X"  # Player X pieces
        board[3][0], board[3][2] = "O", "O"  # Player O pieces
        return board

    def get_player_names(self):
        """Prompt players for their names."""
        player_x = input("Enter name for player X: ")
        player_o = input("Enter name for player O: ")
        return {"X": player_x, "O": player_o} # Minus 1

    def print_board(self, board):
        """Print the current game board."""
        for row in board:
            print("|" + "|".join(row) + "|")
        print()  # Blank line for spacing

    def move_piece(self, board, start, end, current_turn):
        """Attempt to move a piece on the board."""
        sx, sy = start
        ex, ey = end
        # Validate move
        if sx < 0 or sx > 3 or sy < 0 or sy > 3 or ex < 0 or ex > 3 or ey < 0 or ey > 3:
            return False, "Move out of bounds."
        if board[sx][sy] != current_turn:
            return False, "Not your piece."
        if abs(sx - ex) > 1 or abs(sy - ey) > 1:
            return False, "Can only move to adjacent squares."
        if board[ex][ey] != " ":
            return False, "Target square is not empty."

        # Check if capturing opponent's piece
        if abs(sx - ex) == 1 and abs(sy - ey) == 1:
            opponent = "O" if current_turn == "X" else "X"
            if board[ex][ey] == opponent:
                print(f"{current_turn}'s piece captured {opponent}'s piece!")
                board[ex][ey] = " "  # Remove opponent's piece

        board[ex][ey] = board[sx][sy]  # Move the piece
        board[sx][sy] = " "
        return True, "Successfully moved."

    def change_turn(self, current_turn):
        """Switch turns between players."""
        return "O" if current_turn == "X" else "X"
    # Ternary Operator - You can return something and oput an if statement as long as there is not else if statement.

    def check_win(self, board):
        """Check if there's a winner."""
        pieces = {"X": 0, "O": 0}
        for row in board:
            for cell in row:
                if cell in pieces:
                    pieces[cell] += 1
        if pieces["X"] == 0:
            return "O"
        if pieces["O"] == 0:
            return "X"
        return None

    def load_high_scores(self):
        """Load high scores from a JSON file."""
        try:
            with open("high_scores.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_high_scores(self):
        """Save the current high scores to a JSON file."""
        with open("high_scores.json", "w") as file:
            json.dump(self.high_scores, file, indent=4)

    def update_high_scores(self, winner):
        """Update the high scores with the latest game result."""
        if winner in self.high_scores:
            self.high_scores[winner] += 1
        else:
            self.high_scores[winner] = 1
        self.save_high_scores()

    def display_high_scores(self):
        """Display the high scores."""
        print("High Scores:")
        for name, score in sorted(self.high_scores.items(), key=lambda item: item[1], reverse=True):
            # Minus 1
            print(f"{name}: {score}")
        print()

    def play_round(self):
        """Play a single round of the game."""
        board = self.create_board()
        players = self.get_player_names()
        current_turn = "X"
        game_over = False

        while not game_over:
            self.print_board(board)
            print(f"{players[current_turn]}'s turn (Player {current_turn})")
            start_pos = input("Enter start position (row,col) or 'q' to quit: ")
            if start_pos.lower() == "q":
                return False  # Quit the game

            end_pos = input("Enter end position (row,col): ")
            start = tuple(map(int, start_pos.split(',')))
            # Minus 1 - Does not actually check the numbers only splits it.
            end = tuple(map(int, end_pos.split(',')))
            # Minus 1 - Does not actually check the numbers only splits it.
            moved, message = self.move_piece(board, start, end, current_turn)
            if moved:
                winner = self.check_win(board)
                if winner:
                    print(f"{players[winner]} wins!")
                    self.update_high_scores(players[winner])
                    game_over = True
                current_turn = self.change_turn(current_turn)
            else:
                print(message)
        return True

    def play_game(self):
        """Start the game loop, offering the option to play multiple rounds."""
        playing = True
        while playing:
            playing = self.play_round()
            if playing:
                print("Round over. Play again? (Press 'q' to quit or any other key to continue)")
                choice = input().lower()
                if choice == "q":
                    break  # Exit the game loop
            self.display_high_scores()

if __name__ == "__main__":
    game = SimpleCheckers()
    game.play_game()
