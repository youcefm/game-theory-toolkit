import numpy as np
from tools.game import StrategicGame

players ={1: Player(1, [1,2,3], lambda x: x), 2: Player(1, [1,2,3], lambda x: x)}

g = StrategicGame(players=players)
c = g.contingencies()
for el in c:
	print el
