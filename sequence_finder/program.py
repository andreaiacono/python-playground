import random
import sys
from sequence_finder.parser import NumericStringParser
from sequence_finder import utils


INPUT_NAME = 'N'
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
        while True:
            self._code = self.create_expression()
            if INPUT_NAME in self._code:
                break
        # print("program: " + str(self))
        self.nsp = NumericStringParser()

    def clear_results(self):
        self.results = []
        self.score = sys.maxint

    def get_code(self):
        return self._code

    def get_presentation_code(self):
        return self._code[1:-1].lower()

    def set_code(self, new_code):
        self._code = new_code

    def get_random_subexpression(self):
        parenthesis = []
        for index in range(1, len(self._code)):
            if self._code[index] == '(' and self._code[index-1] != 's' and self._code[index-1] != 'n':
                parenthesis.append(index)

        if len(parenthesis) == 0:
            return -1, ""

        index = random.choice(parenthesis)
        print("index=" + str(index))
        return index, self.get_subexpression_starting_at(index)

    def insert_subexpression_at(self, expression, index):
        print("called index=" + str(index))
        self._code = self._code[:index] + expression + self._code[index+1:]

    def get_subexpression_starting_at(self, index):
        open_parenthesis = 0
        expression = self._code
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

    def create_expression(self):
        expression = "(" + self.get_random_operand()
        for i in range(0, random.randint(0, 4)):
            expression += self.get_random_operator()
            expression += self.get_random_operand()
        return expression + ")"

    def mutate(self):
        for index in range(0, len(self._code)):
            if self._code[index] == '(':
                if utils.prob(1, 5):
                    self.remove_subexpression(index)
                    self._code = self._code[:index] + self.create_expression() + self._code[index:]
                    return

    def remove_subexpression(self, index):
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

