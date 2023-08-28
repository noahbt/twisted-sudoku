#!/usr/bin/env python3

import argparse
import sys
import time
from abc import ABC, abstractmethod


class Puzzle(ABC):

    def __init__(self, filename):
        self.board = self._parse_puzzle(filename)


    def solve(self):
        print('-'*120)

        self.print_board()
        print

        start_time = time.time()
        self.solve_puzzle()
        elapsed = time.time() - start_time
        print('Elapsed time: {:.2f}s'.format(elapsed))

        if self.is_solved():
            print('Solution: ')
            self.print_board()
        else:
            print('Could not solve')
        print


    @abstractmethod
    def _parse_puzzle(self, filename):
        """ Read in filename and parse board plus any other data, return Puzzle """
        pass


    @abstractmethod
    def get_possible_vals(self, i, j):
        """ return a list of possible values for the cell at i, j """
        pass


    def solve_puzzle(self):
        """
            Recursively attempt to solve the puzzle cell by cell.
            At each empty cell, get possible values and try each one, then continue
            to the next empty cell and repeat.
            If you have exhausted all possible values for a cell, return False
            and try the next value at the previous empty location
        """
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    possible_vals = self.get_possible_vals(i, j)
                    for val in possible_vals:
                        self.board[i][j] = val
                        if self.solve_puzzle():
                            return True
                        self.board[i][j] = 0
                    return False
        return True


    def parse_board(self, data):
        """ Parse 9 lines of 9 characters into a 9x9 matrix """
        board = []
        for d in data:
            row = []
            for j in range(9):
                row.append(int(d[j]))
            board.append(row)
        return board


    def print_board(self):
        """ Print out board to console """
        for i in range(9):
            row = ""
            for j in range(9):
                val = self.board[i][j]
                if val == 0:
                    row += '-, '
                else:
                    row += f'{val}, '
            print(f'[{row[:-2]}]')


    def is_solved(self):
        """ Ensure each row has numbers 1..9 """
        col_counts = [0] * 9
        row_counts = [0] * 9
        for i in range(9):
            for j in range(9):
                cval = self.board[j][i]
                if cval > 0:
                    col_counts[cval-1] += 1
                rval = self.board[i][j]
                if rval > 0:
                    row_counts[rval-1] += 1
        return all(c == 9 for c in col_counts) and all(c == 9 for c in row_counts)


    def get_row_vals(self, row):
        """ Returns all non-zero values in the given row """
        return [val for val in self.board[row] if val != 0]


    def get_column_vals(self, col):
        """ Returns all non-zero values in the given column """
        return [row[col] for row in self.board if row[col] != 0]


    def get_group_vals(self, row, col):
        """ 
            Returns all non-zero values in the given 3x3 group
            Should be overridden in puzzles like jigsaw/wraparound
        """
        group_vals = []
        g_row = row // 3 * 3
        g_col = col // 3 * 3
        for i in range(9):
            group_vals.append(self.board[g_row + i // 3][g_col + i % 3])
        return [g for g in group_vals if g != 0]

