import random
import numpy as np
from itertools import product
from scipy.optimize import minimize

class StrategicGame(object):
	"""
		class to define games in strategic form
	"""

	def __init__(self, players=None, convex_numerical_strategy_set=True, precision=0.01, max_iter=100, trim_factor=10):
		self.players=players
		self.convex_numerical_strategy_set=convex_numerical_strategy_set
		self.precision=precision
		self.max_iter=max_iter
		self.trim_factor=trim_factor

	def fixed_point_of_bestresponse_mapping(self, seed, point_selection_type='random'):
		profile = seed
		delta = 1.0/self.precision
		itr = 0
		N = len(self.players) # number of players

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
				if self.convex_numerical_strategy_set:
					new_strategy = (1.0*(N-2)*profile[player-1] + 1.0*(br))/(N-1) 						 # works for strategies defined on the real line
				else:
					new_strategy = br 																		 # need to think about this more
				new_profile.append(new_strategy)


			delta = sum((np.array(new_profile) - np.array(profile))**2)**0.5
			itr+=1
 			profile=list(new_profile)
 		if itr == self.max_iter:
 			print 'WARNING: Reached max number of iterations, with a delta of {x} times above precision'.format(x=delta/self.precision)
 		self.fixed_point = new_profile

 	def contingencies(self):
 		return product(*[self.players[player].strategies for player in self.players])




 	def liapunov_value(self, profile):
 		v_profile = 0
 		for player in self.players:
 			g_player = 0
 			position = self.players[player].position -1
 			m_profile =  self.players[player].evaluate_payoff(profile[position], np.delete(profile, position))
 			for strategy in self.players[player].strategies:
 				m_strategy = self.players[player].evaluate_payoff(strategy, np.delete(profile, position))
 				g_player += max((m_strategy- m_profile)**2, 0)
 			v_profile += g_player
 		return v_profile

 	def nash_equilibria(self, seed):
 		return minimize(self.liapunov_value, seed, method='Nelder-Mead', 
 			options={'disp': True})




if __name__ == '__main__':
	main()