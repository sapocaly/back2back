#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
@version: ??
@author: Ye Sheng
@license: Apache Licence
@contact: sym1all@hotmail.com
@file: gui
@time: 9/22/16 6:23 PM
@project: back2back
"""

from graphics import *


color_dict = {0:'white',1: color_rgb(197,110,153), 2: color_rgb(197,110,153), 3: color_rgb(104,168,211), 4: color_rgb(69,122,175),
              5: color_rgb(59,72,129), 6: color_rgb(126,165,81), 7: color_rgb(60,96,95), 8: color_rgb(93,63,121),
              9: color_rgb(211,187,86), 10: color_rgb(211,132,83), 11: color_rgb(193,73,78)}


class GUI:
    def __init__(self,board):
        self.board = board
        self.win = GraphWin(title='Back2BackSolver',width=600,height=500)
        self.win.setCoords(0,5,6,0)
        self.circles = []
        for row in range(5):
            self.circles.append([])
            for col in range(6):
                circle = Circle(Point(0.5 + col, 0.5 + row),0.4)
                circle.setOutline('white')
                circle.draw(self.win)
                self.circles[row].append(circle)

    def update(self):
        for row in range(5):
            for col in range(6):
                spot = self.board.board_top[row][col]
                color = color_dict[spot]
                self.circles[row][col].setFill(color)





