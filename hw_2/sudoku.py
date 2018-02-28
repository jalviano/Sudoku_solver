# sudoku.py

from sudoku_io import SudokuIO
from utils import CSP
from backtracking import (recursive_backtracking_search, instrumented_recursive_backtracking, backtracking_search,
                          first_unassigned_variable, mrv, no_inference, mac, find_intersections)


def equal_constraint(A, a, B, b):
    return a != b


def solve(variables, domains, neighbors, assignment, heuristic, with_inferences, instrumented):
    sudoku = CSP(variables, domains, neighbors, equal_constraint)
    if with_inferences:
        # problem 2.4
        return backtracking_search(assignment, sudoku, heuristic, mac)
    elif instrumented:
        # problem 2.3
        return instrumented_recursive_backtracking(assignment, sudoku, heuristic)
    else:
        # problem 2.2
        return recursive_backtracking_search(assignment, sudoku, heuristic)


if __name__ == '__main__':
    puzzles = ['001', '002', '010', '015', '025',
               '026', '048', '051',
               '062',
               '076', '081', '082', '090', '095', '099', '100']
    for p in puzzles:
        puzzle = SudokuIO(p)
        result = solve(puzzle.variables, puzzle.domains, puzzle.neighbors, puzzle.assignment, mrv, True, True)
        print('Puzzle {} result: {}'.format(p, result))
        puzzle.output_puzzle(result)
