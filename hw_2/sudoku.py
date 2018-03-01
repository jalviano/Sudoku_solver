# sudoku.py

from sudoku_io import SudokuIO
from utils import CSP
from backtracking import (recursive_backtracking_search, instrumented_recursive_backtracking, backtracking_search,
                          first_unassigned_variable, mrv, no_inference, mac, equal_constraint)


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


def solve_problem_2_2(puzzles):
    print('Solving puzzles for problem 2.2...\n')
    for p in puzzles:
        puzzle = SudokuIO(p)
        sudoku = CSP(puzzle.variables, puzzle.domains, puzzle.neighbors, equal_constraint)
        result = recursive_backtracking_search(puzzle.assignment, sudoku, first_unassigned_variable)
        print('Puzzle {} result: {}'.format(p, result))
        puzzle.output_puzzle(result)


def solve_problem_2_3(puzzles):
    print('\n\nSolving puzzles for problem 2.3 without MRV...\n')
    for p in puzzles:
        puzzle = SudokuIO(p)
        sudoku = CSP(puzzle.variables, puzzle.domains, puzzle.neighbors, equal_constraint)
        result = instrumented_recursive_backtracking(puzzle.assignment, sudoku, first_unassigned_variable, [])
        print('Puzzle {} result: {}'.format(p, result))
        puzzle.output_puzzle(result)
    print('\n\nSolving puzzles for problem 2.3 with MRV...\n')
    for p in puzzles:
        puzzle = SudokuIO(p)
        sudoku = CSP(puzzle.variables, puzzle.domains, puzzle.neighbors, equal_constraint)
        result = instrumented_recursive_backtracking(puzzle.assignment, sudoku, mrv, [])
        print('Puzzle {} result: {}'.format(p, result))
        puzzle.output_puzzle(result)


def solve_problem_2_4(puzzles):
    print('\n\nSolving puzzles for problem 2.4 with AC-3 only...\n')
    for p in puzzles:
        puzzle = SudokuIO(p)
        sudoku = CSP(puzzle.variables, puzzle.domains, puzzle.neighbors, equal_constraint)
        result = backtracking_search(puzzle.assignment, sudoku, mrv, mac, False)
        print('Puzzle {} result: {}'.format(p, result))
        puzzle.output_puzzle(result)
    print('\n\nSolving puzzles for problem 2.4 with all inference methods...\n')
    for p in puzzles:
        puzzle = SudokuIO(p)
        sudoku = CSP(puzzle.variables, puzzle.domains, puzzle.neighbors, equal_constraint)
        result = backtracking_search(puzzle.assignment, sudoku, mrv, mac, True)
        print('Puzzle {} result: {}'.format(p, result))
        puzzle.output_puzzle(result)


if __name__ == '__main__':
    puzzles = ['001', '002', '010', '015', '025',
               '026', '048', '051',
               '062',
               '076', '081', '082', '090', '095', '099', '100']
    solve_problem_2_2(puzzles)
    solve_problem_2_3(puzzles)
    solve_problem_2_4(puzzles)
