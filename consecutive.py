#!/usr/bin/python3

import argparse
from base import Puzzle


def _main(filename):
    puzzle = ConsecutivePuzzle(filename)
    puzzle.solve()


class ConsecutivePuzzle(Puzzle):
    """
        Twisted Sudoku puzzle where bars between pairs of squares show that all
        the adjacent square values must have a difference of 1, such as 4 and 5
    """

    def __init__(self, filename):
        self.board, self.pairs = self._parse_puzzle(filename)


    def _parse_puzzle(self, filename):
        with open(filename) as f:
            data = f.readlines()
        board = self.parse_board(data[:9])
        pairs = self.parse_pairs(data[10:])
        return board, pairs
        

    def parse_pairs(self, data):
        pairs = {}
        for d in data:
            p1, p2 = d.split(',')
            pair1 = (int(p1[0]), int(p1[1]))
            pair2 = (int(p2[0]), int(p2[1]))

            if pair1 not in pairs:
                pairs[pair1] = []
            pairs[pair1].append(pair2)

            if pair2 not in pairs:
                pairs[pair2] = []
            pairs[pair2].append(pair1)
        return pairs


    def get_possible_vals(self, i, j):
        # Start with 1..9, then eliminate row, col and group values
        possible_vals = list(range(1, 10))

        if (i, j) in self.pairs:
            possible_vals = self.get_pair_vals(i, j)

        row_vals = self.get_row_vals(i)
        col_vals = self.get_column_vals(j)
        group_vals = self.get_group_vals(i, j)

        for val in row_vals + col_vals + group_vals:
            if val in possible_vals:
                possible_vals.remove(val)
        return possible_vals


    def get_pair_vals(self, i, j):
        """ Check all adjacent squares for pairness and values """
        vals = []
        pvals = []
        possible_pairs = self.pairs[(i, j)]
        for coord in possible_pairs:
            val = self.board[coord[0]][coord[1]]
            if val != 0:
                if val == 1:
                    return [2]
                elif val == 9:
                    return [8]
                pvals.append(val)
        if len(pvals) > 0:
            for pval in pvals:
                if len(vals) == 0:
                    vals.append(pval - 1)
                    vals.append(pval + 1)
                else:
                    for val in vals:
                        if val !=  pval - 1 and val != pval + 1:
                            vals.remove(val)
            return vals
        return list(range(1, 10))



if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Solve a Twisted Sudoku Puzzle.')
    parser.add_argument('filename')
    args = parser.parse_args()
    _main(args.filename)

