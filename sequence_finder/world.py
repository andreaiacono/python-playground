import time
import sys
import random

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
        while True:
            evolution_round += 1
            best_index = -1
            print("bew best index")
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

            # if timeout exits the loop
            if time.time() - start > constants.EXECUTION_TIMEOUT:
                break

            # renew the population according to best scores
            self.next_round()

        return self.population[best_index]

    def next_round(self):
        sorted_population = sorted(self.population, key=lambda p: p.score)
        for i in range(0, constants.BEST_FIT_SIZE):
            program = sorted_population[i]
            # if utils.prob(1, 3):
            #     program.mutate()
            if utils.prob(1, 3):
                sorted_population[i], sorted_population[i+1] = self.crossover(program, sorted_population[i+1])

    @staticmethod
    def get_fitness(expected_value, obtained_value):
        return abs(expected_value - obtained_value)

    def crossover(self, program1, program2):

        len1 = len(program1.get_code())
        len2 = len(program2.get_code())

        min_len = len1 if len1 < len2 else len2
        crossover = random.randint(1, min_len)
        new_code1 = program1._code[0:crossover] + program2._code[crossover:len2-1]
        new_code2 = program2._code[0:crossover] + program1._code[crossover:len1-1]
        program1.set_code(new_code1)
        program2.set_code(new_code2)

        return [program1, program2]

