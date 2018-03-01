# sudoku_io.py

from utils import same_row, same_col, same_box


class SudokuIO(object):

    def __init__(self, input='001', output='puzzles/output.txt'):
        self.input = 'puzzles/puzzle_{}.txt'.format(input)
        self.output = output
        self.NUM_VARS = 81
        self.vars = [0] * self.NUM_VARS
        self.var_domain = [[None] * 9 for _ in range(self.NUM_VARS)]
        self.variables = [i for i in range(81)]
        self._build_puzzle()
        self.domains = self._domains()
        self.neighbors = {i: [j for j in range(81) if i != j and (same_row(i, j) or same_col(i, j) or same_box(i, j))]
                          for i in self.variables}
        self.assignment = {i: self.vars[i] for i in self.variables if self.vars[i] != 0}

    def _domains(self):
        d = {}
        for i in self.variables:
            if self.vars[i] == 0:
                l = [j for j in range(1, 10)]
            else:
                l = [self.vars[i]]
            d[i] = l
        return d

    def _build_puzzle(self):
        file = open(self.input, 'r')
        for a in range(self.NUM_VARS):
            ch = ' '
            while ch == '\n' or ch == '\r' or ch == ' ':
                ch = file.readline(1)
            if ch == '-':
                self.vars[a] = 0
            else:
                s = '' + ch
                i = int(s)
                self.vars[a] = i
                for j in range(9):
                    if j == i - 1:
                        self.var_domain[a][j] = True
                    else:
                        self.var_domain[a][j] = False

    def output_puzzle(self, solution):
        file = open(self.output, 'w')
        for a in range(9):
            for b in range(9):
                c = 9 * a + b
                if solution[c] == 0:
                    file.write('- ')
                else:
                    file.write(str(solution[c]) + ' ')
            file.write('\r\n')
