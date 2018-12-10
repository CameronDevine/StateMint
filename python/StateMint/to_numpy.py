'''
This module provides convenience functions for turning symbolic matrices into Numpy matrices for simulation and analysis.
'''

import numpy as np
from sympy import symbols

def array(data, values = {}):
	'''Convert a symbolic matrix to a Numpy array.

	Converts a given symbolic matrix, most likely returned in the output of `StateMint.Solve`, into a Numpy array.

	Args:
		data (sympy.Matrix): The symbolic matrix to convert to a Numpy array.
		values (dict of str: float, optional): The values to replace each symbolic variable with in a dictionary with the key as a string of the variable name, and the value as the number to replace it with

	Returns:
		numpy.ndarray: A Numpy array of the matrix using the values given
	'''
	subs = {}
	for val in values:
		if val is str:
			subs[symbols(val)] = values[val]
		else:
			subs[val] = values[val]
	return np.array(data.subs(subs)).astype(np.float64)

def matrix(data, values = {}):
	'''Convert a symbolic matrix to a Numpy matrix.

	Converts a given symbolic matrix, most likely returned in the output of `StateMint.Solve`, into a Numpy matrix.

	Args:
		data (sympy.Matrix): The symbolic matrix to convert to a Numpy matrix.
		values (dict of str: float, optional): The values to replace each symbolic variable with in a dictionary with the key as a string of the variable name, and the value as the number to replace it with

	Returns:
		numpy.matrix: A Numpy matrix using the values given
	'''
	subs = {}
	for val in values:
		if val is str:
			subs[symbols(val)] = values[val]
		else:
			subs[val] = values[val]
	return np.matrix(data.subs(subs)).astype(np.float64)
