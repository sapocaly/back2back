#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
@version: ??
@author: Ye Sheng
@license: Apache Licence
@contact: sym1all@hotmail.com
@file: solver
@time: 9/21/16 12:44 PM
@project: back2back
"""

import random

class Solver:
    def __init__(self, board):
        self.board = board
        self.solution = None
        self.state_visited_count = 0
        self.stack = [board]
        self.seen = set()
        self.state_count = 0

    def solve(self):
        random.shuffle(self.board.not_on)
        # empty means no solution
        while self.stack:
            # DFS,LILO
            current_state = self.stack.pop()
            self.state_visited_count += 1
            # all pieces on, solution
            if not current_state.not_on:
                return current_state
            states_to_add = []
            not_on = current_state.not_on
            random.shuffle(not_on)
            if not (current_state.partial_filled_top or current_state.partial_filled_bot):
                new_states = []
                empty_spots = []
                for row in range(5):
                    for col in range(6):
                        # empty spot
                        if current_state.board_bot[row][col] == 0:
                            empty_spots.append((row, col))
                for spot in empty_spots:
                    for piece in not_on:
                        for direction in range(8):
                            coords = piece.half_filled_coords[direction][0]
                            new_state = current_state.clone()
                            success = new_state.add_piece_at(coords[0], coords[1], spot[0], spot[1], piece, direction)
                            if success:
                                new_states.append(new_state)
                states_to_add += new_states
            else:
                to_continue = True
                for half_filled in current_state.partial_filled_bot:
                    new_states = []
                    for piece in not_on:
                        # top side down directions
                        for direction in range(4):
                            for coords in piece.half_filled_coords[direction]:
                                new_state = current_state.clone()
                                success = new_state.add_piece_at(coords[0], coords[1], half_filled[0], half_filled[1],
                                                                 piece,
                                                                 direction)
                                if success:
                                    new_states.append(new_state)

                    if not new_states:
                        # any spot that can not be filled means current state will not give a solution
                        to_continue = False
                        # not adding any statesto the stack
                        states_to_add = []
                        break
                    else:
                        states_to_add += new_states
                # not going to continue if exist spot can not be filled
                if to_continue:
                    for half_filled in current_state.partial_filled_top:
                        new_states = []
                        for piece in not_on:
                            for direction in range(4, 8):
                                for coords in piece.half_filled_coords[direction]:
                                    new_state = current_state.clone()
                                    success = new_state.add_piece_at(coords[0], coords[1], half_filled[0],
                                                                     half_filled[1],
                                                                     piece,
                                                                     direction)
                                    if success:
                                        new_states.append(new_state)
                        if not new_state:
                            states_to_add = []
                            break
                        else:
                            states_to_add += new_states
            for new_state in states_to_add:
                self.state_count += 1
                hash_string = new_state.hash_string()
                if not hash_string in self.seen:
                    self.stack.append(new_state)
                    self.seen.add(hash_string)


