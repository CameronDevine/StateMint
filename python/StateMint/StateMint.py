'''
This package provides a function to symbolically determine the differential equation describing the dynamics of a system. As inputs the `Solve` function takes the elemental and constraint equations of a system. These equations must be in the forms specified by Rowell and Wormley in "System Dynamics: An Introduction". A `tutorial <https://github.com/CameronDevine/StateMint/blob/master/tutorial.md>`_ is available which covers how to prepare equations for use with this code. There is also an `example <https://github.com/CameronDevine/StateMint/blob/master/python/Example.ipynb>`_ which covers the details of how to use this code. Convenience functions to convert the symbolic matrices to Numpy objects are also included.

This code can be installed by running `pip install StateMint`, or one of the other interfaces can be used. Available are a Mathematica package, and a web `interface <http://statemint.stmartin.edu/>`_.
'''

import sympy
from sympy.parsing.sympy_parser import parse_expr

t, s = sympy.symbols('t s')
dummy = sympy.symbols('dummy')

names = [
	'Eq',
	'Function',
	'Symbol',
	'Integer',
	'Float',
	'sqrt',
	'exp',
	'log',
	'cos',
	'sin',
	'tan',
	'cot',
	'sec',
	'csc',
	'sinc',
	'asin',
	'acos',
	'atan',
	'asec',
	'acsc',
	'atan2',
	'sinh',
	'cosh',
	'tanh',
	'coth',
	'sech',
	'csch',
	'asinh',
	'acosh',
	'atanh',
	'acoth',
	'asech',
	'acsch',
	'I',
	're',
	'im',
	'Abs',
	'arg',
	'conjugate',
	'ceiling',
	'floor',
	'sign'
]

funcs = dict((name, getattr(sympy, name)) for name in names)

def sympify_vec(data):
	return [parse_expr(el + '(t)', global_dict = funcs) for el in data]

def sympify_eqs(data):
	if len(data) == 0:
		return []
	return [parse_expr('Eq(' + el.replace("'", "(t).diff(t)").replace('=', ',') + ')', global_dict = funcs) for el in data]

def make_matrix(eqs, vars, D = False):
	M = sympy.zeros(len(eqs), len(vars))
	for i in range(len(eqs)):
		for j in range(len(vars)):
			if D:
				M[i,j] = sympy.simplify(sympy.diff(eqs[i].subs(vars[j].diff(t), dummy), dummy))
			else:
				M[i,j] = sympy.simplify(sympy.diff(eqs[i], vars[j]))
	return M

def make_vec(vars):
	return [sympy.sympify(str(v).replace('(t)', '')) for v in vars]

class output:
	'''A container for the resulting differential equation.

	This class is a container in which the output from `StateMint.Solve` is placed. This allows the results of the solution to be easily accessed as members of the class.
	'''

	A = None
	'''sympy.Matrix: The state matrix, :math:`A`.

	This matrix is found in state space formulations of dynamic systems such as, :math:`\dot{x}=Ax+Bu`.
	'''

	B = None
	'''sympy.Matrix: The input matrix, :math:`B`.

	This matrix is found in state space formulations of dynamics systems such as, :math:`\dot{x}=Ax+Bu`.
	'''

	C = None
	'''sympy.Matrix: The output matrix, :math:`C`.

	This matrix is found in a linear output equation of the form, :math:`y=Cx+Du`.
	'''

	D = None
	'''sympy.Matrix: The feedthrough matrix, :math:`D`.

	This matrix is found in a linear output equation of the form, :math:`y=Cx+Du`.
	'''

	E = None
	'''sympy.Matrix: The time derivative input matrix, :math:`E`.

	This matrix is found state space formulations of dynamic systems such as, :math:`\dot{x}=Ax+Bu+E\dot{u}`.
	'''

	F = None
	'''sympy.Matrix: The time derivative feedthrough matrix, :math:`F`.

	This matrix is found in linear output equations of the form, :math:`y=Cx+Du+F\dot{u}`.
	'''

	Bp = None
	'''sympy.Matrix: The input matrix, :math:`B'`.

	This matrix is found in equations such as, :math:`\dot{x}'=Ax'+B'u`, where the time derivative of the input has been removed by modifying the state vector.
	'''

	Dp = None
	'''sympy.Matrix: The feedthrough matrix, :math:`D'`.

	This matrix is found in equations such as, :math:`y=Ax'+D'u`, where the time derivative of the input has been removed by modifying the state vector.
	'''

	TF = None
	'''sympy.Matrix: The transfer function of the system.'''

	StateVec = None
	'''sympy.Matrix: The symbolic state vector :math:`x`.'''

	OutputVec = None
	'''sympy.Matrix: The symbolic output vector :math:`y`.'''

	StateEq = None
	'''sympy.Matrix: The full state equation, :math:`\dot{x}=f(x,y)`.'''

	OutEq = None
	'''sympy.Matrix: The full output equation, :math:`y=h(x,u)`.'''

	InputVec = None
	'''sympy.Matrix: The symbolic input vector :math:`u`.'''

