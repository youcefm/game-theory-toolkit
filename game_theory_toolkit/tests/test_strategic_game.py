import numpy as np
#from game_theory_toolkit.game import StrategicGame
#from player import Player
import game_theory_toolkit

players ={1: Player(1, [1,2,3], lambda x: x), 2: Player(1, [1,2,3], lambda x: x)}

g = StrategicGame(players=players)
c = g.contingencies()
for el in c:
	print el
