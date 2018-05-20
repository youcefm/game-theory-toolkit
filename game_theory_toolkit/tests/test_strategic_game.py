import numpy as np
#from ..game import StrategicGame
#from ..player import Player
#import game_theory_toolkit

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from game import StrategicGame, TwoPlayerEvolutionaryGame, EvolutionaryGame
from player import Player

s = [1,2,3]
p =[1.0/3, 1.0/3, 1.0/3]
players ={1: Player(1, p, lambda x: x), 2: Player(1, p, lambda x: x)}

g = StrategicGame(players=players)
print 'What is this object:', str(g)
print 'New function: ', g.UniformlyRandomStrategy()
c = g.contingencies()
l = []
for el in c:
	l.append(list(el))
print 'Manual calculation: ', l
print l[1][1]

def matching_penny_utility(strategy, profile, level = 10):
	heads_count, tails_count = 0,0
	for value in profile:
		if value=='H':
			heads_count+=1
		elif value=='T':
			tails_count+=1
	heads_payoff = heads_count - tails_count
	if strategy == 'H':
		return heads_payoff + level
	else:
		return - heads_payoff + level

eg = TwoPlayerEvolutionaryGame(Player(1, ['H', 'T'], matching_penny_utility),
	Player(1, ['H', 'T'], matching_penny_utility), {1: [0.25, 0.75], 2: [0.25, 0.75]})
eg.compute_current_fitness()
print 'Current Fitness: ', eg.current_fitness
print 'Intial Population: ', eg.current_population_distributions
eg.replicator_dynamics_step()
print 'New Population: ', eg.current_population_distributions

print '--- Try with Evolutionary Game ---'
neg = EvolutionaryGame(Player(1, ['H', 'T'], matching_penny_utility), [0.25, 0.75])
print 'Intial Population: ', neg.current_population_distribution
neg.replicator_dynamics_step()
print 'New Population: ', neg.current_population_distribution
