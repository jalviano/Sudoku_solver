# backtracking.py

from utils import (first, argmin_random_tie, num_legal_values, revise, same_row, same_col, same_box,
                   get_row, get_col, get_box)


def order_domain_values(var, assignment, csp):
    return csp.choices(var)


def first_unassigned_variable(assignment, csp):
    return first([var for var in csp.variables if var not in assignment])


def mrv(assignment, csp):
    return argmin_random_tie([v for v in csp.variables if v not in assignment],
                             key=lambda var: num_legal_values(csp, var, assignment))


def no_inference(csp, var, value, assignment, removals):
    return True


def mac(csp, var, value, assignment, removals):
    ac3 = AC3(csp, [(X, var) for X in csp.neighbors[var]], removals)
    return ac3


def AC3(csp, queue=None, removals=None):
    if queue is None:
        queue = [(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]]
    csp.support_pruning()
    while queue:
        (Xi, Xj) = queue.pop()
        if revise(csp, Xi, Xj, removals):
            if not csp.curr_domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return True


def find_pairs(csp, removals):
    for v1 in csp.variables:
        d1 = set(csp.curr_domains[v1])
        for v2 in csp.neighbors[v1]:
            d2 = set(csp.curr_domains[v2])
            if len(d1) == 2 and d1 == d2:
                others = []
                if same_row(v1, v2):
                    others = get_row(v1)
                elif same_col(v1, v2):
                    others = get_col(v1)
                if same_box(v1, v2):
                    others += get_box(v1)
                for v3 in set(others):
                    if v3 != v1 and v3 != v2:
                        for d in csp.curr_domains[v3]:
                            if d in d1:
                                csp.prune(v3, d, removals)


def find_intersections(csp, var, value, assignment, removals):

    def intersection(overlap):
        box = get_box(var)
        if len(overlap) == 1 or len(overlap) == 2:
            same = True
            for v in overlap:
                if box != get_box(v):
                    same = False
            if same:
                for v in box:
                    d = csp.curr_domains[v]
                    if v != var and v not in overlap and value in d:
                        csp.prune(v, value, removals)

    row_overlap = [v for v in get_row(var) if v != var and value in csp.curr_domains[v]]
    intersection(row_overlap)
    col_overlap = [v for v in get_col(var) if v != var and value in csp.curr_domains[v]]
    intersection(col_overlap)


def init_domains(csp, assignment):
    # d = {i: [j for j in range(1, 10) if j not in [assignment.get(n) for n in csp.neighbors[i]]] for i in csp.variables}
    d = {}
    for i in csp.variables:
        no = [assignment.get(n) for n in csp.neighbors[i]]
        l = []
        if len(csp.domains[i]) > 0:
            for j in range(1, 10):
                if j not in no:
                    l.append(j)
        d[i] = l
    csp.curr_domains = d
    """empty = len([v for v in d.values() if len(v) == 0])
    ave = sum([len(v) for v in d.values()]) / empty
    print('Average domain size: {}', ave)"""


def recursive_backtracking_search(assignment, csp, heuristic):
    if len(assignment) == len(csp.variables):
        return assignment
    var = heuristic(assignment, csp)
    for value in order_domain_values(var, assignment, csp):
        if csp.nconflicts(var, value, assignment) == 0:
            csp.assign(var, value, assignment)
            result = recursive_backtracking_search(assignment, csp, heuristic)
            if result is not None:
                return result
            csp.unassign(var, assignment)
    return None


def instrumented_recursive_backtracking(assignment, csp, heuristic, guesses=0):
    if len(assignment) == len(csp.variables):
        print('{} guesses'.format(guesses))
        return assignment
    var = heuristic(assignment, csp)
    values = order_domain_values(var, assignment, csp)
    guesses += len(values) - 1
    for value in values:
        if csp.nconflicts(var, value, assignment) == 0:
            csp.assign(var, value, assignment)
            result = instrumented_recursive_backtracking(assignment, csp, heuristic, guesses)
            if result is not None:
                return result
            csp.unassign(var, assignment)
    return None


def backtracking_search(a, csp, heuristic, inference):

    def backtrack(assignment, guesses=0):
        if len(assignment) == len(csp.variables):
            print('{} guesses'.format(guesses))
            return assignment
        var = heuristic(assignment, csp)
        values = order_domain_values(var, assignment, csp)
        guesses += len(values) - 1
        for value in values:
            if csp.nconflicts(var, value, assignment) == 0:
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                find_pairs(csp, removals)
                # find_intersections(csp, var, value, assignment, removals)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment, guesses)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    init_domains(csp, a)
    return backtrack(a)
