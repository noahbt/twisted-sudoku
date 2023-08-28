#!/usr/bin/python
import sys


class Puzzle:
    def __init__(self, board, groups):
        self.board = board
        self.groups = groups


def _main():
    print('-'*120)
    if len(sys.argv) < 2:
        print('Please specify a filename!\t./helper.py <filename.csv> [max_vals]\n')
        return
    if len(sys.argv) == 3:
        max_vals = int(sys.argv[2])
    else:
        max_vals = 2

    board, groups = parse_puzzle(sys.argv[1], False)
    puzzle = Puzzle(board, groups)

    print_board(puzzle)
    print

    vals = find_vals(puzzle, max_vals)
    for k,v in vals.items():
        print(k, v)

    print


def print_board(puzzle):
    for row in puzzle.board:
        print(row)


def parse_puzzle(filename, has_groups):
    with open(filename) as f:
        data = f.readlines()
    board = []
    for i in range(9):
        row = []
        for j in range(9):
            c = data[i][j]
            row.append(int(c))
        board.append(row)
    if not has_groups:
        return board, None
    groups = []
    for i in range(10, 19):
        row = []
        for p in data[i].split(','):
            row.append((int(p[0]), int(p[1])))
        groups.append(row)
    return board, groups


def find_vals(puzzle, max_possible):
    ret_vals = {}
    for i in range(9):
        for j in range(9):
            if puzzle.board[i][j] == 0:
                possible_vals = get_possible_vals(puzzle, i, j)
                if len(possible_vals) <= max_possible:
                    ret_vals[(i, j)] = possible_vals
    return ret_vals


def get_possible_vals(puzzle, i, j):
    """ Start with 1..9, then eliminate row, col and group values """
    possible_vals = range(1, 10)
    row_vals = get_row_vals(puzzle.board, i)
    col_vals = get_column_vals(puzzle.board, j)
    group_vals = get_group_vals(puzzle, i, j)

    for val in row_vals + col_vals + group_vals:
        if val in possible_vals:
            possible_vals.remove(val)

    return possible_vals


def get_row_vals(board, row):
    return board[row]


def get_column_vals(board, col):
    return [row[col] for row in board]


def get_group_vals(puzzle, row, col):
    group_vals = []
    if not puzzle.groups:
        g_row = row / 3 * 3
        g_col = col / 3 * 3
        for i in range(9):
            group_vals.append(puzzle.board[g_row + i / 3][g_col + i % 3])
    else:
        for group in puzzle.groups:
            if (row, col) in group:
                for i,j in group:
                    group_vals.append(puzzle.board[i][j])
    return group_vals


if __name__=='__main__':
    _main()

