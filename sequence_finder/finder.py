from sequence_finder.world import World
import random

def get_result_table(vals):
    table = '<table border="1"><th>n</th>'
    for i in range(0, len(vals)):
        table += '<th>' + str(i + 1) + '</th>'

    table += '<tr><td>a(n)</td>'
    for val in vals:
        table += '<td>' + str(val) + '</td>'
    table += '</tr></table>'

    return table


def print_solution(vals, program):
    return '<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=AM_HTMLorMML-full"></script><h2>Sequence finder</h2><br/>Requested sequence: ' \
           + str(vals) + '<br/><br/>`a(n) = ' + str(program.get_presentation_code()) + '`<br/><br/>' + get_result_table(vals)


def print_best_result(vals, program):
    return '<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=AM_HTMLorMML-full"></script><h2>Sequence finder</h2><br/>No result found before timeout. Best solution so far: ' + \
           str(program.score) + '<br/><br/>`a(n) = ' + str(program.get_presentation_code()) + '`<br/><br>Expected results:' + get_result_table(vals) + \
           "<br>Obtained results:" + get_result_table(program.results)


def execute(values):
    #random.seed(348)
    vals = map(float, values.split(","))
    world = World()
    best_program = world.start(vals)

    if best_program.score == 0:
        return print_solution(vals, best_program)

    return print_best_result(vals, best_program)

print execute("1,4,9,16")