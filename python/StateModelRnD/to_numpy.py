import numpy as np
from sympy import symbols

def array(data, values = {}):
	subs = {}
	for val in values:
		if val is str:
			subs[symbols(val)] = values[val]
		else:
			subs[val] = values[val]
	return np.array(data.subs(subs)).astype(np.float64)

def matrix(data, values = {}):
	subs = {}
	for val in values:
		if val is str:
			subs[symbols(val)] = values[val]
		else:
			subs[val] = values[val]
	return np.matrix(data.subs(subs)).astype(np.float64)
