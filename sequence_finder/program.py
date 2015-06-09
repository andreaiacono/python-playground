from sequence_finder.parser import NumericStringParser

__author__ = 'andrea'

import random
import sys
from string import Template
from cStringIO import StringIO

from sequence_finder import utils


INPUT_NAME = 'n'
PREFIX = '\t'
OPERATORS = ['+', '-', '*', '/', '^']
UNARY_OPERATORS = ['+', '-']
CODE_TEMPLATE = Template('''

def compute(''' + INPUT_NAME + '''):
$code
\treturn ''' + INPUT_NAME + '''

print(compute($input))
''')

LINE_TEMPLATE = Template(PREFIX + '$input $operator $operand')


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

                # if utils.prob(1, 5):
                # # unary
                #     operand = self.get_random_operand()
                #     operator = self.get_random_unary_operator()
                # else:
                self._code = self.get_expression()
                # print(self._code)

                if utils.prob(1, 8):
                    break

        self.nsp = NumericStringParser()

    def clear_results(self):
        self.results = []

    def is_useless(self, operator, operand):
        return (operand == '0' and operator == '+=') \
               or (operand == '0' and operator == '-=') \
               or (operand == '1' and operator == '*=') \
               or (operand == '1' and operator == '/=') \
               or (operand == INPUT_NAME and operator == '=')

    def get_code(self):
        return self._code

    def set_code(self, new_code):
        self._code = new_code

    def get_ops(self, index):
        operand = self._code[index][len(PREFIX):len(PREFIX) + len(INPUT_NAME)]
        operator = self._code[index][len(PREFIX) + len(INPUT_NAME) + 3:].strip()
        return [operand, operator]

    @staticmethod
    def get_random_operator():
        return OPERATORS[random.randint(0, len(OPERATORS) - 1)]

    @staticmethod
    def get_random_unary_operator():
        return UNARY_OPERATORS[random.randint(0, len(UNARY_OPERATORS) - 1)]

    def get_random_operand(self):
        if utils.prob(1, 2):
            if utils.prob(1, 2):
                return str(random.randint(0, 10))
            else:
                if utils.prob(1, 4):
                    return INPUT_NAME
                else:
                    return "sin" + self.get_expression()
        else:
            return self.get_expression()

    def get_expression(self):
        operator = self.get_random_operator()
        operand1 = self.get_random_operand()
        operand2 = self.get_random_operand()
        return "(" + operand1 + "" + operator + "" + operand2 + ")"

    def mutate(self):
        line_index = random.randint(0, len(self._code) - 1)
        operator, operand = self.get_ops(line_index)

        if random.randint(1, 2) > 1:
            operand = self.get_random_operand()
        else:
            operator = self.get_random_operator()

        self._code[line_index] = LINE_TEMPLATE.substitute(input=INPUT_NAME, operator=operator, operand=operand)

    def execute_code(self, i):
        code = self._code.replace(INPUT_NAME, str(i))
        try:
            result = self.nsp.eval(code)
        except ZeroDivisionError:
            result = 0
        except ValueError:
            result = 0
        except OverflowError:
            result = sys.maxint

        return result

    def set_score(self, score):
        self.score = score

    def add_result(self, result):
        self.results.append(result)

    def __repr__(self):
        return "Program: score=" + str(self.score)
