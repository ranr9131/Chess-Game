import pygame
from constants import *
from Pieces import *

class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.create_board()
        self.is_checkmate = False
        self.winner_color = None

    def draw_squares(self,win):
        win.fill(GREEN)
        for row in range(ROWS):
            for col in range(row%2,ROWS,2):
                pygame.draw.rect(win,LIGHT_GREEN,(row*SQUARE_SIZE,col*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            # Filling board with empty spaces
            self.board.append([0 for i in range(8)])

            # Placing pieces
            if row == 0:
                current_color = BLACK
                self.board[row][0],self.board[row][7] = Rook(row,0,current_color),Rook(row,7,current_color)
                self.board[row][1],self.board[row][6] = Knight(row,1,current_color),Knight(row,6,current_color)
                self.board[row][2],self.board[row][5] = Bishop(row,2,current_color),Bishop(row,5,current_color)
                self.board[row][3] = Queen(row,3,current_color)
                self.board[row][4] = King(row,4,current_color)
            if row == 7:
                current_color = WHITE
                self.board[row][0],self.board[row][7] = Rook(row,0,current_color),Rook(row,7,current_color)
                self.board[row][1],self.board[row][6] = Knight(row,1,current_color),Knight(row,6,current_color)
                self.board[row][2],self.board[row][5] = Bishop(row,2,current_color),Bishop(row,5,current_color)
                self.board[row][3] = Queen(row,3,current_color)
                self.board[row][4] = King(row,4,current_color)
            if row == 1:
                current_color = BLACK
                for i in range(8):
                    self.board[row][i] = Pawn(row,i,current_color)
            if row == 6:
                current_color = WHITE
                for i in range(8):
                    self.board[row][i] = Pawn(row,i,current_color)


    def draw(self,win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] != 0:
                    self.board[row][col].draw(win)

    def move(self,piece,row,col):
        self.board[piece.row][piece.col],self.board[row][col] = self.board[row][col],self.board[piece.row][piece.col]
        piece.move(row,col)
        try:
            piece.has_moved = True
        except:
            pass

    def get_piece(self,row,col):
        return self.board[row][col]

    def get_all_possible_moves_team(self,board_list,piece):
        opposing_pieces_list = []
        for i in range(len(board_list)):
            for j in range(len(board_list[i])):
                if board_list[i][j] != 0:
                    if board_list[i][j].color != piece.color:
                        opposing_pieces_list.append(board_list[i][j])

        all_possible_moves_team = []
        for check_piece in opposing_pieces_list:
            try:
                if check_piece.is_pawn:
                    moves = check_piece.find_possible_moves(self,board_list,search_extra_diagonal=True).keys()
                    for move in moves:
                        all_possible_moves_team.append(move)
            except:
                moves = check_piece.find_possible_moves(self,board_list).keys()
                for move in moves:
                    all_possible_moves_team.append(move)

        return all_possible_moves_team

    def get_valid_moves(self,piece):
        moves = {}

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                try:
                    if self.board[i][j].is_king and self.board[i][j].color == piece.color:
                        king_pos = (self.board[i][j].row,self.board[i][j].col)
                except:
                    pass

        friendly_pieces = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != 0:
                    if self.board[i][j].color == piece.color:
                        friendly_pieces.append(self.board[i][j])

        if king_pos in self.get_all_possible_moves_team(self.board,piece):
            checkmate = True
            for friendly_piece in friendly_pieces:
                potential_moves = friendly_piece.find_possible_moves(self,self.board,self.get_all_possible_moves_team(self.board,friendly_piece),check_moves=True)
                if potential_moves != {}:
                    checkmate = False

            if checkmate:
                self.is_checkmate = True
                colors = [WHITE,BLACK]
                colors.remove(piece.color)
                self.winner_color = colors[0]
            else:
                moves = piece.find_possible_moves(self,self.board,self.get_all_possible_moves_team(self.board,piece),check_moves=True)
        else:
            moves = piece.find_possible_moves(self,self.board,self.get_all_possible_moves_team(self.board,piece),check_moves=True)

        return moves

    def winner(self):
        return self.winner_color
