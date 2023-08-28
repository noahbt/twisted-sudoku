#!/usr/bin/env python3

import argparse
from base import Puzzle


def _main(filename):
    puzzle = OddEvenPuzzle(filename)
    puzzle.solve()


class OddEvenPuzzle(Puzzle):
    """
        Twisted Sudoku puzzle where all shaded squares must contain even digits.
    """

    def __init__(self, filename):
        self.board, self.evens = self._parse_puzzle(filename)


    def _parse_puzzle(self, filename):
        with open(filename) as f:
            data = f.readlines()
        board = self.parse_board(data[:9])
        evens = self.parse_evens(data[10:])
        return board, evens


    def parse_evens(self, data):
        """ parses board and returns list of even coordinates """
        evens = []
        for i in range(9):
            for j in range(9):
                if data[i][j] == '1':
                    evens.append((i, j))
        return evens


    def get_possible_vals(self, i, j):
        if (i, j) in self.evens:
            possible_vals = list(range(2, 10, 2))
        else:
            possible_vals = list(range(1, 10))
        row_vals = self.get_row_vals(i)
        col_vals = self.get_column_vals(j)
        group_vals = self.get_group_vals(i, j)

        for val in row_vals + col_vals + group_vals:
            if val in possible_vals:
                possible_vals.remove(val)
        return possible_vals


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Solve a Twisted Sudoku Puzzle.')
    parser.add_argument('filename')
    args = parser.parse_args()
    _main(args.filename)

