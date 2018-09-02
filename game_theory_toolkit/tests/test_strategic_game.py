import numpy as np
#from ..game import StrategicGame
#from ..player import Player
#import game_theory_toolkit

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from game import StrategicGame, TwoPlayerEvolutionaryGame, EvolutionaryGame
from player import Player, PlayerSet

s = [1,2,3]
p =[1.0/3, 1.0/3, 1.0/3]
players ={1: Player(1, p, lambda x: x), 2: Player(1, p, lambda x: x)}

g = StrategicGame(players=players)
print 'What is this object:', str(g)


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
	Player(1, ['H', 'T'], matching_penny_utility), {1: [0.4, 0.6], 2: [0.4, 0.6]})
eg.compute_current_fitness()
print 'Current Fitness: ', eg.current_fitness
print 'Intial Population: ', eg.current_population_distributions
#eg.replicator_dynamics_step()
#print 'New Population: ', eg.current_population_distributions
print 'ESS is: ', eg.find_ess().ess

print '--- Try with Evolutionary Game ---'
neg = EvolutionaryGame(Player(1, ['H', 'T'], matching_penny_utility), [0.25, 0.75])
print 'Intial Population: ', neg.current_population_distribution
neg.replicator_dynamics_step()
print 'New Population: ', neg.current_population_distribution
neg.current_population_distribution = [0.5, 0.5]
print 'Find ESS: ', neg.find_ess().ess

p = PlayerSet()

def p_f(x, y):
	return 4*(x+y)**0.5 - x

p.add(Player('Al', range(5), p_f))
p.add(Player('So', range(5), p_f))

print p.compute_action_profiles().compute_profile_distribution().expected_payoff(0)
print p.action_profiles
print p.profile_distribution

#location game

def loc_profit_fnc(loc1, other_locs):
	num_same = 0
	N = len(other_locs)
	for loc in other_locs:
		if loc == loc1:
			num_same += 1
	if num_same == N:
		#print 'payoff 1: ', 1.0/(num_same+1)
		return round(1.0/(num_same+1),4)

	other_locs = [x for x in other_locs if x != loc1]
	#print 'new other locs: ', other_locs

	if loc1 < min(other_locs):
		#print 'payoff 2: ', ((loc1 + min(other_locs))/2.0)/(num_same+1.0)
		return round(((loc1 + min(other_locs))/2.0)/(num_same+1.0),4)
	elif loc1 > max(other_locs):
		#print 'payoff 3: ', (1.0-(loc1 + max(other_locs))/2.0)/(num_same+1.0)
		return round((1.0-(loc1 + max(other_locs))/2.0)/(num_same+1.0),4)
	else:
		lower, upper = [], []
		for loc in other_locs:
			if loc < loc1:
				lower.append(loc)
			elif loc > loc1:
				upper.append(loc)
		#print 'Payoff 4: ', ((min(upper) + loc1)/2.0 - (max(lower) + loc1)/2.0)/(num_same+1.0)
		return round(((min(upper) + loc1)/2.0 - (max(lower) + loc1)/2.0)/(num_same+1.0),4)

print 'answer should be 0.5:  ', loc_profit_fnc(0.5, [0.5001])
print 'answer should be 0.3:  ', loc_profit_fnc(0.9, [0.5])
ps = PlayerSet()
action_set = np.arange(0,1.01, 0.01)
ps.add(Player('Al', [round(x,2) for x in action_set], loc_profit_fnc))
ps.add(Player('Link', [round(x,2) for x in action_set], loc_profit_fnc))
ps.add(Player('Ynk', [round(x,2) for x in action_set], loc_profit_fnc))
ps.add(Player('Snk', [round(x,2) for x in action_set], loc_profit_fnc))
ps.add(Player('Ynk', [round(x,2) for x in action_set], loc_profit_fnc))
#ps.add(Player('Snk', [round(x,2) for x in action_set], loc_profit_fnc))
#ps.compute_action_profiles()
#print ps.action_profiles[150]
print 'Strategies: ', ps[0].action_set
print 'BR player 0: ', ps[0].best_response_set([0.25, 0.75]).current_best_response
print 'Payoff of 0.25', ps[0].evaluate_payoff(0.25, [0.25, 0.75, 0.75])
print 'Payoff of 0.6', ps[0].evaluate_payoff(0.6, [0.25, 0.75, 0.75])
print 'Payoff of 0.35', ps[0].evaluate_payoff(0.35, [0.25, 0.75, 0.75])

#g = StrategicGame(players=ps, shrink=True, precision = 0.001)
#print 'Equilibrium of location game with 4 players: ', g.fixed_point_of_bestresponse_mapping([0.25,0.75, 0.75, 0.8, 0.8]).fixed_point
	
