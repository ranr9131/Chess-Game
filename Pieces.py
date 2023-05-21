import pygame
from constants import *
import copy
import os

# Main piece class
class Piece:
    def __init__(self,row,col,color):
        self.row = row
        self.col = col
        self.color = color
        # if self.color == WHITE:
        #     self.direction = -1
        # else:
        #     self.direction = 1

        self.x = 0
        self.y = 0
        self.calc_position()

    def calc_position(self):
        self.x = (SQUARE_SIZE*self.col) + (SQUARE_SIZE//2)
        self.y = (SQUARE_SIZE*self.row) + (SQUARE_SIZE//2)

    def move(self,row,col):
        self.row = row
        self.col = col
        self.calc_position()

    def fix_check(self,board_object,board_grid,piece_possible_moves,king_moved=False):
        if not king_moved:
            possible_moves_copy = piece_possible_moves.copy()
            board_grid_copy = copy.deepcopy(board_grid)


            for i in range(len(board_grid)):
                for j in range(len(board_grid[i])):
                    try:
                        if board_grid[i][j].is_king and board_grid[i][j].color == self.color:
                            king_pos = (board_grid[i][j].row,board_grid[i][j].col)
                    except:
                        pass


            for move in possible_moves_copy.copy().keys():

                board_copy = copy.deepcopy(board_grid_copy)

                board_copy[move[0]][move[1]] = board_copy[self.row][self.col]
                board_copy[self.row][self.col] = 0

                try:
                    if king_pos in board_object.get_all_possible_moves_team(board_copy,board_grid_copy[self.row][self.col]):
                        del possible_moves_copy[move]

                except:
                    pass


            return possible_moves_copy

        else:
            possible_moves_copy = piece_possible_moves.copy()
            board_grid_copy = copy.deepcopy(board_grid)

            for move in possible_moves_copy.copy().keys():
                board_copy = copy.deepcopy(board_grid_copy)

                if (move[0],move[1]) in board_object.get_all_possible_moves_team(board_copy,board_grid_copy[self.row][self.col]):
                    del possible_moves_copy[move]

            return possible_moves_copy


# Subclasses
class Pawn(Piece):
    def __init__(self,row,col,color):
        super().__init__(row,col,color)
        self.has_moved = False
        self.is_pawn = True

    def draw(self,win):
        if self.color == BLACK:
            pawn_sprite = pygame.image.load(os.path.join("Sprites","pawn_black.ppm"))
        else:
            pawn_sprite = pygame.image.load(os.path.join("Sprites","pawn_white.ppm"))
        pawn_sprite.set_colorkey((255,0,0))
        pawn_sprite = pygame.transform.scale(pawn_sprite,(SQUARE_SIZE-20,SQUARE_SIZE-20))
        win.blit(pawn_sprite,(self.x - ((SQUARE_SIZE-20)//2),self.y - ((SQUARE_SIZE-20)//2)))

    def find_possible_moves(self,board_object,board,opposing_moves=None,search_extra_diagonal=False,check_moves=False):
        possible_moves = {}
        if self.color == WHITE:
            if self.row > 0 and self.col > 0:
                if board[self.row-1][self.col-1] != 0:
                    if board[self.row-1][self.col-1].color != self.color:
                        possible_moves[(self.row-1,self.col-1)] = (self.row-1,self.col-1)
                else:
                    possible_moves[(self.row-1,self.col-1)] = None
            if self.row > 0 and self.col < 7:
                if board[self.row-1][self.col+1] != 0:
                    if board[self.row-1][self.col+1].color != self.color:
                        possible_moves[(self.row-1,self.col+1)] = (self.row-1,self.col+1)
                else:
                    possible_moves[(self.row-1,self.col+1)] = None

            if not self.has_moved:
                if board[self.row-1][self.col] == 0:
                    possible_moves[(self.row-1,self.col)] = 0
                if board[self.row-2][self.col] == 0 and board[self.row-1][self.col] == 0:
                    possible_moves[(self.row-2,self.col)] = 0
            else:
                # if (self.row-1) > 0:
                if (self.row) > 0:
                    if board[self.row-1][self.col] == 0:
                        possible_moves[(self.row-1,self.col)] = 0
        else:
            if self.row < 7 and self.col > 0:
                if board[self.row+1][self.col-1] != 0:
                    if board[self.row+1][self.col-1].color != self.color:
                        possible_moves[(self.row+1,self.col-1)] = (self.row+1,self.col-1)
                else:
                    possible_moves[(self.row+1,self.col-1)] = None
            if self.row < 7 and self.col < 7:
                if board[self.row+1][self.col+1] != 0:
                    if board[self.row+1][self.col+1].color != self.color:
                        possible_moves[(self.row+1,self.col+1)] = (self.row+1,self.col+1)
                else:
                    possible_moves[(self.row+1,self.col+1)] = None

            if not self.has_moved:
                if board[self.row+1][self.col] == 0:
                    possible_moves[(self.row+1,self.col)] = 0
                if board[self.row+2][self.col] == 0 and board[self.row+1][self.col] == 0:
                    possible_moves[(self.row+2,self.col)] = 0
            else:
                # if (self.row+1) < 7:
                if (self.row) < 7:
                    if board[self.row+1][self.col] == 0:
                        possible_moves[(self.row+1,self.col)] = 0

        if not search_extra_diagonal:
            for possible_move in possible_moves.copy().keys():
                if possible_moves.copy()[possible_move] == None:
                    del possible_moves[possible_move]

        if check_moves:
            possible_moves = self.fix_check(board_object,board,possible_moves)


        return possible_moves


class Rook(Piece):
    def __init__(self,row,col,color):
        super().__init__(row,col,color)
        self.has_moved = False
        self.is_rook = True

    def draw(self,win):
        if self.color == BLACK:
            rook_sprite = pygame.image.load(os.path.join("Sprites","rook_black.ppm"))
        else:
            rook_sprite = pygame.image.load(os.path.join("Sprites","rook_white.ppm"))
        rook_sprite.set_colorkey((255,0,0))
        rook_sprite = pygame.transform.scale(rook_sprite,(SQUARE_SIZE-20,SQUARE_SIZE-20))
        win.blit(rook_sprite,(self.x - ((SQUARE_SIZE-20)//2),self.y - ((SQUARE_SIZE-20)//2)))

    def find_possible_moves(self,board_object,board,opposing_moves=None,check_moves=False):
        possible_moves = {}

        row_counter = self.row
        searching = True
        while searching:
            row_counter += 1
            if row_counter <= 7:
                if board[row_counter][self.col] == 0:
                    possible_moves[(row_counter,self.col)] = 0
                else:
                    if board[row_counter][self.col].color == self.color:
                        searching = False
                    else:
                        possible_moves[(row_counter,self.col)] = (row_counter,self.col)
                        searching = False
            else:
                searching = False

        row_counter = self.row
        searching = True
        while searching:
            row_counter -= 1
            if row_counter >= 0:
                if board[row_counter][self.col] == 0:
                    possible_moves[(row_counter,self.col)] = 0
                else:
                    if board[row_counter][self.col].color == self.color:
                        searching = False
                    else:
                        possible_moves[(row_counter,self.col)] = (row_counter,self.col)
                        searching = False
            else:
                searching = False

        col_counter = self.col
        searching = True
        while searching:
            col_counter += 1
            if col_counter <= 7:
                if board[self.row][col_counter] == 0:
                    possible_moves[(self.row,col_counter)] = 0
                else:
                    if board[self.row][col_counter].color == self.color:
                        searching = False
                    else:
                        possible_moves[(self.row,col_counter)] = (self.row,col_counter)
                        searching = False
            else:
                searching = False

        col_counter = self.col
        searching = True
        while searching:
            col_counter -= 1
            if col_counter >= 0:
                if board[self.row][col_counter] == 0:
                    possible_moves[(self.row,col_counter)] = 0
                else:
                    if board[self.row][col_counter].color == self.color:
                        searching = False
                    else:
                        possible_moves[(self.row,col_counter)] = (self.row,col_counter)
                        searching = False
            else:
                searching = False

        if check_moves:
            possible_moves = self.fix_check(board_object,board,possible_moves)

        return possible_moves

class Knight(Piece):
    def draw(self,win):
        if self.color == BLACK:
            knight_sprite = pygame.image.load(os.path.join("Sprites","knight_black.ppm"))
        else:
            knight_sprite = pygame.image.load(os.path.join("Sprites","knight_white.ppm"))
        knight_sprite.set_colorkey((255,0,0))
        knight_sprite = pygame.transform.scale(knight_sprite,(SQUARE_SIZE-20,SQUARE_SIZE-20))
        win.blit(knight_sprite,(self.x - ((SQUARE_SIZE-20)//2),self.y - ((SQUARE_SIZE-20)//2)))

    def find_possible_moves(self,board_object,board,opposing_moves=None,check_moves=False):
        possible_moves = {}
        if (self.row-2) >= 0 and (self.col-1) >= 0:
            if board[self.row-2][self.col-1] == 0:
                possible_moves[(self.row-2,self.col-1)] = 0
            elif board[self.row-2][self.col-1].color != self.color:
                possible_moves[(self.row-2,self.col-1)] = (self.row-2,self.col-1)
        if (self.row-2) >= 0 and (self.col+1) <= 7:
            if board[self.row-2][self.col+1] == 0:
                possible_moves[(self.row-2,self.col+1)] = 0
            elif board[self.row-2][self.col+1].color != self.color:
                possible_moves[(self.row-2,self.col+1)] = (self.row-2,self.col+1)
        if (self.row-1) >= 0 and (self.col-2) >= 0:
            if board[self.row-1][self.col-2] == 0:
                possible_moves[(self.row-1,self.col-2)] = 0
            elif board[self.row-1][self.col-2].color != self.color:
                possible_moves[(self.row-1,self.col-2)] = (self.row-1,self.col-2)
        if (self.row-1) >= 0 and (self.col+2) <= 7:
            if board[self.row-1][self.col+2] == 0:
                possible_moves[(self.row-1,self.col+2)] = 0
            elif board[self.row-1][self.col+2].color != self.color:
                possible_moves[(self.row-1,self.col+2)] = (self.row-1,self.col+2)
        if (self.row+1) <= 7 and (self.col-2) >= 0:
            if board[self.row+1][self.col-2] == 0:
                possible_moves[(self.row+1,self.col-2)] = 0
            elif board[self.row+1][self.col-2].color != self.color:
                possible_moves[(self.row+1,self.col-2)] = (self.row+1,self.col-2)
        if (self.row+1) <= 7 and (self.col+2) <= 7:
            if board[self.row+1][self.col+2] == 0:
                possible_moves[(self.row+1,self.col+2)] = 0
            elif board[self.row+1][self.col+2].color != self.color:
                possible_moves[(self.row+1,self.col+2)] = (self.row+1,self.col+2)
        if (self.row+2) <= 7 and (self.col-1) >= 0:
            if board[self.row+2][self.col-1] == 0:
                possible_moves[(self.row+2,self.col-1)] = 0
            elif board[self.row+2][self.col-1].color != self.color:
                possible_moves[(self.row+2,self.col-1)] = (self.row+2,self.col-1)
        if (self.row+2) <= 7 and (self.col+1) <= 7:
            if board[self.row+2][self.col+1] == 0:
                possible_moves[(self.row+2,self.col+1)] = 0
            elif board[self.row+2][self.col+1].color != self.color:
                possible_moves[(self.row+2,self.col+1)] = (self.row+2,self.col+1)

        if check_moves:
            possible_moves = self.fix_check(board_object,board,possible_moves)

        return possible_moves


class Bishop(Piece):
    def draw(self,win):
        if self.color == BLACK:
            bishop_sprite = pygame.image.load(os.path.join("Sprites","bishop_black.ppm"))
        else:
            bishop_sprite = pygame.image.load(os.path.join("Sprites","bishop_white.ppm"))
        bishop_sprite.set_colorkey((255,0,0))
        bishop_sprite = pygame.transform.scale(bishop_sprite,(SQUARE_SIZE-20,SQUARE_SIZE-20))
        win.blit(bishop_sprite,(self.x - ((SQUARE_SIZE-20)//2),self.y - ((SQUARE_SIZE-20)//2)))

    def find_possible_moves(self,board_object,board,opposing_moves=None,check_moves=False):
        possible_moves = {}

        for direction in [[1,-1],[-1,1],[1,1],[-1,-1]]:
            if [[1,-1],[-1,1],[1,1],[-1,-1]].index(direction) == 0:
                row_counter = self.row + direction[0]
                col_counter = self.col + direction[1]
                searching = True
                while searching:
                    if row_counter <= 7 and col_counter >= 0:
                        if board[row_counter][col_counter] == 0:
                            possible_moves[(row_counter,col_counter)] = 0
                        else:
                            if board[row_counter][col_counter].color == self.color:
                                searching = False
                            else:
                                possible_moves[(row_counter,col_counter)] = (row_counter,col_counter)
                                searching = False
                    else:
                        searching = False

                    row_counter += direction[0]
                    col_counter += direction[1]

            if [[1,-1],[-1,1],[1,1],[-1,-1]].index(direction) == 1:
                row_counter = self.row + direction[0]
                col_counter = self.col + direction[1]
                searching = True
                while searching:
                    if row_counter >= 0 and col_counter <= 7:

                        if board[row_counter][col_counter] == 0:
                            possible_moves[(row_counter,col_counter)] = 0
                        else:
                            if board[row_counter][col_counter].color == self.color:
                                searching = False
                            else:
                                possible_moves[(row_counter,col_counter)] = (row_counter,col_counter)
                                searching = False
                    else:
                        searching = False

                    row_counter += direction[0]
                    col_counter += direction[1]

            if [[1,-1],[-1,1],[1,1],[-1,-1]].index(direction) == 2:
                row_counter = self.row + direction[0]
                col_counter = self.col + direction[1]
                searching = True
                while searching:
                    if row_counter <= 7 and col_counter <= 7:
                        if board[row_counter][col_counter] == 0:
                            possible_moves[(row_counter,col_counter)] = 0
                        else:
                            if board[row_counter][col_counter].color == self.color:
                                searching = False
                            else:
                                possible_moves[(row_counter,col_counter)] = (row_counter,col_counter)
                                searching = False
                    else:
                        searching = False

                    row_counter += direction[0]
                    col_counter += direction[1]

            if [[1,-1],[-1,1],[1,1],[-1,-1]].index(direction) == 3:
                row_counter = self.row + direction[0]
                col_counter = self.col + direction[1]
                searching = True
                while searching:
                    if row_counter >= 0 and col_counter >= 0:
                        if board[row_counter][col_counter] == 0:
                            possible_moves[(row_counter,col_counter)] = 0
                        else:
                            if board[row_counter][col_counter].color == self.color:
                                searching = False
                            else:
                                possible_moves[(row_counter,col_counter)] = (row_counter,col_counter)
                                searching = False
                    else:
                        searching = False

                    row_counter += direction[0]
                    col_counter += direction[1]

        if check_moves:
            possible_moves = self.fix_check(board_object,board,possible_moves)

        return possible_moves


class Queen(Piece):
    def draw(self,win):
        if self.color == BLACK:
            queen_sprite = pygame.image.load(os.path.join("Sprites","queen_black.ppm"))
        else:
            queen_sprite = pygame.image.load(os.path.join("Sprites","queen_white.ppm"))
        queen_sprite.set_colorkey((255,0,0))
        queen_sprite = pygame.transform.scale(queen_sprite,(SQUARE_SIZE-20,SQUARE_SIZE-20))
        win.blit(queen_sprite,(self.x - ((SQUARE_SIZE-20)//2),self.y - ((SQUARE_SIZE-20)//2)))

    def find_possible_moves(self,board_object,board,opposing_moves=None,check_moves=False):
        possible_moves = {}

        for direction in [[1,-1],[-1,1],[1,1],[-1,-1]]:
            if [[1,-1],[-1,1],[1,1],[-1,-1]].index(direction) == 0:
                row_counter = self.row + direction[0]
                col_counter = self.col + direction[1]
                searching = True
                while searching:
                    if row_counter <= 7 and col_counter >= 0:
                        if board[row_counter][col_counter] == 0:
                            possible_moves[(row_counter,col_counter)] = 0
                        else:
                            if board[row_counter][col_counter].color == self.color:
                                searching = False
                            else:
                                possible_moves[(row_counter,col_counter)] = (row_counter,col_counter)
                                searching = False
                    else:
                        searching = False

                    row_counter += direction[0]
                    col_counter += direction[1]

            if [[1,-1],[-1,1],[1,1],[-1,-1]].index(direction) == 1:
                row_counter = self.row + direction[0]
                col_counter = self.col + direction[1]
                searching = True
                while searching:
                    if row_counter >= 0 and col_counter <= 7:

                        if board[row_counter][col_counter] == 0:
                            possible_moves[(row_counter,col_counter)] = 0
                        else:
                            if board[row_counter][col_counter].color == self.color:
                                searching = False
                            else:
                                possible_moves[(row_counter,col_counter)] = (row_counter,col_counter)
                                searching = False
                    else:
                        searching = False

                    row_counter += direction[0]
                    col_counter += direction[1]

            if [[1,-1],[-1,1],[1,1],[-1,-1]].index(direction) == 2:
                row_counter = self.row + direction[0]
                col_counter = self.col + direction[1]
                searching = True
                while searching:
                    if row_counter <= 7 and col_counter <= 7:
                        if board[row_counter][col_counter] == 0:
                            possible_moves[(row_counter,col_counter)] = 0
                        else:
                            if board[row_counter][col_counter].color == self.color:
                                searching = False
                            else:
                                possible_moves[(row_counter,col_counter)] = (row_counter,col_counter)
                                searching = False
                    else:
                        searching = False

                    row_counter += direction[0]
                    col_counter += direction[1]

            if [[1,-1],[-1,1],[1,1],[-1,-1]].index(direction) == 3:
                row_counter = self.row + direction[0]
                col_counter = self.col + direction[1]
                searching = True
                while searching:
                    if row_counter >= 0 and col_counter >= 0:
                        if board[row_counter][col_counter] == 0:
                            possible_moves[(row_counter,col_counter)] = 0
                        else:
                            if board[row_counter][col_counter].color == self.color:
                                searching = False
                            else:
                                possible_moves[(row_counter,col_counter)] = (row_counter,col_counter)
                                searching = False
                    else:
                        searching = False

                    row_counter += direction[0]
                    col_counter += direction[1]

        row_counter = self.row
        searching = True
        while searching:
            row_counter += 1
            if row_counter <= 7:
                if board[row_counter][self.col] == 0:
                    possible_moves[(row_counter,self.col)] = 0
                else:
                    if board[row_counter][self.col].color == self.color:
                        searching = False
                    else:
                        possible_moves[(row_counter,self.col)] = (row_counter,self.col)
                        searching = False
            else:
                searching = False

        row_counter = self.row
        searching = True
        while searching:
            row_counter -= 1
            if row_counter >= 0:
                if board[row_counter][self.col] == 0:
                    possible_moves[(row_counter,self.col)] = 0
                else:
                    if board[row_counter][self.col].color == self.color:
                        searching = False
                    else:
                        possible_moves[(row_counter,self.col)] = (row_counter,self.col)
                        searching = False
            else:
                searching = False

        col_counter = self.col
        searching = True
        while searching:
            col_counter += 1
            if col_counter <= 7:
                if board[self.row][col_counter] == 0:
                    possible_moves[(self.row,col_counter)] = 0
                else:
                    if board[self.row][col_counter].color == self.color:
                        searching = False
                    else:
                        possible_moves[(self.row,col_counter)] = (self.row,col_counter)
                        searching = False
            else:
                searching = False

        col_counter = self.col
        searching = True
        while searching:
            col_counter -= 1
            if col_counter >= 0:
                if board[self.row][col_counter] == 0:
                    possible_moves[(self.row,col_counter)] = 0
                else:
                    if board[self.row][col_counter].color == self.color:
                        searching = False
                    else:
                        possible_moves[(self.row,col_counter)] = (self.row,col_counter)
                        searching = False
            else:
                searching = False

        if check_moves:
            possible_moves = self.fix_check(board_object,board,possible_moves)

        return possible_moves

class King(Piece):
    def __init__(self,row,col,color):
        super().__init__(row,col,color)
        self.has_moved = False
        self.is_king = True
        self.castle = False

    def draw(self,win):
        if self.color == BLACK:
            king_sprite = pygame.image.load(os.path.join("Sprites","king_black.ppm"))
        else:
            king_sprite = pygame.image.load(os.path.join("Sprites","king_white.ppm"))
        king_sprite.set_colorkey((255,0,0))
        king_sprite = pygame.transform.scale(king_sprite,(SQUARE_SIZE-20,SQUARE_SIZE-20))
        win.blit(king_sprite,(self.x - ((SQUARE_SIZE-20)//2),self.y - ((SQUARE_SIZE-20)//2)))

    def find_possible_moves(self,board_object,board,opposing_moves=None,check_moves=False):
        possible_moves = {}

        if self.col - 1 >= 0:
            if board[self.row][self.col - 1] == 0:
                possible_moves[(self.row,self.col-1)] = 0
            elif board[self.row][self.col - 1].color != self.color:
                possible_moves[(self.row,self.col-1)] = (self.row,self.col-1)
        if self.col + 1 <= 7:
            if board[self.row][self.col + 1] == 0:
                possible_moves[(self.row,self.col+1)] = 0
            elif board[self.row][self.col + 1].color != self.color:
                possible_moves[(self.row,self.col+1)] = (self.row,self.col+1)
        if self.row - 1 >= 0:
            if board[self.row - 1][self.col] == 0:
                possible_moves[(self.row-1,self.col)] = 0
            elif board[self.row-1][self.col].color != self.color:
                possible_moves[(self.row-1,self.col)] = (self.row-1,self.col)
        if self.row + 1 <= 7:
            if board[self.row + 1][self.col] == 0:
                possible_moves[(self.row+1,self.col)] = 0
            elif board[self.row+1][self.col].color != self.color:
                possible_moves[(self.row+1,self.col)] = (self.row+1,self.col)
        if self.row - 1 >= 0 and self.col - 1 >= 0:
            if board[self.row - 1][self.col - 1] == 0:
                possible_moves[(self.row-1,self.col-1)] = 0
            elif board[self.row-1][self.col - 1].color != self.color:
                possible_moves[(self.row-1,self.col-1)] = (self.row-1,self.col-1)
        if self.row - 1 >= 0 and self.col + 1 <= 7:
            if board[self.row - 1][self.col + 1] == 0:
                possible_moves[(self.row-1,self.col+1)] = 0
            elif board[self.row-1][self.col + 1].color != self.color:
                possible_moves[(self.row-1,self.col+1)] = (self.row-1,self.col+1)
        if self.row + 1 <= 7 and self.col + 1 <= 7:
            if board[self.row + 1][self.col + 1] == 0:
                possible_moves[(self.row+1,self.col+1)] = 0
            elif board[self.row+1][self.col+1].color != self.color:
                possible_moves[(self.row+1,self.col+1)] = (self.row+1,self.col+1)
        if self.row + 1 <= 7 and self.col - 1 >= 0:
            if board[self.row + 1][self.col - 1] == 0:
                possible_moves[(self.row+1,self.col-1)] = 0
            elif board[self.row+1][self.col-1].color != self.color:
                possible_moves[(self.row+1,self.col-1)] = (self.row+1,self.col-1)

        if not self.has_moved:
            if board[self.row][self.col + 1] == 0 and board[self.row][self.col + 2] == 0:
                try:
                    if board[self.row][self.col + 3].is_rook:
                        if not board[self.row][self.col + 3].has_moved:
                            possible_moves[(self.row,self.col+2)] = (self.row,self.col+2)
                            self.castle = True
                except:
                    pass
            if board[self.row][self.col - 1] == 0 and board[self.row][self.col - 2] == 0 and board[self.row][self.col - 3] == 0:
                try:
                    if board[self.row][self.col - 4].is_rook:
                        if not board[self.row][self.col - 4].has_moved:
                            possible_moves[(self.row,self.col-2)] = (self.row,self.col-2)
                            self.castle = True
                except:
                    pass

        if opposing_moves != None:
            for possible_move in possible_moves.copy().keys():
                if possible_move in opposing_moves:
                    del possible_moves[possible_move]

        if check_moves:
            possible_moves = self.fix_check(board_object,board,possible_moves,king_moved=True)

        return possible_moves
