import numpy as np

class Player(object):
	"""
		class that contains data and methods for a player of a strategic game
		the needed inputs to instantiate a player are:
		-position: an integer valued player identifier (e.g, 1, 2 ,3)
		-strategies: a list of the player's strategies (a continuous strategy space can be approximated with a grid of values)
		-payoff_function: a method that accepets two arguments: player_strategy and other_players_strategy_profile and serves 
						   to compute a player's payoffs from a specific state. The logic for this function is specified by the
						   user, outside of the Player class. Examples are provides in examples.py
		-analytic_best_response: if provided, this method is used to calculate the best response set to a profile. The profile (list) is a required argument.
								 If not provided, the best response set is calculated through maximization over all possible profiles.
		-types: the possible types of the player instance, for bayesian games. the framework uses Harsanyi's formulation of player types in strategic form.
		-beliefs: player's beliefs about the distribution of types of his opponents. If provided, a type must be provided as well.
		
		methods:
		-evaluate_payoff: uses the provided payoff_function to return a player's payoff (scalar) from a specific strategy profile. 
		-best_response_set: method that returns the best response set (list) against a particular profile from other players. 
							Also writes the output in the current_best_response attribute.
	"""
	def __init__(self, position, strategies, payoff_function, analytic_best_response=None, types=None, beliefs=None):
		self.position = position
		self.strategies = strategies
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
			possible_set = {strategy:self.evaluate_payoff(strategy, profile) for strategy in self.strategies}
			best_payoff = max(possible_set.values())
			best_response_set = [key for key in possible_set if possible_set[key]==best_payoff]
		self.current_best_response = sorted(best_response_set)
		return self.current_best_response

if __name__ == '__main__':
	main()