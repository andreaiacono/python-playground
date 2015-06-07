__author__ = 'andrea'

import random
import sys
from string import Template
from cStringIO import StringIO

from sequence_finder import utils


INPUT_NAME = 'n'
OPERATORS = ['+=', '-=', '*=', '=']
TEMPLATE = Template('''

def compute(''' + INPUT_NAME + '''):
$code
\treturn ''' + INPUT_NAME + '''

print(compute($input))
''')


class Program:
    """
    this class represents some lines of code to be executed
    """

    def __init__(self):
        self.score = sys.maxint
        self.results = []
        self._code = []
        for line in range(random.randint(1, 5)):
            while True:
                operand = self.get_operand()
                operator = self.get_operator()
                if not self.is_useless(operator, operand):
                    break
            self._code.append('\t' + INPUT_NAME + ' ' + str(operator) + ' ' + str(operand))

    def clear_results(self):
        self.results = []

    def is_useless(self, operator, operand):
        return (operand == '0' and operator == '+=') \
               or (operand == '0' and operator == '-=') \
               or (operand == '1' and operator == '*=') \
               or (operand == '1' and operator == '/=') \
               or (operand == INPUT_NAME and operator == '=')

    def get_code(self):
        code = ''
        for line in self._code:
            code += line + "\n"
        return code

    def get_ops(self, index):
        operand = self._code[index][len(INPUT_NAME), 2]
        operator = self._code[index][len(INPUT_NAME) + 2]
        return [operand, operator]

    def get_operator(self):
        return OPERATORS[random.randint(0, len(OPERATORS) - 1)]

    def get_operand(self):
        if utils.prob(1, 2):
            return str(random.randint(0, 5))
        return INPUT_NAME

    def execute_code(self, i):
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        exec (TEMPLATE.substitute(code=self.get_code(), input=i))
        sys.stdout = old_stdout
        return int(redirected_output.getvalue().strip())

    def set_score(self, score):
        self.score = score

    def add_result(self, result):
        self.results.append(result)

    def __repr__(self):
        return "Program: score=" + str(self.score)