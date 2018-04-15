## Game Theory toolkit Examples
from itertools import product
import random
import numpy as np
from tools.player import Player
from tools.game import BaseGame

### Compute best response against a fixed profile for public goods utility function:
param=6
def quadratic_utility(strategy, profile, param=param):
	return param*(strategy+sum(profile))**0.5 - strategy

# analytic best response function : 
# FOC is param*0.5/(strategy + sum(profile))**0.5 - 1=0  and strategy >=0 --> strategy = max(0,(param*0.5)**2 - sum(profile))

profile = [0,1,2,3]
print 'Analytic Best Response:', max(0,(param*0.5)**2 - sum(np.array(profile)))

ready_player_one = Player(1, np.arange(0,20, 0.1), utility_function=quadratic_utility)

print ready_player_one.best_response_set(profile)

### Define general matching pennies utility function and compute best response against fixed profile:

def matching_penny_utility(strategy, profile):
	heads_count, tails_count = 0,0
	for value in profile:
		if value=='H':
			heads_count+=1
		elif value=='T':
			tails_count+=1
	heads_payoff = heads_count - tails_count
	if strategy == 'H':
		return heads_count
	else:
		return - heads_count

ready_player_two = Player(2, ['H', 'T'], utility_function=matching_penny_utility)

print ready_player_two.best_response_set(['H', 'H', 'H', 'H', 'H', 'T', 'T', 'T'])

### Define and solve a 2 player Cournot oligopoly game

# Profit function:
a,b,c=50,1,2
def profit_fnc(my_quantity, others_quantities, a=a, b=b, c=c, cost_type = 'quadratic'):
	price = max(0,a- (my_quantity + sum(others_quantities))/b)
	if cost_type == 'quadratic':
		return price*my_quantity - c*my_quantity**2 
	elif cost_type == 'linear':
		return price*my_quantity - c*my_quantity
	else: 
		return price*my_quantity - c*my_quantity

def cournot_best_response_function(profile, a=a,b=b,c=c, cost_type = 'quadratic'):
	if cost_type=='quadratic':
		return (a*b - sum(profile))/(2.0*(1 + c*b))
	elif cost_type == 'linear':
		return (b*(a -c) - sum(profile))/2.0
	else: 
		return (b*(a -c) - sum(profile))/2.0

player = Player(1, np.arange(0,a*b,0.01), profit_fnc, cournot_best_response_function)
print 'Analytic Best response example: ', player.best_response_set([1,5,6,4])

# Create player instances
players = {}
N = 3
for n in range(1, N+1):
	players[n] = Player(n, np.arange(0,a*b,0.01), profit_fnc)

# Analytic solution (symmetric), for comparison
# FOC (quadratic cost) : a - (2*my_quantity + (n-1)*my_quantity)/b  - 2*c*my_quantity = 0 --> my_quantity = a/(n+1+2*c*b)
# FOC (linear cost): a - (2*my_quantity + (n-1)*my_quantity)/b - c = 0                    --> my_quantity =(a-c)*b/(n+1)
print 'Analytic Solution for Linear Cost (N={N}):'.format(N=N), 1.0*(a-c)*b/(N+1)
print 'Analytic Solution for Quadratic Cost (N={N})'.format(N=N), 1.0*a*b/(N+1+2*c*b)

cournot_game = BaseGame()
cournot_game.players=players
cournot_game.find_fixed_point_of_bestresponse_mapping(seed=np.random.randint(0, a*b, N))
print 'Equilibrium is: ', cournot_game.fixed_point

# Game Theory Toolkit solution using iterated best response idea
# q= np.random.randint(0, a*b, 1)
# eps = 100
# itr = 0
# max_itr = 20
# while eps> 0.01 and itr < max_itr:
# 	q_new = np.mean(players[1].best_response_set([np.mean(players[2].best_response_set([q]))]))
# 	eps = abs(q_new-q)
# 	print 'iteration:', itr
# 	print 'previous strategy:', q
# 	print 'new strategy:', q_new
# 	q=q_new
# 	itr+=1



