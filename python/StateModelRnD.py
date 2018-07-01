# Import everything from the sympy library.
from sympy import *

p = False

# Define the symbols t and s.
t, s = symbols('t s')
# Define a dummy variable named dummy.
dummy = symbols('dummy')

def sympify_vec(string):
	return [sympify(el + '(t)') for el in string.split(',')]

def sympify_eqs(string):
	if len(string) == 0:
		return []
	return [sympify('Eq(' + el.replace('=', ',') + ')') for el in string.replace('\'', '(t).diff(t)').split(',')]

def make_matrix(eqs, vars, D = False):
	M = zeros(len(eqs), len(vars))
	for i in range(len(eqs)):
		for j in range(len(vars)):
			if D:
				M[i,j] = simplify(diff(eqs[i].subs(vars[j].diff(t), dummy), dummy))
			else:
				M[i,j] = simplify(diff(eqs[i], vars[j]))
	return M

def make_vec(vars):
	return [sympify(str(v).replace('(t)', '')) for v in vars]

# The main find state space model function.
def find(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars):
	# InVars: A string of input variable seperated by spaces.
	# StVarElEqns: A string of state variable elemental equations seperated by commas, using ' for derivative, and = for equality.
	# OtherElEqns: A string of non-state elemental equations seperated by commas, using ' for derivative, and = for equality.
	# Constrains: A string of constraint (continuity and compatability) equations seperated by commas.
	# 
	InVars = sympify_vec(InVars)

	OutputVars = sympify_vec(OutputVars)

	StVarElEqns = sympify_eqs(StVarElEqns)

	OtherElEqns = sympify_eqs(OtherElEqns)

	Constraints = sympify_eqs(Constraints)

	#print "Symbolic Expressions Created"

	StVars = [integrate(eq.lhs, t) for eq in StVarElEqns]

	PriVars = [eq.lhs for eq in OtherElEqns]

	SecVars = [eq.lhs for eq in Constraints]

	#print "Variable Collected"

	func_subs = dict([(sympify(str(var).replace('(t)', '')), var) if '(t)' in str(var) else (var, sympify(str(var) + '(t)')) for var in InVars + StVars + PriVars + SecVars])

	StVarElEqns = [eq.subs(func_subs) for eq in StVarElEqns]

	OtherElEqns = [eq.subs(func_subs) for eq in OtherElEqns]

	StVars = [eq.subs(func_subs) for eq in StVars]

	PriVars = [eq.subs(func_subs) for eq in PriVars]

	SecVars = [eq.subs(func_subs) for eq in SecVars]

	#print "Functions Created"

	Constraints = [eq.subs(func_subs) for eq in Constraints]

	DConstraints_sub = dict(
		[(const.lhs, const.rhs) for const in Constraints]
		+[(const.lhs.diff(t), const.rhs.diff(t)) for const in Constraints if const.lhs.diff(t) != 0])

	St2 = [Eq(eq.lhs, eq.rhs.subs(DConstraints_sub)) for eq in StVarElEqns]

	Co2 = [eq.subs(DConstraints_sub) for eq in OtherElEqns]

	E3 = {}
	for eq1 in Co2:
		eq = eq1.copy()
		for eq2 in Co2:
			if eq1 != eq2:
				eq = eq.subs(eq2.lhs, eq2.rhs)
		E3[eq.lhs] = solve(eq, eq.lhs)[0]

	StateEquation = St2
	_StateEquation = None
	while StateEquation != _StateEquation:
		_StateEquation = StateEquation
		StateEquation = [eq.subs(E3) for eq in StateEquation]

	StateEqsFinal = [simplify(solve(eq.doit(), st.diff(t))[0]) for (eq, st) in zip(StateEquation, StVars)]

	OutputSubs = dict([(st.diff(t), eq) for (eq, st) in zip(StateEqsFinal, StVars)])
	OutputSubs.update(DConstraints_sub)
	OutputSubs.update(E3)

	OutputEqsFinal = OutputVars
	_OutputEqsFinal = None
	while OutputEqsFinal != _OutputEqsFinal:
		_OutputEqsFinal = OutputEqsFinal
		OutputEqsFinal = [eq.subs(OutputSubs) for eq in OutputEqsFinal]

	#print "Equations Solved"

	A = make_matrix(StateEqsFinal, StVars)
	B = make_matrix(StateEqsFinal, InVars)
	C = make_matrix(OutputEqsFinal, StVars)
	D = make_matrix(OutputEqsFinal, InVars)
	E = make_matrix(StateEqsFinal, InVars, True)
	F = make_matrix(OutputEqsFinal, InVars, True)

	Bp = A * E + B
	Dp = C * E + D

	#print "Matricies Created"

	TF = Matrix([C * (s * eye(A.shape[0]) - A)**-1 * Bp + Dp + F * s]).T

	#print "Transfer Function Found"

	StVec = make_vec(StVars)
	OutVec = make_vec(OutputVars)
	InVec = make_vec(InVars)
	
	StateEqsFinalMat = Matrix([StateEqsFinal]).T
	OutputEqsFinalMat = Matrix([OutputEqsFinal]).T

	return {'A': A, 'B': B, 'C': C, 'D': D, 'E': E, 'F': F, 'Bp': Bp, 'Dp': Dp, 'TF': TF, 'StateVec': StVec, 'OutputVec': OutVec, 'StateEq': StateEqsFinalMat, 'OutEq': OutputEqsFinalMat, 'InputVec': InVec}
