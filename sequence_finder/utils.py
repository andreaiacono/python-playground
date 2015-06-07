__author__ = 'andrea'

import random

def prob(n, m):
    '''
    computes a random probability
    :param n:
    :param m:
    :return: true if a random value from 0 to m is greater then n
    '''
    return random.randint(0, m) > n

