# difficulty_classifier.py

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sudoku_io import SudokuIO
from utils import CSP
from backtracking import equal_constraint, order_domain_values, mrv


def recursive_backtracking_search(assignment, csp, guesses=[]):
    if len(assignment) == len(csp.variables):
        return sum(guesses)
    var = mrv(assignment, csp)
    values = order_domain_values(var, assignment, csp)
    guesses.append(len(values) - 1)
    for value in values:
        if csp.nconflicts(var, value, assignment) == 0:
            csp.assign(var, value, assignment)
            result = recursive_backtracking_search(assignment, csp, guesses)
            if result is not None:
                return result
            csp.unassign(var, assignment)
    return None


def get_init_domains(csp, assignment):
    d = {}
    for i in csp.variables:
        no = [assignment.get(n) for n in csp.neighbors[i]]
        l = []
        if len(csp.domains[i]) > 0:
            for j in range(1, 10):
                if j not in no:
                    l.append(j)
        d[i] = l
    return [len(v) for v in d.values()]


def format_trn_data():
    puzzles = {
        '1-1': 1,
        '1-2': 1,
        '1-3': 1,
        '1-4': 1,
        '1-5': 1,
        '2-1': 2,
        '2-2': 2,
        '2-3': 2,
        '2-4': 2,
        '2-5': 2,
        '3-1': 3,
        '3-2': 3,
        '3-3': 3,
        '3-4': 3,
        '3-5': 3,
        '4-1': 4,
        '4-2': 4,
        '4-3': 4,
        '4-4': 4,
        '4-5': 4,
    }
    trn_x = open('data/trn_x.txt', 'w')
    trn_y = open('data/trn_y.txt', 'w')
    for k, v in puzzles.items():
        puzzle = SudokuIO(k)
        sudoku = CSP(puzzle.variables, puzzle.domains, puzzle.neighbors, equal_constraint)
        domain_sizes = get_init_domains(sudoku, puzzle.assignment)
        guesses = recursive_backtracking_search(puzzle.assignment, sudoku)
        features = domain_sizes + [guesses, ]
        for j in range(len(features)):
            if j != len(features) - 1:
                trn_x.write(str(features[j]) + ', ')
            else:
                trn_x.write(str(features[j]) + '\n')
        trn_y.write(str(v) + '\n')


def format_tst_data():
    puzzles = {
        '001': 1,
        '002': 1,
        '010': 1,
        '015': 1,
        '025': 1,
        '026': 2,
        '048': 2,
        '051': 2,
        '062': 3,
        '076': 4,
        '081': 4,
        '082': 4,
        '090': 4,
        '095': 4,
        '099': 4,
        '100': 4,
    }
    trn_x = open('data/tst_x.txt', 'w')
    trn_y = open('data/tst_y.txt', 'w')
    for k, v in puzzles.items():
        puzzle = SudokuIO(k)
        sudoku = CSP(puzzle.variables, puzzle.domains, puzzle.neighbors, equal_constraint)
        domain_sizes = get_init_domains(sudoku, puzzle.assignment)
        guesses = recursive_backtracking_search(puzzle.assignment, sudoku)
        features = domain_sizes + [guesses, ]
        for j in range(len(features)):
            if j != len(features) - 1:
                trn_x.write(str(features[j]) + ', ')
            else:
                trn_x.write(str(features[j]) + '\n')
        trn_y.write(str(v) + '\n')


def read_trn_data():
    train_x = np.loadtxt('data/trn_x.txt', delimiter=', ', dtype=int)
    train_y = np.loadtxt('data/trn_y.txt', delimiter=', ', dtype=int)
    return train_x, train_y


def read_tst_data():
    test_x = np.loadtxt('data/tst_x.txt', delimiter=', ', dtype=int)
    return test_x


def build_classifier():
    X, y = read_trn_data()
    model = KNeighborsClassifier(n_neighbors=1)
    score = cross_val_score(model, X, y, cv=StratifiedKFold(n_splits=2), scoring='accuracy')
    mean_score = np.array(score).mean()
    print('Estimated accuracy: {}'.format(mean_score))
    x = read_tst_data()
    model.fit(X, y)
    pred = model.predict(x)
    print(pred)


if __name__ == '__main__':
    # format_trn_data()
    # format_tst_data()
    build_classifier()
