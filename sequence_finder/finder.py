import random
from string import Template


OPERATORS = ['+=', '-=', '*=', '/=', '^n']
INPUT_NAME = 'input'
TEMPLATE = Template('''
#import math

def compute(''' + INPUT_NAME + ''', output):
$code
\treturn ''' + INPUT_NAME + '''

''')


def get_operator():
    return OPERATORS[random.randint(0, len(OPERATORS) - 1)]


def get_operand():
    return str(random.randint(0, 10))


def get_new_program():
    code = ''
    for line in range(random.randint(0, 5)):
        code += '\t' + INPUT_NAME + ' ' + str(get_operator()) + ' ' + str(get_operand()) + '\n'
    return TEMPLATE.substitute(code=code)

# program = get_new_program()
# print(program)
# print(exec(program))


def execute(values):
    vals = map(int, values.split(","))
    return "execution result: " + str(vals[2])