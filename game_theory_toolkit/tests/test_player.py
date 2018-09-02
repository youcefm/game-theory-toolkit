import numpy as np
from game_theory_toolkit.player import *

def matching_penny_utility(strategy, profile):
	heads_count, tails_count = 0,0
	for value in profile:
		if value=='H':
			heads_count+=1
		elif value=='T':
			tails_count+=1
	heads_payoff = heads_count - tails_count
	if strategy == 'H':
		return heads_payoff
	else:
		return - heads_payoff

def quadratique_utility(strategy, profile):
	return np.mean(profile)*strategy - strategy**2 

def constant_utility(strategy, profile):
	return 5

def cutoff_utility(strategy, profile):
	if strategy<=np.min(profile):
		return strategy
	else:
		return 0

class TestPlayerMethods(object):

	def evaluate_payoff_test_template(self, strategy_set, utility_fnc, profile_1, profile_2):
		player = Player(1, strategy_set, utility_fnc)
		actual = (player.evaluate_payoff(profile_1[0], profile_1[1]), player.evaluate_payoff(profile_2[0], profile_2[1]))
		return actual

	def best_response_set_test_template(self, strategy_set, utility_fnc, profile_1, profile_2, analytic_best_response = None):
		player = Player(1, strategy_set, utility_fnc, analytic_best_response)
		actual = (sorted(player.best_response_set(profile_1).current_best_response), 
			sorted(player.best_response_set(profile_2).current_best_response))
		return actual

	def test_evaluate_payoff_binary_action(self):
		actual = self.evaluate_payoff_test_template(['H', 'T'], matching_penny_utility, ['H', ['H', 'H', 'T']], ['T', ['H', 'H', 'H', 'T']])
		expected = (1, -2)
		assert actual == expected

	def test_evaluate_payoff_quadratic_utility(self):
		actual = self.evaluate_payoff_test_template(range(0, 100, 1), quadratique_utility, [2 ,[1,1,1]], [2 ,[4,0,8]])
		expected = (-2, 4)
		assert actual == expected

	def test_evaluate_payoff_constant_utility(self):
		actual = self.evaluate_payoff_test_template(range(0, 100, 1), constant_utility, [2 ,[1,1,1]], [2 ,[4,0,8]])
		expected = (5,5)
		assert actual == expected

	def test_cutoff_payoff(self):
		actual = self.evaluate_payoff_test_template(range(0, 100, 1), cutoff_utility, [0.5 ,[0.5000,1,1]], [1.23 ,[1.225005,0,8]])
		expected = (0.5, 0)
		assert actual == expected

	def test_best_response_set_binary_action(self):
		actual = self.best_response_set_test_template(['H', 'T'], matching_penny_utility, ['H', 'H', 'T'], ['H', 'H', 'T', 'T'])
		expected = (['H'], ['H', 'T'])
		assert actual == expected

	def test_best_response_set_quadratic_utility(self):
		actual = self.best_response_set_test_template(np.arange(0, 20, 0.5), quadratique_utility, [10,10,10], [2.5,2.5,2.5])
		expected = ([5], [1.0, 1.5])
		assert actual == expected

	def test_best_response_set_constant_utility(self):
		strategy_set = np.arange(0,2,0.5)
		actual = self.best_response_set_test_template(strategy_set, constant_utility, [10,10,10], [2.5,2.5,2.5])
		expected = (sorted(list(strategy_set)), sorted(list(strategy_set)))
		assert actual == expected

	def test_best_response_set_cutoff_utility(self):
		actual = self.best_response_set_test_template(np.arange(0,5, 0.1), cutoff_utility, [0.4, 1, 1.99994], [2.444, 0.1000003, 2])
		expected = ([0.4], [0.1])
		assert actual == expected

	def test_analytic_best_response_has_priority(self):
		actual = self.best_response_set_test_template(np.arange(0,5, 0.1), cutoff_utility, [0.4, 1, 1.99994], [2.444, 0.1000003, 2], 
			analytic_best_response= lambda x: [5])
		expected = ([5], [5])
		assert actual == expected





