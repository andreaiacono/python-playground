import copy
import random
import time
import sys

from sequence_finder import constants
from sequence_finder import utils
from sequence_finder.expression import Expression
from sequence_finder.parser import NumericStringParser

__author__ = 'andrea'


class World:
    """
    this class represent a world where a population of programs will be evolved
    """

    def __init__(self):
        self.population = []
        self.nsp = NumericStringParser()
        for i in range(0, constants.POPULATION_SIZE):
            self.population.append(Expression(self.nsp))

    def start(self, vals):
        evolution_round = 0
        start = time.time()
        best_score = sys.maxint
        while True:
            evolution_round += 1
            best_index = 0
            for j in range(0, constants.POPULATION_SIZE):
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
                  ". Computing new population.. [" + str(self.population[best_index]) + "]: " + str(self.population[best_index].score))
            # print self.population

            self.evolve(best_index)
            print("New Round " + str(self.population[0].get_expression()))

        return self.population[best_index]

    def evolve(self, best_index):
        sorted_population = sorted(self.population, key=lambda p: p.score)
        new_population = [copy.copy(self.population[best_index])]
        new_population.extend(sorted_population[:-1])
        for i in range(2, constants.BEST_FIT_SIZE):
            if utils.prob(1, 3):
                new_population[i].mutate()
            if utils.prob(1, 3):
                self.crossover(new_population[i], new_population[i+1])
            pass

        for i in range(constants.BEST_FIT_SIZE, constants.POPULATION_SIZE-1):
            new_population[i] = Expression(self.nsp)

        self.population = new_population

    @staticmethod
    def get_fitness(expected_value, obtained_value):
        return abs(expected_value - obtained_value)

    @staticmethod
    def crossover(program1, program2):

        # print("progr1 =" + program1.get_code() + " progra2=" + program2.get_code())
        index1, expr1 = program1.get_random_subexpression()
        index2, expr2 = program2.get_random_subexpression()
        if index1 == -1 or index2 == -1:
            return
        # print("index1=" + str(index1) + " index2=" + str(index2))

        program1.remove_subexpression(index1)
        program2.remove_subexpression(index2)
        # print("now index1=" + str(index1) + " index2=" + str(index2))
        # print("after remove progr1 =" + program1.get_code() + " progra2=" + program2.get_code())

        program1.insert_subexpression_at(expr2, index1)
        program2.insert_subexpression_at(expr1, index2)
        # print("final progr1 =" + program1.get_code() + " progra2=" + program2.get_code())


