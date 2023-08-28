#!/usr/bin/env python3

import argparse
from base import Puzzle


def _main(filename):
    puzzle = QuadMarksPuzzle(filename)
    puzzle.solve()


class QuadMark():
    def __init__(self, coords, values):
        self.coords = coords
        self.possible_values = values
        self.original_values = values


class QuadMarksPuzzle(Puzzle):
    """
        Twisted Sudoku puzzle that starts with no values. A set of four digits are
        shown on the intersection between some sets of squares. These digits must
        be placed in the four adjoining squares. 
    """

    def __init__(self, filename):
        self.board, self.marks = self._parse_puzzle(filename)


    def _parse_puzzle(self, filename):
        with open(filename) as f:
            data = f.readlines()
        board = self.parse_board(data[:9])
        marks = self.parse_marks(data[10:])
        return board, marks


    def parse_marks(self, data):
        """ Each row looks like this 03,04,13,14,2349 """
        marks = {}
        for line in data:
            coords = []
            for s in line.strip().split(','):
                if len(s) == 2:
                    coords.append((int(s[0]), int(s[1])))
                else:
                    values = [int(v) for v in s]
            for coord in coords:
                if coord not in marks:
                    marks[coord] = QuadMark(coords, values)
                else:
                    new_vals = []
                    for v in marks[coord].possible_values:
                        if v in values:
                            new_vals.append(v)
                    marks[coord].possible_values = new_vals
        return marks


    def get_possible_vals(self, i, j):
        possible_vals = list(range(1, 10))
        if (i, j) in self.marks:
            possible_vals = self.get_quadmark_vals(i, j)

        row_vals = self.get_row_vals(i)
        col_vals = self.get_column_vals(j)
        group_vals = self.get_group_vals(i, j)
        non_quadmark_vals = self.get_non_quadmark_vals(i, j)

        for val in row_vals + col_vals + group_vals + non_quadmark_vals:
            if val in possible_vals:
                possible_vals.remove(val)
        return possible_vals


    def get_quadmark_vals(self, row, col):
        vals = []
        if (row, col) in self.marks:
            vals += self.marks[(row, col)].possible_values
            for (i, j) in self.marks[(row, col)].coords:
                if (i, j) != (row, col) and self.board[i][j] != 0:
                    if self.board[i][j] in vals:
                        vals.remove(self.board[i][j])
        return vals


    def get_non_quadmark_vals(self, row, col):
        """ if a quad exists in this group but this cell is not affected, return the non quadmark values """
        vals = []
        group_center = ((row // 3 * 3) + 1, (col // 3 * 3) + 1)
        if group_center in self.marks:
            if (row, col) not in self.marks[group_center].coords:
                vals += self.marks[group_center].original_values
        return vals


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Solve a Twisted Sudoku Puzzle.')
    parser.add_argument('filename')
    args = parser.parse_args()
    _main(args.filename)

