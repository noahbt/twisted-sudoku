#!/usr/bin/env python3

import argparse
from base import Puzzle


def _main(filename):
    puzzle = JigsawPuzzle(filename)
    puzzle.solve()


class JigsawPuzzle(Puzzle):
    """
        Twisted Sudoku puzzle where groups are no longer 3x3 and are 
        defined like jigsaw pieces. Same group principles exist.
    """

    def __init__(self, filename):
        self.board, self.groups = self._parse_puzzle(filename)


    def _parse_puzzle(self, filename):
        with open(filename) as f:
            data = f.readlines()
        board = self.parse_board(data[:9])
        groups = self.parse_groups(data[10:])
        return board, groups


    def parse_groups(self, data):
        groups = []
        for d in data:
            row = []
            for p in d.strip().split(','):
                row.append((int(p[0]), int(p[1])))
            groups.append(row)
        return groups


    def get_possible_vals(self, i, j):
        possible_vals = list(range(1, 10))
        row_vals = self.get_row_vals(i)
        col_vals = self.get_column_vals(j)
        group_vals = self.get_group_vals(i, j)

        for val in row_vals + col_vals + group_vals:
            if val in possible_vals:
                possible_vals.remove(val)
        return possible_vals


    def get_group_vals(self, row, col):
        """ 
            Returns all non-zero values in the jigsaw group that row,col is in
        """
        group_vals = []
        for group in self.groups:
            if (row, col) in group:
                for i,j in group:
                    group_vals.append(self.board[i][j])
        return group_vals


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Solve a Twisted Sudoku Puzzle.')
    parser.add_argument('filename')
    args = parser.parse_args()
    _main(args.filename)

