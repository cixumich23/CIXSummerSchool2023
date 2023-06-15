import random
from itertools import product

import gurobipy as gp
from gurobipy import GRB

try:
    # Try starting the environment
    env = gp.Env(empty=True)
    env.start()

except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ': ' + str(e))

except AttributeError:
    print('Encountered an attribute error')