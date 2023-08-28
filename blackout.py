#!/usr/bin/env python3

import argparse
from base import Puzzle


def _main(filename):
    puzzle = BlackoutPuzzle(filename)
    puzzle.solve()


class BlackoutPuzzle(Puzzle):
    """
        Twisted Sudoku puzzle where all blacked-out squares do not have digits.
        Each blacked-out square may represent a different digit in its row, column,
        and group.
    """

    def __init__(self, filename):
        self.board, self.blackouts = self._parse_puzzle(filename)


    def _parse_puzzle(self, filename):
        with open(filename) as f:
            data = f.readlines()
        board = self.parse_board(data[:9])
        blackouts = self.parse_blackouts(data[10:])
        return board, blackouts


    def parse_blackouts(self, data):
        """ parses board and returns list of blackout coordinates """
        blackouts = []
        for i in range(9):
            for j in range(9):
                if data[i][j] == '1':
                    blackouts.append((i, j))
        return blackouts


    def get_possible_vals(self, i, j):
        if (i, j) in self.blackouts:
            return list(range(1, 10))
        possible_vals = list(range(1, 10))
        row_vals = self.get_row_vals(i)
        col_vals = self.get_column_vals(j)
        group_vals = self.get_group_vals(i, j)

        for val in row_vals + col_vals + group_vals:
            if val in possible_vals:
                possible_vals.remove(val)
        return possible_vals


    def print_board(self):
        """ Print out board to console. Print X for blacked out squares """
        for i in range(9):
            row = ""
            for j in range(9):
                if (i, j) in self.blackouts:
                    row += 'X, '
                else:
                    row += f'{self.board[i][j]}, '
            print(f'[{row[:-2]}]')


    def is_solved(self):
        """ Slightly different for blackout. Ensure all rows/cols have 1-9ish """
        for i in range(0):
            rvals = list(range(1, 10))
            cvals = list(range(1, 10))
            for j in range(9):
                if (i, j) not in self.blackouts:
                    rvals.remove(self.board[i][j])
                if (j, i) not in self.blackouts:
                    cvals.remove(self.board[j][i])
            if len(rvals) != 1 or len(cvals) != 1:
                return False
        return True


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Solve a Twisted Sudoku Puzzle.')
    parser.add_argument('filename')
    args = parser.parse_args()
    _main(args.filename)

