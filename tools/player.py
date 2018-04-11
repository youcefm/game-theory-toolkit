import numpy as np

class Player(object):
	"""
		class that contains data and methods for a player of a strategic game
		the needed inputs to instantiate a player are:
		-position: an integer valued player identifier (e.g, 1, 2 ,3)
		-strategies: a list of the player's strategies (a continuous strategy space can be approximated with a grid of values)
		-utility_function: a method that accepets two arguments: player_strategy and other_players_strategy_profile and serves 
						   to compute a player's payoffs from a specific state. The logic for this function is specified by the
						   user, outside of the Player class. Examples are provides in examples.py
		-analytic_best_response: if provided, this method is used to calculate the best response set to a profile. The profile (list) is a required argument.
								 If not provided, the best response set is calculated through maximization over all possible profiles.
		methods:
		-evaluate_payoff: uses the provided utility_function to return a player's payoff (scalar) from a specific strategy profile 
		-best_response_set: method that returns the best response set (list) against a particular profile from other players
	"""
	def __init__(self, position, strategies, utility_function, analytic_best_response=None):
		self.position = position
		self.strategies = strategies
		self.utility_function = utility_function
		self.analytic_best_response = analytic_best_response

	def evaluate_payoff(self, player_strategy, other_players_strategy_profile):
		return self.utility_function(np.array(player_strategy), np.array(other_players_strategy_profile))

	def best_response_set(self, profile):
		if self.analytic_best_response:
			best_response_set = self.analytic_best_response(profile)
		else:
			possible_set = {strategy:self.evaluate_payoff(strategy, profile) for strategy in self.strategies}
			best_payoff = max(possible_set.values())
			best_response_set = [key for key in possible_set if possible_set[key]==best_payoff]
		return best_response_set

if __name__ == '__main__':
	main()