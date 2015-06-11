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

    def start(self, vals):
        evolution_round = 0
        start = time.time()
        best_score = sys.maxint
        while True:
            evolution_round += 1
            best_index = 0
            for j in range(1, constants.POPULATION_SIZE):
                score = 0.0
                program = self.population[j]
                program.clear_results()
                for i in range(len(vals)):
                    partial_result = program.execute_code(i + 1)
                    score += self.get_fitness(vals[i], partial_result)
                    program.add_result(partial_result)

                # print("evaluating " + program.get_presentation_code() + ": " + str(score) + " - Best: " + str(best_score) + "[" + str(best_index) + "]")
                program.set_score(score)
                if score < best_score:
                    best_index = j
                    best_score = score

                if score == 0:
                    return program

            # if timeout exits the loop
            if time.time() - start > constants.EXECUTION_TIMEOUT:
                break

            # renew the population according to best scores
            print("Round " + str(evolution_round) + " finished. Best score: " + str(best_score) + " - Best index: " + str(best_index) +
                  ". Computing new population.. [" + str(self.population[best_index]) + "]")
            print self.population

            self.evolve()

        return self.population[best_index]

    def evolve(self):
        sorted_population = sorted(self.population, key=lambda p: p.score)
        new_population = [sorted_population[0]]
        new_population.extend(sorted_population[:-1])
        for i in range(1, constants.BEST_FIT_SIZE):
            if utils.prob(1, 3):
                new_population[i].mutate()
            # if utils.prob(1, 3):
            #     new_population[i], new_population[i + 1] = self.crossover(new_population[i], new_population[i + 1])

        for i in range(constants.BEST_FIT_SIZE, constants.POPULATION_SIZE-1):
            new_population[i] = Program()

        self.population = new_population

    @staticmethod
    def get_fitness(expected_value, obtained_value):
        return abs(expected_value - obtained_value)

    def crossover(self, program1, program2):

        len1 = len(program1.get_code())
        len2 = len(program2.get_code())

        shorter = program1.get_code() if len1 < len2 else program2.get_code()
        # for index in range(0, len(program1.get_code())-1):
        # if shorter[index] == '(':
        #         if utils.prob(1, 5):
        #             index1 = index
        #
        # for index in range(0, len(program2.get_code())-1):
        #     if shorter[index] == '(':
        #         if utils.prob(1, 5):
        #             index2 = index

        #
        #
        # new_code1 = program1._code[0:crossover] + program2._code[crossover:len2 - 1]
        # new_code2 = program2._code[0:crossover] + program1._code[crossover:len1 - 1]
        # program1.set_code(new_code1)
        # program2.set_code(new_code2)

        return [program1, program2]

