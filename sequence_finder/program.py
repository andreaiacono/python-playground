import random
import sys
from sequence_finder.parser import NumericStringParser
from sequence_finder import utils


INPUT_NAME = 'n'
OPERATORS = ['+', '-', '*', '/', '^']
UNARY_OPERATORS = ['+', '-']


class Program:
    """
    this class represents some lines of code to be executed
    """

    def __init__(self):
        self.score = sys.maxint
        self.results = []
        self._code = []
        self._code = self.get_expression()
        self.nsp = NumericStringParser()

    def clear_results(self):
        self.results = []

    def get_code(self):
        return self._code

    def get_presentation_code(self):
        return self._code[1:-1].lower()

    def set_code(self, new_code):
        self._code = new_code

    @staticmethod
    def get_random_operator():
        return OPERATORS[random.randint(0, len(OPERATORS) - 1)]

    @staticmethod
    def get_random_unary_operator():
        return UNARY_OPERATORS[random.randint(0, len(UNARY_OPERATORS) - 1)]

    def get_random_operand(self):
        if utils.prob(5, 5):
            if utils.prob(1, 2):
                if utils.prob(1, 4):
                    return str(random.randint(0, 10))
                else:
                    if utils.prob(1, 2):
                        return "PI"
                    else:
                        return "E"
            else:
                if utils.prob(1, 4):
                    return INPUT_NAME
                else:
                    prob = random.randint(0, 3)
                    if prob == 0:
                        return "sin" + self.get_expression()
                    elif prob == 1:
                        return "cos" + self.get_expression()
                    elif prob == 2:
                        return "tan" + self.get_expression()
                    else:
                        return "sgn" + self.get_expression()
        else:
            return self.get_expression()

    def get_expression(self):
        operator = self.get_random_operator()
        operand1 = self.get_random_operand()
        operand2 = self.get_random_operand()
        return "(" + operand1 + "" + operator + "" + operand2 + ")"

    def mutate(self):
        for index in range(0, len(self._code)):
            if self._code[index] == '(':
                if utils.prob(1, 5):
                    self.remove_parenthesis(index)
                    self._code = self._code[:index] + self.get_expression() + self._code[index:]
                    return

    def remove_parenthesis(self, index):
        open_parenthesis = 0
        expression = self._code
        for i in range(index, len(expression)):
            if expression[i] == '(':
                open_parenthesis += 1
            if expression[i] == ')':
                open_parenthesis -= 1

            if open_parenthesis == 0:
                self._code = expression[:index] + expression[i + 1:]
                return
        return

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
        return "Program: score=" + str(self.score) + " - Expression=" + self._code

