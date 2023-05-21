from constants import *
from board import *

class Game:
    def __init__(self,win):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_moves(self.valid_moves)
        pygame.display.update()

    def reset(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}

    def select(self,row,col):
        if self.selected:
            result = self.move(row,col)

            if not result:
                self.selected = None
                self.select(row,col)
        piece = self.board.get_piece(row,col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False

    def move(self,row,col):
        piece = self.board.get_piece(row,col)
        # if self.selected and piece == 0 and (row,col) in self.valid_moves:
        if self.selected and (row,col) in self.valid_moves:
            # self.board.move(self.selected,row,col)
            removed = self.valid_moves[(row,col)]
            if removed:
                self.remove_piece(*removed)

            temp_row = self.selected.row
            temp_col = self.selected.col

            self.board.move(self.selected,row,col)

            try:
                if self.selected.is_pawn:
                    if row in [0,7]:
                        self.board.board[row][col] = Queen(row,col,self.selected.color)
            except:
                pass

            try:
                if self.selected.is_king and self.selected.castle:
                    # (self.selected.row,self.col+2)
                    if (row,col) == (temp_row,temp_col-2):
                        self.board.board[self.selected.row][0].has_moved = True

                        self.board.move(self.board.board[self.selected.row][0],temp_row,3)
                        self.selected.castle = False


                    if (row,col) == (temp_row,temp_col+2):
                        self.board.board[self.selected.row][7].has_moved = True
                        self.board.move(self.board.board[self.selected.row][7],temp_row,5)
                        self.selected.castle = False
            except:
                pass


            self.change_turn()

        else:
            return False
        return True

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

    def remove_piece(self,row,col):
        self.board.board[row][col] = 0

    def draw_moves(self,moves):
        for move in moves:
            row,col = move
            pygame.draw.circle(self.win,BLUE,((col*SQUARE_SIZE)+(SQUARE_SIZE//2),(row*SQUARE_SIZE)+(SQUARE_SIZE//2)),15)

    def winner(self):
        return self.board.winner()
