import numpy as np
from itertools import product

class Player(object):
	"""
		class that contains data and methods for a player of a strategic game

		:param: name: 						player identifier (e.g, 1, 2 ,3, 'mo', 'Al')

		:param: action_set: 				a list of the player's actions (a continuous 
			                				strategy space can be approximated with a grid of values)

		:param: payoff_function: 			a function that accepts two arguments: player_strategy 
		                         			and other_players_strategy_profile and serves 
						         			to compute a player's payoffs from a specific state. 
						         			The logic for this function is specified by the
						         			user, outside of the Player class. Examples are provides in examples.py

		:param: analytic_best_response: 	if provided, this function is used to calculate the best response set to a profile. 
		                                	The profile (list) is a required argument. If not provided, the best response set is 
		                                	calculated through maximization over all possible actions.

		:param: types: 						the possible types of the player instance, for bayesian games. 
					   						The framework uses Harsanyi's formulation of player types in strategic form.

		:param: beliefs: 					player's beliefs about the distribution of types of his opponents. 
		                 					If provided, a type must be provided as well.
		
		:method: evaluate_payoff: 			uses the provided payoff_function to return a player's payoff (scalar) 
		                          			from a specific strategy profile. 

		:method: best_response_set: 		method that returns the best response set (list) against a particular 
		                            		profile from other players. Also writes the output in the current_best_response attribute.
	"""
	def __init__(self, name, action_set, payoff_function,
				 analytic_best_response=None, types=None, beliefs=None):
		self.name = name
		self.action_set = action_set
		self.payoff_function = payoff_function
		self.analytic_best_response = analytic_best_response
		self.types = types
		self.beliefs = beliefs
		self.mixed_strategy = (1.0/len(action_set))*np.ones(len(action_set))

	def evaluate_payoff(self, player_strategy,
						other_players_strategy_profile, **kwargs):

		return self.payoff_function(player_strategy, other_players_strategy_profile, **kwargs)

	def best_response_set(self, profile, **kwargs):
		if self.analytic_best_response:
			best_response_set = self.analytic_best_response(profile, **kwargs)
		else:
			possible_set = {strategy:self.evaluate_payoff(strategy, profile, **kwargs) for strategy in self.action_set}
			best_payoff = max(possible_set.values())
			best_response_set = [key for key in possible_set if possible_set[key]==best_payoff]
		self.current_best_response = sorted(best_response_set)
		return self


class PlayerSet(dict):
	"""
		Dict that holds set of player instances. Initiates to an empty dict.

		:method: add: 						to add a player to the set. Can add a Player() instance, 
						  					or pass parameters and let the method create the instance 
						  					by providing the params in a dict.

		:method: remove: 					remove a player by providing the name of the player to remove (wrapper around pop() method).

		:method: compute_action_profiles: 	a list of all action profiles possible within the player set
	"""

	def __init__(self, initial_set={}):
		super(PlayerSet, self).__init__(initial_set)
		self.num_players = 0
		self.index = 0

	def add(self, player=None, position=None, **kwargs):

		if position:
			index = position
		else:
			index = self.index

		if player:
			self[index] = player
			player.position = index
		else:
			self[self.index] = Player(**kwargs)
			self[self.index].position = self.index
		self.num_players += 1
		self.index = self.num_players

	def remove(self, position):

		self.pop(position)
		self.num_players = self.num_players - 1
		self.index = self.num_players
		for key in self:
			if key > position:
				self[key].position = key -1
				self[key -1] = self[key]
				self.pop(key)

	def compute_action_profiles(self):

		p = product(*[self[player].action_set for player in self])
 		contingencies = []
 		for el in p:
 			contingencies.append(list(el))
 		self.action_profiles = contingencies
 		return self

 	def mixed_strategy_profile(self):
 		self.msp = [self[player].mixed_strategy for player in self]
 		return self

 	def compute_profile_distribution(self):

 		self.mixed_strategy_profile()
 		p = product(*self.msp)
 		contingencies = []
 		for el in p:
 			proba = np.prod(list(el))
 			contingencies.append(proba)
 		self.profile_distribution = contingencies
 		return self

	def expected_payoff(self, player_position):
		p = self[player_position]
		v = sum(np.array(self.profile_distribution)*\
			np.fromiter((p.evaluate_payoff(profile[p.position], 
								np.delete(profile, p.position)) for profile in np.array(self.action_profiles)), 
						np.array(self.action_profiles).dtype, 
						count=len(self.action_profiles)
						)
			)
		return v


if __name__ == '__main__':
	main()