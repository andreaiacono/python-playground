import random
from string import Template
import sys
import time

from cStringIO import StringIO


OPERATORS = ['+=', '-=', '*=', '^=']
INPUT_NAME = 'input'
TEMPLATE = Template('''
#import math

def compute(''' + INPUT_NAME + '''):
$code
\treturn ''' + INPUT_NAME + '''

def fit(input, output):
    return input - output if input > output else output - input

#print(compute($input))
print(fit(compute($input), $output))

''')


def prob(n):
    return random.randint(1, n) == 1

def get_ops(line):
    operand = line[len(INPUT_NAME), 2]
    operator = line[len(INPUT_NAME)+ 2]
    print("opn=" + operand + " opt=" + operator)
    return [operand, operator]

def mutation(line):
    operator, operand = get_ops(line)

    if random.randint(1, 2) > 1:
        operand = get_operand()
    else:
        operator = get_operator()

    return '\t' + INPUT_NAME + ' ' + str(operator) + ' ' + str(operand) + '\n'


def get_operator():
    return OPERATORS[random.randint(0, len(OPERATORS) - 1)]


def get_operand():
    if prob(2):
        return str(random.randint(0, 5))

    return INPUT_NAME


def get_new_program():
    code = ''
    for line in range(random.randint(1, 3)):
        code += '\t' + INPUT_NAME + ' ' + str(get_operator()) + ' ' + str(get_operand()) + '\n'
    return code


def print_result(vals, code):

    table = '<table border="1">'
    for i in range(0, len(vals)):
        table += '<th>' + str(i+1) + '</th>'

    table += '<tr>'
    for val in vals:
        table += '<td>' + str(val) + '</td>'
    table += '</tr></table>'


    return '<h2>Sequence finder</h2><br/>Requested sequence: ' + str(vals) + '</br><br/>Code: <pre>' + str(
        code) + '</pre>' + table


def no_result(best_result, best_code, vals, results):

    table = '<table border="1">'
    for i in range(0, len(vals)):
        table += '<th>' + str(i+1) + '</th>'

    table += '<tr>'
    for val in vals:
        table += '<td>' + str(val) + '</td>'
    table += '</tr></table>'

    table += '<table border="1">'
    for i in range(0, len(results)):
        table += '<th>' + str(i+1) + '</th>'

    table += '<tr>'
    for result in results:
        table += '<td>' + str(result) + '</td>'
    table += '</tr></table>'
    return '<h2>Sequence finder</h2><br/>No result found before timeout. Best solution so far: ' + str(
        best_result) + '<br/>Code: <pre>' + str(best_code) + '</pre>' + table


def execute(values):
    print("starting")
    vals = map(int, values.split(","))

    result = 1
    best_results = []
    best_result = 1000000
    counter = 0
    best_code = ''
    start = time.time()
    while result != 0 and time.time() - start < 5:
        result = 0
        counter += 1
        code = get_new_program()
        results = []
        for i in range(len(vals)):
            old_stdout = sys.stdout
            redirected_output = sys.stdout = StringIO()
            exec(TEMPLATE.substitute(code=code, input=i + 1, output=vals[i]))
            sys.stdout = old_stdout
            partial_result = int(redirected_output.getvalue().strip())
            result += partial_result
            results.append(partial_result)
            print("result for input " + str(i + 1) + " ouput=" + str(vals[i]) + ": " + str(partial_result))

        print("Try: " + str(counter) + " - score " + str(result) + " - results=" + str(results) + "CODE\n" + code)

        if result < best_result:
            best_code = code
            best_result = result
            best_results = results

    if result == 0:
        return print_result(vals, code)

    return no_result(best_result, best_code, vals, best_results)

