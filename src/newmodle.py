#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
@version: ??
@author: Ye Sheng
@license: Apache Licence
@contact: sym1all@hotmail.com
@file: newmodle
@time: 9/17/16 2:06 PM
@project: back2back
"""
import copy

def empty_copy(obj):
    class Empty(obj.__class__):
        def __init__(self):
            pass

    newcopy = Empty()
    newcopy.__class__ = obj.__class__
    return newcopy


class Board:
    def __init__(self, top=[[0 for col in range(6)] for row in range(5)],
                 bot=[[0 for col in range(6)] for row in range(5)],
                 partial_filled_top=[],
                 partial_filled_bot=[],
                 not_on=[]):
        self.board_top = top
        self.board_bot = bot
        self.partial_filled_top = partial_filled_top
        self.partial_filled_bot = partial_filled_bot
        self.not_on = not_on

    def hash_string(self):
        return str(self.board_top) + str(self.board_bot)

    def clone(self):
        board_top = [row[:] for row in self.board_top]
        board_bot = [row[:] for row in self.board_bot]
        return Board(top=board_top, bot=board_bot,
                     partial_filled_top=self.partial_filled_top[:],
                     partial_filled_bot=self.partial_filled_bot[:], not_on=self.not_on[:])

    def update_half_filled(self):
        self.partial_filled_bot = []
        self.partial_filled_top = []
        for row in range(5):
            for col in range(6):
                if self.board_bot[row][col] + self.board_top[row][col] != 0:
                    if self.board_bot[row][col] == 0:
                        self.partial_filled_top.append((row, col))
                    elif self.board_top[row][col] == 0:
                        self.partial_filled_bot.append((row, col))

    def _is_in_range(self, row, col):
        # test for valid index
        return (5 - 1 >= row >= 0) and (6 - 1 >= col >= 0)

    def add_piece_at(self, y, x, row, col, piece, direction):
        layout = piece.layouts[direction]
        for r in range(3):
            for c in range(3):
                depth = layout[r][c]
                abs_row = row + r - y
                abs_col = col + c - x
                if depth != 0:
                    if direction < 4:
                        if (not self._is_in_range(abs_row, abs_col)) or (self.board_top[abs_row][abs_col] != 0):
                            return False
                        if (depth == 2) and (self.board_bot[abs_row][abs_col] != 0):
                            return False
                    else:
                        if (not self._is_in_range(abs_row, abs_col)) or (self.board_bot[abs_row][abs_col] != 0):
                            return False
                        if (depth == 2) and (self.board_top[abs_row][abs_col] != 0):
                            return False
        for r in range(3):
            for c in range(3):
                depth = layout[r][c]
                abs_row = row + r - y
                abs_col = col + c - x
                if depth != 0:
                    if direction < 4:
                        if depth == 1:
                            if self.board_bot[abs_row][abs_col] != 0:
                                self.partial_filled_bot.remove((abs_row, abs_col))
                            else:
                                self.partial_filled_top.append((abs_row, abs_col))
                            self.board_top[abs_row][abs_col] = piece.name
                        else:
                            self.board_top[abs_row][abs_col] = piece.name
                            self.board_bot[abs_row][abs_col] = piece.name
                    else:
                        if depth == 1:
                            if self.board_top[abs_row][abs_col] != 0:
                                self.partial_filled_top.remove((abs_row, abs_col))
                            else:
                                self.partial_filled_bot.append((abs_row, abs_col))
                            self.board_bot[abs_row][abs_col] = piece.name
                        else:
                            self.board_bot[abs_row][abs_col] = piece.name
                            self.board_top[abs_row][abs_col] = piece.name
        self.not_on.remove(piece)
        return True

    def __str__(self):
        s = ''
        for row in self.board_top:
            s += row.__str__()
            s += '\n'
        s += '\n'
        for row in self.board_bot:
            s += row.__str__()
            s += '\n'
        return s


class Piece:
    def __init__(self, name, layout):
        self.layouts = [layout]
        self.half_filled_coords = []
        for i in range(3):
            self.layouts.append(Piece._rotate_90_degree_layout(self.layouts[i]))
        for i in range(4):
            self.layouts.append(Piece._flip(self.layouts[i]))
        for layout in self.layouts:
            half_filled = []
            for row in range(3):
                for col in range(3):
                    if layout[row][col] == 1:
                        half_filled.append((row, col))
            self.half_filled_coords.append(half_filled)
        self.name = name

    @staticmethod
    def _rotate_90_degree_layout(layout):
        return zip(*layout[::-1])

    @staticmethod
    def _flip(layout):
        return [row[::-1] for row in layout]

    def __str__(self):
        return '\n'.join([row.__str__() for row in self.layouts[0]])
