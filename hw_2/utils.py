# csp.py

import math
import random


class Problem(object):

    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def actions(self, node):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, node):
        if isinstance(self.goal, list):
            return is_in(node.state, self.goal)
        else:
            return node.state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self, state):
        raise NotImplementedError


class CSP(Problem):

    def __init__(self, variables, domains, neighbors, constraints):
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.curr_domains = None
        self.nassigns = 0

    def assign(self, var, val, assignment):
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, val, assignment):
        def conflict(var2):
            return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])
        return count(conflict(v) for v in self.neighbors[var])

    def display(self, assignment):
        print('CSP:', self, 'with assignment:', assignment)

    def actions(self, state):
        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = first([v for v in self.variables if v not in assignment])
            return [(var, val) for val in self.domains[var] if self.nconflicts(var, val, assignment) == 0]

    def result(self, state, action):
        (var, val) = action
        return state + ((var, val),)

    def goal_test(self, state):
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    def support_pruning(self):
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):
        self.support_pruning()
        return {v: self.curr_domains[v][0] for v in self.variables if 1 == len(self.curr_domains[v])}

    def restore(self, removals):
        for B, b in removals:
            self.curr_domains[B].append(b)

    def conflicted_vars(self, current):
        return [var for var in self.variables if self.nconflicts(var, current[var], current) > 0]


def count(seq):
    return sum(bool(x) for x in seq)


def first(iterable, default=None):
    try:
        return iterable[0]
    except IndexError:
        return default
    except TypeError:
        return next(iterable, default)


def is_in(elt, seq):
    return any(x is elt for x in seq)


def get_x(i):
    return math.floor(i / 9)


def get_y(i):
    return i % 9


def same_row(i, j):
    if get_x(i) == get_x(j):
        return True
    return False


def same_col(i, j):
    if get_y(i) == get_y(j):
        return True
    return False


def same_box(i, j):
    xi = get_x(i)
    yi = get_y(i)
    xj = get_x(j)
    yj = get_y(j)
    return (int(xi / 3), int(yi / 3)) == (int(xj / 3), int(yj / 3))


def get_col(i):
    return [j for j in range(0, 81) if same_col(i, j)]


def get_row(i):
    return [j for j in range(0, 81) if same_row(i, j)]


def get_box(i):
    return [j for j in range(0, 81) if same_box(i, j)]


def num_legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        return count(csp.nconflicts(var, val, assignment) == 0 for val in csp.domains[var])


def argmin_random_tie(seq, key=(lambda x: x)):
    # return min(shuffled(seq), key=key)
    return min(seq, key=key)


def shuffled(iterable):
    items = list(iterable)
    random.shuffle(items)
    return items


def revise(csp, Xi, Xj, removals):
    revised = False
    for x in csp.curr_domains[Xi]:
        if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised
