#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
@version: ??
@author: Ye Sheng
@license: Apache Licence
@contact: sym1all@hotmail.com
@file: modle
@time: 9/3/16 10:15 AM
@project: back2back
"""
from graphics import *

# some constants
SIDE_ORIGINAL = 1
SIDE_FLIPPED = -1

BOARD_WIDTH = 6
BOARD_HEIGHT = 5


"""
SOME THOUGHTS:
both board and pieces are represented by 2d-arrays. Since no pieces with dimension greater than 3,
pieces are all represented by 3*3 2d-array.pieces are allways 'facing down' but the board can be flipped. Pieces can rotate.

For future implementation of the AI, I may want to optimize some of the code since some of the action is relatively expensive.
For example, I will never want to update th GUI when I brute force through all the possible solutions.

Another thing here need to be worked on is the GUI display of the pieces is not really clear. Need to find another better way to do this.

The overall structure of the code is kind of crude.I may want to add functions to read the configuration of the boardfrom txt files to generate the preset of the board.

"""

class Board:
    """
    board class, support basic operation
    """

    def __init__(self):
        # using 2 2d array to represent the board
        self.layer_top = [[' ' for col in range(BOARD_WIDTH)] for row in range(BOARD_HEIGHT)]
        self.layer_bot = [row[:] for row in self.layer_top]
        # recording current facing
        self.side = SIDE_ORIGINAL
        self.pieces = []

    def flip_board(self):
        # flip the board vertically, change arrays correspodingly
        self.layer_top = [row[::-1] for row in self.layer_top]
        self.layer_bot = [row[::-1] for row in self.layer_bot]
        self.layer_bot, self.layer_top = self.layer_top, self.layer_bot
        self.side = self.side * -1

    def clear(self):
        # reinitialize the board
        self.layer_top = [[' ' for col in range(BOARD_WIDTH)] for row in range(BOARD_HEIGHT)]
        self.layer_bot = [row[:] for row in self.layer_top]
        self.side = SIDE_ORIGINAL
        self.pieces = []

    def is_full(self):
        # check whether the board is full
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if self.layer_top[row][col] == ' ' and self.layer_bot[row][col] == ' ':
                    return False
        return True

    def __str__(self):
        # console print for test
        s = ''
        for row in self.layer_top:
            s += row.__str__()
            s += '\n'
        s += '\n'
        for row in self.layer_bot:
            s += row.__str__()
            s += '\n'
        return s

    def add_piece_at(self, piece, row, col):
        # add piece at specified location, will raise exception if locatoin is invalid
        # the piece is locate by the top left cell of the piece layout
        for r in range(3):
            for c in range(3):
                depth = piece.layout[r][c]
                abs_row = row + r
                abs_col = col + c
                if depth != 0:
                    if (not self._is_in_range(abs_row, abs_col)) or self.layer_top[abs_row][abs_col] != ' ':
                        raise Exception()
                    self.layer_top[abs_row][abs_col] = piece.s
                    if depth == 2:
                        if self.layer_bot[abs_row][abs_col] != ' ':
                            raise Exception()
                        self.layer_bot[abs_row][abs_col] = piece.s

    def _is_in_range(self, row, col):
        # test for valid index
        return (BOARD_HEIGHT - 1 >= row >= 0) and (BOARD_WIDTH - 1 >= col >= 0)

    def remove_piece(self, piece=None, s=None):
        # remove piece from board
        if piece is not None:
            target = piece.s
        else:
            target = s
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                if self.layer_top[row][col] == target:
                    self.layer_top[row][col] = ' '
                if self.layer_bot[row][col] == target:
                    self.layer_bot[row][col] = ' '


class Piece:
    def __init__(self, name, layout):
        self.layout = layout
        self.s = name

    def rotate_90_degree(self):
        # rotate the 2d array 90 degree clockwisely
        self.layout = zip(*self.layout[::-1])

    def __str__(self):
        return '\n'.join([row.__str__() for row in self.layout])


# some information for the GUI layout
PIECE_DICT = {'p1': ['pink', 7, 0], 'p2': ['pink', 10, 0], 'lb': ['black', 7, 3], 'b': ['blue', 10, 3],
              'n': ['brown', 0, 6], 'g': ['green', 3, 6], 'o': ['grey', 6, 6], 'p': ['purple', 9, 6],
              'y': ['yellow', 0, 9], 'ora': ['orange', 3, 9], 'r': ['red', 6, 9]}

# initializing all the pieces
p1 = Piece('p1', [[2, 2, 0], [1, 0, 0], [0, 0, 0]])
p2 = Piece('p2', [[2, 2, 0], [1, 0, 0], [0, 0, 0]])
lb = Piece('lb', [[2, 0, 0], [1, 0, 0], [2, 0, 0]])
b = Piece('b', [[0, 2, 0], [0, 1, 0], [1, 2, 0]])
n = Piece('n', [[0, 2, 0], [1, 2, 0], [0, 0, 0]])
g = Piece('g', [[0, 0, 2], [2, 1, 1], [0, 0, 0]])
o = Piece('o', [[0, 2, 0], [2, 1, 0], [0, 0, 0]])
p = Piece('p', [[1, 0, 0], [1, 2, 0], [0, 2, 0]])
y = Piece('y', [[0, 1, 0], [1, 2, 2], [0, 0, 0]])
ora = Piece('ora', [[0, 0, 1], [2, 1, 2], [0, 0, 0]])
r = Piece('r', [[1, 2, 2], [0, 0, 0], [0, 0, 0]])

PIECES = [p1, p2, lb, b, n, g, o, p, y, ora, r]


class GUI:
    # GUI class, bassically using grid of circles to both represent the board and pieces
    # piece filled in the top layer represented by two circles, bottom layer ones represented by one circle
    def __init__(self, board, pieces):
        self.board = board
        self.pieces = pieces
        self.win = GraphWin(title='back2back', width=800, height=800)
        self.win.setCoords(0, 13, 13, 0)
        # circles for the board
        self.board_circles = [[None for col in range(BOARD_WIDTH)] for row in range(BOARD_HEIGHT)]
        self.board_circles_top = [[[] for col in range(BOARD_WIDTH)] for row in range(BOARD_HEIGHT)]
        # grid circles to display all the free pieces
        self.grid_circles = [[None for col in range(BOARD_WIDTH + 7)] for row in range(BOARD_HEIGHT + 8)]
        for row in range(BOARD_HEIGHT + 8):
            for col in range(BOARD_WIDTH + 7):
                circle = Circle(Point(col + 0.5, row + 0.5), 0.4)
                circle.setFill('white')
                circle.setOutline('white')
                circle.draw(self.win)
                self.grid_circles[row][col] = circle
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                circle = Circle(Point(col + 0.5, row + 0.5), 0.4)
                circle.draw(self.win)
                self.board_circles[row][col] = circle

        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                circle = Circle(Point(col + 0.5, row + 0.5), 0.4)
                self.board_circles_top[row][col].append(circle)
                circle = Circle(Point(col + 0.5, row + 0.5), 0.35)
                self.board_circles_top[row][col].append(circle)

    def display_pieces(self):
        for p in PIECES:
            if p in self.pieces:
                color = PIECE_DICT[p.s][0]
                x = PIECE_DICT[p.s][1]
                y = PIECE_DICT[p.s][2]
                for row in range(3):
                    for col in range(3):
                        grid_circle = self.grid_circles[y + row][x + col]
                        if p.layout[row][col] == 0:
                            grid_circle.setFill('white')
                        else:
                            grid_circle.setFill(color)
            else:
                x = PIECE_DICT[p.s][1]
                y = PIECE_DICT[p.s][2]
                for row in range(3):
                    for col in range(3):
                        grid_circle = self.grid_circles[y + row][x + col]
                        grid_circle.setFill('white')

    def update(self):
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                bot_fill = self.board.layer_bot[row][col]
                circle = self.board_circles[row][col]
                if bot_fill == ' ':
                    circle.setFill('white')
                else:
                    circle.setFill(PIECE_DICT[bot_fill][0])
                top_fill = self.board.layer_top[row][col]
                circles = self.board_circles_top[row][col]
                if top_fill == ' ':
                    circles[0].undraw()
                    circles[1].undraw()
                else:
                    circles[0].setFill(PIECE_DICT[top_fill][0])
                    circles[1].setFill(PIECE_DICT[top_fill][0])
                    try:
                        circles[0].draw(self.win)
                        circles[1].draw(self.win)
                    except:
                        None
        self.display_pieces()


"""
here are severall functions that player are going to use through the console
"""

def add_piece_at(piece, x, y):
    if piece in gui.pieces:
        try:
            board.add_piece_at(piece, y - 1, x - 1)
            gui.pieces.remove(piece)
            gui.update()
        except:
            print 'INVALID POSITION!!!!'
    else:
        print 'ALREADY IN BOARD!!!!'


def remove_pice(piece):
    if piece in gui.pieces:
        gui.pieces.append(piece)
        board.remove_piece(piece)
        gui.update()
    else:
        print 'NOT IN BOARD YET!!!!!!!'


def clear_board():
    board.clear()
    gui.update()
    gui.pieces = [p1, p2, lb, b, n, g, o, p, y, ora, r]
    gui.update()


def rotate_piece(piece):
    if piece in gui.pieces:
        piece.rotate_90_degree()
        gui.update()


def flip_board():
    board.flip_board()
    gui.update()


def print_board():
    print board

if __name__ == '__main__':
    board = Board()
    gui = GUI(board, pieces=PIECES[:])
    gui.update()

    while True:
        command = raw_input('ENTER A VALID COMMAND TO CONTINUE:')
        try:
            exec command
            if gui.board.is_full():
                print 'Well Done!!!'
                break
        except:
            print 'INVALID COMMAND!!!!'
    gui.win.getMouse()
