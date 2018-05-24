import numpy as np

class Player(object):
	"""
		class that contains data and methods for a player of a strategic game

		:param: position: an integer valued player identifier (e.g, 1, 2 ,3)
		:param: action_set: a list of the player's actions (a continuous strategy space can be approximated with a grid of values)
		:param: payoff_function: a function that accepts two arguments: player_strategy and other_players_strategy_profile and serves 
						   to compute a player's payoffs from a specific state. The logic for this function is specified by the
						   user, outside of the Player class. Examples are provides in examples.py
		:param: analytic_best_response: if provided, this function is used to calculate the best response set to a profile. The profile (list) is a required argument.
								 If not provided, the best response set is calculated through maximization over all possible actions.
		:param: types: the possible types of the player instance, for bayesian games. the framework uses Harsanyi's formulation of player types in strategic form.
		:param: beliefs: player's beliefs about the distribution of types of his opponents. If provided, a type must be provided as well.
		
		:method: evaluate_payoff: uses the provided payoff_function to return a player's payoff (scalar) from a specific strategy profile. 
		:method: best_response_set: method that returns the best response set (list) against a particular profile from other players. 
							Also writes the output in the current_best_response attribute.
	"""
	def __init__(self, position, action_set, payoff_function, analytic_best_response=None, types=None, beliefs=None):
		self.position = position
		self.action_set = action_set
		self.payoff_function = payoff_function
		self.analytic_best_response = analytic_best_response
		self.types = types
		self.beliefs = beliefs

	def evaluate_payoff(self, player_strategy, other_players_strategy_profile):
		if self.beliefs:
			return self.payoff_function(np.array(player_strategy), np.array(other_players_strategy_profile), self.type, self.beliefs)
		else:
			return self.payoff_function(np.array(player_strategy), np.array(other_players_strategy_profile))

	def best_response_set(self, profile):
		if self.analytic_best_response:
			best_response_set = self.analytic_best_response(profile)
		else:
			possible_set = {strategy:self.evaluate_payoff(strategy, profile) for strategy in self.action_set}
			best_payoff = max(possible_set.values())
			best_response_set = [key for key in possible_set if possible_set[key]==best_payoff]
		self.current_best_response = sorted(best_response_set)
		return self.current_best_response

if __name__ == '__main__':
	main()