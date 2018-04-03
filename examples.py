## Game Theory toolkit Examples
from itertools import product
import random
import numpy as np
from tools.player import Player

#find best response against a fixed profile for quadratique utility:

def quadratic_utility(strategy, profile, param=0.2):
	return strategy+sum(profile) - param*strategy**2

ready_player_one = Player(1, np.arange(0,10, 0.1), utility_function=quadratic_utility)

#for strategy in ready_player_one.strategies:
#	print strategy, ready_player_one.evaluate_payoff(strategy, [0,1,5,3])
print ready_player_one.best_response_set([0,1,5,3])