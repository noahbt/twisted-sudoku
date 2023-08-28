#!/usr/bin/env python3

import argparse
from base import Puzzle


def _main(filename):
    puzzle = BasicPuzzle(filename)
    puzzle.solve()


class BasicPuzzle(Puzzle):
    """ Just your basic Sudoku puzzle without a twist """

    def _parse_puzzle(self, filename):
        with open(filename) as f:
            data = f.readlines()
        board = self.parse_board(data[:9])
        return board


    def get_possible_vals(self, i, j):
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

