import random
import sys
from sequence_finder import utils


INPUT_NAME = 'N'
OPERATORS = ['+', '-', '*', '/', '^']
UNARY_OPERATORS = ['+', '-']


class Expression:
    """
    this class represents some lines of code to be executed
    """

    def __init__(self, nsp, expression = None):
        self.score = sys.maxint
        self.results = []
        self._expression = (self.create_complete_expression() if expression is None else expression)
        print("program: " + str(self))
        self.nsp = nsp

    def clear_results(self):
        self.results = []
        self.score = sys.maxint

    def get_expression(self):
        return self._expression

    def get_presentation_code(self):
        '''
        returns the expression without the outer parenthesis
        '''
        return self._expression[1:-1].lower()

    def insert_subexpression_at(self, expression, index):
        # print("called index=" + str(index))
        self._expression = self._expression[:index] + expression + self._expression[index + 1:]

    def get_random_subexpression(self):
        parenthesis = []
        for index in range(1, len(self._expression)):
            if self._expression[index] == '(' and self._expression[index-1] != 's' and self._expression[index-1] != 'n':
                parenthesis.append(index)

        if len(parenthesis) == 0:
            return -1, ""

        index = random.choice(parenthesis)
        # print("index=" + str(index))
        return index, self.get_subexpression_starting_at(index)

    def get_subexpression_starting_at(self, index):
        open_parenthesis = 0
        expression = self._expression
        for i in range(index, len(expression)):
            if expression[i] == '(':
                open_parenthesis += 1
            if expression[i] == ')':
                open_parenthesis -= 1

            if open_parenthesis == 0:
                return expression[:index] + expression[i + 1:]

        return expression


    @staticmethod
    def get_random_operator():
        return OPERATORS[random.randint(0, len(OPERATORS) - 1)]

    @staticmethod
    def get_random_unary_operator():
        return UNARY_OPERATORS[random.randint(0, len(UNARY_OPERATORS) - 1)]

    def get_random_operand(self):
        if utils.prob(3, 4):
            if utils.prob(2, 4):
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
                prob = random.randint(0, 2)
                if prob == 0:
                    return "sin" + self.create_expression()
                elif prob == 1:
                    return "cos" + self.create_expression()
                else:
                    return "tan" + self.create_expression()

    def create_complete_expression(self):
        while True:
            expression = self.create_expression()
            if INPUT_NAME in expression:
                break

        return expression

    def create_expression(self):
        expression = "(" + self.get_random_operand()
        for i in range(0, random.randint(0, 4)):
            expression += self.get_random_operator()
            expression += self.get_random_operand()
        return expression + ")"

    def mutate(self):
        for index in range(0, len(self._expression)):
            if self._expression[index] == '(':
                if utils.prob(1, 5):
                    self.remove_subexpression(index)
                    self._expression = self._expression[:index] + self.create_expression() + self._expression[index:]
                    return

    def remove_subexpression(self, index):
        open_parenthesis = 0
        expression = self._expression
        for i in range(index, len(expression)):
            if expression[i] == '(':
                open_parenthesis += 1
            if expression[i] == ')':
                open_parenthesis -= 1

            if open_parenthesis == 0:
                self._expression = expression[:index] + expression[i + 1:]
                return
        return

    def execute_code(self, i):
        code = self._expression.replace(INPUT_NAME, str(i))
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
        return "Program: score=" + str(self.score) + " - Expression=" + self._expression

