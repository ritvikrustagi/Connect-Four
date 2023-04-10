import numpy as np

class GameBoard:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols))

    def is_location_open(self, col):
        return self.grid[self.rows - 1, col] == 0

    def find_open_row(self, col):
        for row in range(self.rows):
            if self.grid[row, col] == 0:
                return row

    def place_piece(self, row, col, player):
        self.grid[row, col] = player

    def check_for_four(self, player):
        for c in range(self.cols):
            for r in range(self.rows - 3):
                if all(self.grid[r + i, c] == player for i in range(4)):
                    return True

        for r in range(self.rows):
            for c in range(self.cols - 3):
                if all(self.grid[r, c + i] == player for i in range(4)):
                    return True

        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                if all(self.grid[r + i, c + i] == player for i in range(4)):
                    return True

        for r in range(3, self.rows):
            for c in range(self.cols - 3):
                if all(self.grid[r - i, c + i] == player for i in range(4)):
                    return True

        return False

    def is_grid_full(self):
        return self.grid.all()

    def reset_board(self):
        self.grid = np.zeros((self.rows, self.cols))

    def show_grid(self):
        print(np.flip(self.grid, 0))
