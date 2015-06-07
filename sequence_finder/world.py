import time
import sys

from sequence_finder import constants
from sequence_finder import utils
from sequence_finder.program import Program


__author__ = 'andrea'


class World:
    """
    this class represent a world where a population of programs will be evolved
    """

    def __init__(self):
        self.population = []
        for i in range(0, constants.POPULATION_SIZE):
            self.population.append(Program())

    def evolve(self, vals):
        best_score = sys.maxint
        evolution_round = 0
        start = time.time()
        best_index = -1
        while time.time() - start < constants.EXECUTION_TIMEOUT:
            evolution_round += 1
            best_index = -1
            for j in range(0, constants.POPULATION_SIZE):
                score = 0
                program = self.population[j]
                program.clear_results()
                for i in range(len(vals)):
                    partial_result = program.execute_code(i + 1)
                    score += self.get_fitness(vals[i], partial_result)
                    program.add_result(partial_result)
                    print("Input: " + str(i + 1) + " - Expected output:" + str(vals[i]) + " - Obtained output:" + str(partial_result))

                program.set_score(score)
                print("Round " + str(evolution_round) + " - Program #" + str(j) + " - score " + str(score) + " - bestscore: " + str(best_score) + " - bestindex=" + str(best_index ) + " - results=" + str(program.results) + "CODE\n" + program.get_code())

                if score < best_score or (score == best_score and len(program.get_code().split("\n")) < len(self.population[best_index].get_code().split("\n"))):
                    best_index = j
                    best_score = score

                if score == 0:
                    return program

            # renew the population according to best scores
            #self.population = self.next_round(self.population)

        return self.population[best_index]

    def next_round(self, population):
        new_population = []
        sorted_population = sorted(self.population, key=lambda program: program.score)
        for program in new_population:
            if utils.prob(1, 3):
                program = mutation(program)


    @staticmethod
    def get_fitness(expected_value, obtained_value):
        return abs(expected_value - obtained_value)

    def mutation(self, line):
        operator, operand = get_ops(line)

        if random.randint(1, 2) > 1:
            operand = get_operand()
        else:
            operator = get_operator()

        return '\t' + INPUT_NAME + ' ' + str(operator) + ' ' + str(operand) + '\n'