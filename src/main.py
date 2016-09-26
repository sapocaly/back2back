#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
@version: ??
@author: Ye Sheng
@license: Apache Licence
@contact: sym1all@hotmail.com
@file: main
@time: 9/22/16 4:47 PM
@project: back2back
"""

import configure
import solver
import time
import gui



def solve_board(index):
    board = configure.BOARD_MAP[index]
    s = solver.Solver(board)
    time_start = time.time()
    solution = s.solve()
    time_finished = time.time()
    if solution:
        print 'Solution:'
        print solution
        print '\nStates Visited:',s.state_visited_count
        print '\nTotal Seened:',s.state_count
        print '\nUnique Seened:', len(s.seen)
        print '\nTime Cost:',time_finished - time_start
        g = gui.GUI(solution)
        g.update()
        g.win.getMouse()


def test():
    for board in configure.BOARD_MAP.values():
        missing_count = len(board.not_on)
        print '-----------------'
        print missing_count
        total = 1 if missing_count == 10 else 8
        counts = []
        for i in range(total):
            s = solver.Solver(board)
            s.solve()
            print s.state_visited_count
            counts.append(s.state_visited_count)
        print 'avg:',sum(counts)/len(counts)


if __name__ == '__main__':
    #test()
    solve_board(37)


