#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
@version: ??
@author: Ye Sheng
@license: Apache Licence
@contact: sym1all@hotmail.com
@file: conf
@time: 9/21/16 10:58 AM
@project: back2back
"""
import itertools

from newmodle import *

PINK1 = Piece(1, [[2, 2, 0], [1, 0, 0], [0, 0, 0]])
PINK2 = Piece(2, [[2, 2, 0], [1, 0, 0], [0, 0, 0]])
LIGHT_BLUE = Piece(3, [[2, 0, 0], [1, 0, 0], [2, 0, 0]])
BLUE = Piece(4, [[0, 2, 0], [0, 1, 0], [1, 2, 0]])
NAVY = Piece(5, [[0, 2, 0], [1, 2, 0], [0, 0, 0]])
GREEN = Piece(6, [[0, 0, 2], [2, 1, 1], [0, 0, 0]])
OLIVE = Piece(7, [[0, 2, 0], [2, 1, 0], [0, 0, 0]])
PURPLE = Piece(8, [[1, 0, 0], [1, 2, 0], [0, 2, 0]])
YELLOW = Piece(9, [[0, 1, 0], [1, 2, 2], [0, 0, 0]])
ORANGE = Piece(10, [[0, 0, 1], [2, 1, 2], [0, 0, 0]])
RED = Piece(11, [[1, 2, 2], [0, 0, 0], [0, 0, 0]])

PIECES = [LIGHT_BLUE, GREEN, OLIVE, PINK1, PINK2, NAVY, BLUE, PURPLE, YELLOW, RED, ORANGE]

BOARD_MAP = {}

fin = open('../file/boards.txt', 'r')
lines = fin.readlines()

while len(lines) > 10:
    board_map = lines[:13]
    lines = lines[13:]
    index = int(board_map[0][:-1])
    top = [map(int, row[:-1].split(',')) for row in board_map[1:6]]
    bot = [map(int, row[:-1].split(',')) for row in board_map[7:12]]
    colors = set(itertools.chain.from_iterable(top))
    not_on = [piece for piece in PIECES if piece.name not in colors]
    board = Board(top=top, bot=bot, not_on=not_on)
    board.update_half_filled()
    BOARD_MAP[index] = board