def Solve(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars):
	'''Find the differential equations of a dynamic system from elemental and constraint equations.

	This function takes the input and output variables, along with the state, elemental, and constrain equations. It returns a state space model, along with a transfer function and the state and output equations.

	Args:
		InVars (list of str): A list of the system's input variables.
		StVarElEqns (list of str): A list of state variable elemental equations with the primary variables on the left hand side.
		OtherElEqns (list of str): A list of non state variable elemental equations with the primary variables on the left hand side.
		Constraints (list of str): A list of constraint (compatibility and continuity) equations with the secondary variables on the left hand side.
		OutputVars (list of str): A list of the system's output variables.

	Returns:
		output: The symbolically determined differential equation describing the system.
	'''

	InVars = sympify_vec(InVars)

	OutputVars = sympify_vec(OutputVars)

	StVarElEqns = sympify_eqs(StVarElEqns)

	OtherElEqns = sympify_eqs(OtherElEqns)

	Constraints = sympify_eqs(Constraints)

	StVars = [sympy.integrate(eq.lhs, t) for eq in StVarElEqns]

	PriVars = [eq.lhs for eq in OtherElEqns]

	SecVars = [eq.lhs for eq in Constraints]

	func_subs = dict([(sympy.sympify(str(var).replace('(t)', '')), var) if '(t)' in str(var) else (var, sympy.sympify(str(var) + '(t)')) for var in InVars + StVars + PriVars + SecVars])

	StVarElEqns = [eq.subs(func_subs) for eq in StVarElEqns]

	OtherElEqns = [eq.subs(func_subs) for eq in OtherElEqns]

	StVars = [eq.subs(func_subs) for eq in StVars]

	PriVars = [eq.subs(func_subs) for eq in PriVars]

	SecVars = [eq.subs(func_subs) for eq in SecVars]

	Constraints = [eq.subs(func_subs) for eq in Constraints]

	DConstraints_sub = dict(
		[(const.lhs, const.rhs) for const in Constraints]
		+[(const.lhs.diff(t), const.rhs.diff(t)) for const in Constraints if const.lhs.diff(t) != 0])

	St2 = [sympy.Eq(eq.lhs, eq.rhs.subs(DConstraints_sub)) for eq in StVarElEqns]

	Co2 = [eq.subs(DConstraints_sub) for eq in OtherElEqns]

	E3 = {}
	for eq1 in Co2:
		eq = eq1.copy()
		for eq2 in Co2:
			if eq1 != eq2:
				eq = eq.subs(eq2.lhs, eq2.rhs)
		E3[eq.lhs] = sympy.solve(eq, eq.lhs)[0]

	StateEquation = St2
	_StateEquation = None
	while StateEquation != _StateEquation:
		_StateEquation = StateEquation
		StateEquation = [eq.subs(E3) for eq in StateEquation]

	StateEqsFinal = [sympy.simplify(sympy.solve(eq.doit(), st.diff(t))[0]) for (eq, st) in zip(StateEquation, StVars)]

	OutputSubs = dict([(st.diff(t), eq) for (eq, st) in zip(StateEqsFinal, StVars)])
	OutputSubs.update(DConstraints_sub)
	OutputSubs.update(E3)

	OutputEqsFinal = OutputVars
	_OutputEqsFinal = None
	while OutputEqsFinal != _OutputEqsFinal:
		_OutputEqsFinal = OutputEqsFinal
		OutputEqsFinal = [eq.subs(OutputSubs) for eq in OutputEqsFinal]

	A = make_matrix(StateEqsFinal, StVars)
	B = make_matrix(StateEqsFinal, InVars)
	C = make_matrix(OutputEqsFinal, StVars)
	D = make_matrix(OutputEqsFinal, InVars)
	E = make_matrix(StateEqsFinal, InVars, True)
	F = make_matrix(OutputEqsFinal, InVars, True)

	Bp = A * E + B
	Dp = C * E + D

	TF = sympy.Matrix([C * (s * sympy.eye(A.shape[0]) - A)**-1 * Bp + Dp + F * s]).T

	StVec = make_vec(StVars)
	OutVec = make_vec(OutputVars)
	InVec = make_vec(InVars)
	
	StateEqsFinalMat = sympy.Matrix([StateEqsFinal]).T
	OutputEqsFinalMat = sympy.Matrix([OutputEqsFinal]).T

	result = output()
	result.A = A
	result.B = B
	result.C = C
	result.D = D
	result.E = E
	result.F = F
	result.Bp = Bp
	result.Dp = Dp
	result.TF = TF
	result.StateVec = sympy.Matrix(StVec)
	result.OutputVec = sympy.Matrix(OutVec)
	result.StateEq = StateEqsFinalMat
	result.OutEq = OutputEqsFinalMat
	result.InputVec = sympy.Matrix(InVec)

	return result
