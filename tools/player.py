import numpy as np

class Player(object):
	"""

	"""
	def __init__(self, position, strategies, utility_function):
		self.position = position
		self.strategies = strategies
		self.utility_function = utility_function

	def evaluate_payoff(self, player_strategy, other_players_strategy_profile):
		return self.utility_function(np.array(player_strategy), np.array(other_players_strategy_profile))

	def best_response_set(self, profile):
		possible_set = {strategy:self.evaluate_payoff(strategy, profile) for strategy in self.strategies}
		best_payoff = max(possible_set.values())
		best_response_set = [key for key in possible_set if possible_set[key]==best_payoff]
		return best_response_set

if __name__ == '__main__':
	main()