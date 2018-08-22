import numpy as np
from sympy import symbols

def array(data, values = {}):
	'''
	Converts a given symbolic matrix, most likely from :meth:`StateModelRnD.output`, into a Numpy array.

	:param data: The symbolic matrix to convert to a Numpy array
	:param values: The values to replace each symbolic variable with in a dictionary with the key as a string of the variable name, and the value as the number to replace it with
	:type data: sympy.Matrix
	:type values: dict
	:returns: A Numpy array of the matrix using the values given
	:rtype: numpy.ndarray
	'''
	subs = {}
	for val in values:
		if val is str:
			subs[symbols(val)] = values[val]
		else:
			subs[val] = values[val]
	return np.array(data.subs(subs)).astype(np.float64)

def matrix(data, values = {}):
	'''
	Converts a given symbolic matrix, most likely from :meth:`StateModelRnD.output`, into a Numpy matrix.

	:param data: The symbolic matrix to convert to a Numpy matrix
	:param values: The values to replace each symbolic variable with in a dictionary with the key as a string of the variable name, and the value as the number to replace it with
	:type data: sympy.Matrix
	:type values: dict
	:returns: A Numpy matrix of the symbolic matrix using the values given
	:rtype: numpy.matrix
	'''
	subs = {}
	for val in values:
		if val is str:
			subs[symbols(val)] = values[val]
		else:
			subs[val] = values[val]
	return np.matrix(data.subs(subs)).astype(np.float64)
