## Game Theory toolkit Examples
from itertools import product
import random
import numpy as np
from tools.player import Player

#compute best response against a fixed profile for quadratique utility:

def quadratic_utility(strategy, profile, param=2):
	return strategy*sum(profile) - param*strategy**2

ready_player_one = Player(1, np.arange(0,10, 0.1), utility_function=quadratic_utility)

print ready_player_one.best_response_set([0,1,5,3])

#define general matching pennies utility function and compute best response against fixed profile:

def matching_penny_utility(strategy, profile):
	heads_count, tails_count = 0,0
	for value in profile:
		if value=='H':
			heads_count+=1
		elif value=='T':
			tails_count+=1
	heads_payoff = heads_count - tails_count
	if strategy == 'H':
		return heads_count
	else:
		return - heads_count

ready_player_two = Player(2, ['H', 'T'], utility_function=matching_penny_utility)

print ready_player_two.best_response_set(['H', 'H', 'H', 'H', 'H', 'T', 'T', 'T'])

