import sys
import tkinter
import tkinter.messagebox
import pygame
import board

COLOR_WHITE = (255, 255, 255) 
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_BLACK = (0, 0, 0) 



class DisplayPane:
    def __init__(self, rows, cols, cell_size):
        self.board = board.GameBoard(rows, cols)
        self.cell_size = cell_size
        self.radius = cell_size // 2 - 5
        self.width = cols * cell_size
        self.height = (rows + 1) * cell_size
        self.row_offset = cell_size
        self.circle_offset = cell_size // 2
        self.screen = pygame.display.set_mode((self.width, self.height))

    def render_background(self):
 
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                left = c * self.cell_size
                top = r * self.cell_size + self.row_offset
                pygame.draw.rect(self.screen, COLOR_WHITE, (left, top, self.cell_size, self.cell_size))
                pygame.draw.circle(self.screen, COLOR_BLACK, (left + self.circle_offset, top + self.circle_offset), self.radius)
        pygame.display.update()

    def update_pieces(self):
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                if self.board.grid[r, c] == 1:
                    piece_color = COLOR_RED
                elif self.board.grid[r, c] == 2:
                    piece_color = COLOR_YELLOW
                else:
                    piece_color = COLOR_BLACK
                x_pos = c * self.cell_size + self.circle_offset
                y_pos = self.height - (r * self.cell_size + self.circle_offset)
                pygame.draw.circle(self.screen, piece_color, (x_pos, y_pos), self.radius)
        pygame.display.update()

    def move_mouse(self, x_pos, current_color):
        pygame.draw.rect(self.screen, COLOR_BLACK, (0, 0, self.width, self.cell_size))  
        pygame.draw.circle(self.screen, current_color, (x_pos, self.circle_offset), self.radius)
        pygame.display.update()

    def try_placing_piece(self, x_pos, player):
        col = x_pos // self.cell_size
        if self.board.is_location_open(col):
            row = self.board.find_open_row(col)
            self.board.place_piece(row, col, player)
            return True
        return False

    def restart_game(self):
        self.screen = pygame.display.set_mode((self.width, self.height)) 
        self.board.reset_board()
        self.render_background()
        self.update_pieces()


def game_over_prompt(winner=None):
    title = 'Game Over!'
    message = f'Player {winner} won the game! Do you want to Play again?' if winner else 'It was a tie. Play again?'
    return tkinter.messagebox.askyesno(title=title, message=message)


def main():
    tkinter.Tk().wm_withdraw()  
    pygame.init()
    pygame.display.set_caption('Connect 4!')
    display = DisplayPane(6, 7, 90)
    display.render_background()
    continue_game = True
    current_turn = 1
    current_piece_color = COLOR_RED

    while continue_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                display.move_mouse(event.pos[0], current_piece_color)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if display.try_placing_piece(event.pos[0], current_turn):
                    display.update_pieces()
                    if display.board.check_for_four(current_turn):  
                        continue_game = game_over_prompt(current_turn)
                        display.restart_game()
                    elif display.board.is_grid_full():  
                        continue_game = game_over_prompt()
                        display.restart_game()
                    else: 
                        current_turn = 1 if current_turn == 2 else 2
                        current_piece_color = COLOR_RED if current_turn == 1 else COLOR_YELLOW
                        display.move_mouse(event.pos[0], current_piece_color)


if __name__ == "__main__":
    main()
