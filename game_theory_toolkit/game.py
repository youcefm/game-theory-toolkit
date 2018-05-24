import random
import numpy as np
from itertools import product
from scipy.optimize import minimize

class StrategicGame(object):
	"""
		class to model and analyze games in strategic form
	"""

	def __init__(self, players={}, convex_numerical_action_set=True, precision=0.01, max_iter=100, trim_factor=10):
		self.players=players
		self.convex_numerical_action_set=convex_numerical_action_set
		self.precision=precision
		self.max_iter=max_iter
		self.trim_factor=trim_factor

	def fixed_point_of_bestresponse_mapping(self, seed, point_selection_type='random'):
		profile = seed
		delta = 1.0/self.precision
		itr = 0
		N = len(self.players) # number of players
		step = np.log2(N)

		while  delta > self.precision and itr < self.max_iter:
			new_profile = []
			for player in self.players:
				if point_selection_type=='random':
					br = random.choice(self.players[player].best_response_set([x for i,x in enumerate(profile) if i!=player-1])) # choose one in the set
				elif point_selection_type=='min':
					br = np.min(self.players[player].best_response_set([x for i,x in enumerate(profile) if i!=player-1])) # choose minimum of the set
				elif point_selection_type=='max':
					br = np.max(self.players[player].best_response_set([x for i,x in enumerate(profile) if i!=player-1])) # choose maximum of the set
				elif point_selection_type=='mean':
					br = np.mean(self.players[player].best_response_set([x for i,x in enumerate(profile) if i!=player-1])) # choose mean of the set
				if self.convex_numerical_action_set:
					new_strategy = ((step-1)*profile[player-1] + 1.0*(br))/step 						 # works for actions defined on the real line
				else:
					new_strategy = br 																		 # need to think about this more
				new_profile.append(new_strategy)

			if self.convex_numerical_action_set:
				new_delta = sum((np.array(new_profile) - np.array(profile))**2)**0.5
			else:
				new_delta = 100*sum(np.array(new_profile) != np.array(profile))
			print 'Current Delta: ', new_delta

			if new_delta - delta >= -0.5*self.precision: # perturbe strategies if optimization gets stuck
				print "---- Add preturbation to unstuck convergence ----"
				if self.convex_numerical_action_set:
					new_profile = (np.ones(len(new_profile)) + np.random.normal(0, 0.1, len(new_profile)))*np.array(new_profile)
				else:
					new_profile = [random.choice(self.players[player].action_set) for player in self.players]
			delta = new_delta
			itr+=1
 			profile=list(new_profile)
 		if itr == self.max_iter:
 			print 'WARNING: Reached max number of iterations, with a delta of {x} times above precision'.format(x=delta/self.precision)
 		self.fixed_point = new_profile

 	def contingencies(self):
 		p = product(*[self.players[player].action_set for player in self.players])
 		contingencies = []
 		for el in p:
 			contingencies.append(el)
 		return contingencies

 	def UniformlyRandomStrategy(self):
 		p = product(*[1.0/len(self.players[player].action_set)*np.ones(len(self.players[player].action_set)) for player in self.players])
 		l = []
 		for el in p:
 			l.append(el)
 		return l

 	def MixedStrategyProfile(self, mixed_strategies):
 		return


 	def liapunov_value(self, profile):
 		v_profile = 0
 		for player in self.players:
 			g_player = 0
 			position = self.players[player].position -1
 			m_profile =  self.players[player].evaluate_payoff(profile[position], np.delete(profile, position))
 			for strategy in self.players[player].action_set:
 				m_strategy = self.players[player].evaluate_payoff(strategy, np.delete(profile, position))
 				g_player += max((m_strategy- m_profile)**2, 0)
 			v_profile += g_player
 		return v_profile

 	def nash_equilibria(self, seed):
 		return minimize(self.liapunov_value, seed, method='Nelder-Mead', 
 			options={'disp': True})

class EvolutionaryGame(object):
	"""
 		class to model and analyze evolutionary games when interactions are within a single population
 	"""
	def __init__(self, player, initial_population_distribution = []):
		self.player = player
		self.initial_population_distribution = initial_population_distribution
		self.current_population_distribution = initial_population_distribution

	def compute_current_fitness(self):
		expected_payoffs = []
		for strategy1 in self.player.action_set:
			expected_payoff = 0
			for index, strategy2 in enumerate(self.player.action_set):
				v = self.player.evaluate_payoff(strategy1, [strategy2])
				expected_payoff += v*self.current_population_distribution[index]
			expected_payoffs.append(expected_payoff)

		self.current_fitness = expected_payoffs

	def replicator_dynamics_step(self):
		self.compute_current_fitness()
		avg_fitness = sum(np.array(self.current_fitness)*np.array(self.current_population_distribution))
		population_change = np.array(self.current_population_distribution)*(np.array(self.current_fitness) - avg_fitness)
		new_population_distribution = self.current_population_distribution + population_change
		self.current_population_distribution = new_population_distribution


class TwoPlayerEvolutionaryGame(object):
 	"""
 		class to model and analyze evolutionary games when interactions are between two distinct populations
 	"""
	def __init__(self, player1, player2, initial_population_distributions = {}):
		self.player1 = player1
		self.player2 = player2
		self.initial_population_distributions = initial_population_distributions
		self.current_population_distributions = initial_population_distributions

	def compute_current_fitness(self):
		expected_payoffs = {1: [], 2: []} 
		for strategy1 in self.player1.action_set:
			expected_payoff = 0
			for index, strategy2 in enumerate(self.player2.action_set):
				v = self.player1.evaluate_payoff(strategy1, [strategy2])
				expected_payoff += v*self.current_population_distributions[2][index]
			expected_payoffs[1].append(expected_payoff)

		for strategy2 in self.player2.action_set:
			expected_payoff = 0
			for index, strategy1 in enumerate(self.player1.action_set):
				v = self.player2.evaluate_payoff(strategy2, [strategy1])
				expected_payoff += v*self.current_population_distributions[1][index]
			expected_payoffs[2].append(expected_payoff)
		self.current_fitness = expected_payoffs

	def replicator_dynamics_step(self):
		self.compute_current_fitness()
		avg_fitness = {1: sum(np.array(self.current_fitness[1])*np.array(self.current_population_distributions[1])),
		2: sum(np.array(self.current_fitness[2])*np.array(self.current_population_distributions[2]))}
		population_change = {1: np.array(self.current_population_distributions[1])*(np.array(self.current_fitness[1]) - avg_fitness[1]),
		2: np.array(self.current_population_distributions[2])*(np.array(self.current_fitness[2]) - avg_fitness[2])}
		new_population_distributions = {1: self.current_population_distributions[1] + population_change[1],
		2: self.current_population_distributions[2] + population_change[2]}
		self.current_population_distributions = new_population_distributions


if __name__ == '__main__':
	main()