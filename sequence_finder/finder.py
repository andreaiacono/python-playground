import random
from string import Template

from cStringIO import StringIO
import sys


OPERATORS = ['+=', '-=', '*=', '^=']
INPUT_NAME = 'input'
TEMPLATE = Template('''
#import math

def compute(''' + INPUT_NAME + '''):
$code
\treturn ''' + INPUT_NAME + '''

def fit(input, output):
    return input - output

#print(compute($input))
print(fit(compute($input), $output))

''')


def get_operator():
    return OPERATORS[random.randint(0, len(OPERATORS) - 1)]


def get_operand():


    if random.randint(0, 3) > 1:
        return str(random.randint(0, 10))

    return INPUT_NAME;




def get_new_program():
    code = ''
    for line in range(random.randint(1, 5)):
        code += '\t' + INPUT_NAME + ' ' + str(get_operator()) + ' ' + str(get_operand()) + '\n'
    return code


# program = get_new_program()
# print(program)
# print(exec(program))

def print_result(vals, code):
    return '<h2>Sequence finder</h2><br/>Requested sequence: ' + str(vals) + '</br>Code: <pre>' + str(code) + '</pre>'

def execute(values):
    print("starting")
    vals = map(int, values.split(","))

    result = 1
    counter = 0
    while result != 0:
        counter += 1
        code = get_new_program()
        print("Try: " + str(counter) + " CODE\n" + code)
        for i in range(len(vals)):
            old_stdout = sys.stdout
            redirected_output = sys.stdout = StringIO()
            exec(TEMPLATE.substitute(code=code, input=vals[i], output=str(i+1)))
            sys.stdout = old_stdout
            result += int(redirected_output.getvalue().strip())

    if result == 0:
        return print_result(vals, code)

