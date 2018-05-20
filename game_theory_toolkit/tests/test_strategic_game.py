import numpy as np
#from ..game import StrategicGame
#from ..player import Player
#import game_theory_toolkit

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from game import StrategicGame
from player import Player

s = [1,2,3]
p =[1.0/3, 1.0/3, 1.0/3]
players ={1: Player(1, p, lambda x: x), 2: Player(1, p, lambda x: x)}

g = StrategicGame(players=players)
print 'What is this object:', str(g)
print 'New function: ', g.UniformlyRandomStrategy()
c = g.contingencies()
l = []
for el in c:
	l.append(list(el))
print 'Manual calculation: ', l
print l[1][1]
