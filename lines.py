#!/usr/bin/python3

import argparse
from base import Puzzle


def _main(filename):
    puzzle = LinePuzzle(filename)
    puzzle.solve()


class LinePuzzle(Puzzle):
    """
        Twisted Sudoku puzzle where lines indicate numbers that must be
        increasing or decreasing along the line, indicated by a direction.
    """

    def __init__(self, filename):
        self.board, self.lines = self._parse_puzzle(filename)


    def _parse_puzzle(self, filename):
        with open(filename) as f:
            data = f.readlines()
        board = self.parse_board(data[:9])
        lines = self.parse_lines(data[10:])
        return board, lines
        

    def parse_lines(self, data):
        lines = []
        for d in data:
            row = []
            for p in d.split(','):
                row.append((int(p[0]), int(p[1])))
            lines.append(row)
        return lines


    def get_possible_vals(self, i, j):
        # Start with 1..9, then eliminate row, col and group values
        possible_vals = list(range(1, 10))
        row_vals = self.get_row_vals(i)
        col_vals = self.get_column_vals(j)
        group_vals = self.get_group_vals(i, j)
        line_vals = self.get_line_vals(i, j)

        for val in row_vals + col_vals + group_vals + line_vals:
            if val in possible_vals:
                possible_vals.remove(val)
        return possible_vals


    def get_line_vals(self, row, col):
        smallest = 1
        biggest = 9
        for line in self.lines:
            if (row, col) in line:
                index = line.index((row, col))

                smallest = index + 1
                biggest = 9 - (len(line) - (index + 1))
                
                for i, (r, c) in enumerate(line):
                    val = self.board[r][c]
                    if val == 0:
                        # TODO- use possible vals
                        continue
                    diff = i - index
                    if diff < 0:
                        if smallest < val - diff:
                            smallest = val - diff
                    elif diff > 0:
                        if biggest > val - diff:
                            biggest = val - diff
        return list(range(1, smallest)) + list(range(biggest + 1, 10))


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Solve a Twisted Sudoku Puzzle.')
    parser.add_argument('filename')
    args = parser.parse_args()
    _main(args.filename)

