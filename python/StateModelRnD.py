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
	if p: print 'InVars:\n', InVars

	OutputVars = sympify_vec(OutputVars)
	if p: print 'OutputVars:\n', OutputVars

	StVarElEqns = sympify_eqs(StVarElEqns)
	if p: print 'StVarElEqns:\n', StVarElEqns

	OtherElEqns = sympify_eqs(OtherElEqns)
	if p: print 'OtherElEqns:\n', OtherElEqns

	Constraints = sympify_eqs(Constraints)
	if p: print 'Constraints:\n', Constraints

	#print "Symbolic Expressions Created"

	StVars = [integrate(eq.lhs, t) for eq in StVarElEqns]
	if p: print 'StVars:\n', StVars

	PriVars = [eq.lhs for eq in OtherElEqns]
	if p: print 'PriVars:\n', PriVars

	SecVars = [eq.lhs for eq in Constraints]
	if p: print 'SecVars:\n', SecVars

	#print "Variable Collected"

	func_subs = dict([(sympify(str(var).replace('(t)', '')), var) if '(t)' in str(var) else (var, sympify(str(var) + '(t)')) for var in InVars + StVars + PriVars + SecVars])
	if p: print 'func_subs:\n', func_subs

	StVarElEqns = [eq.subs(func_subs) for eq in StVarElEqns]
	if p: print 'StVarElEqns:\n', StVarElEqns

	OtherElEqns = [eq.subs(func_subs) for eq in OtherElEqns]
	if p: print 'OtherElEqns:\n', OtherElEqns

	StVars = [eq.subs(func_subs) for eq in StVars]
	if p: print 'StVars:\n', StVars

	PriVars = [eq.subs(func_subs) for eq in PriVars]
	if p: print 'PriVars:\n', PriVars

	SecVars = [eq.subs(func_subs) for eq in SecVars]
	if p: print 'SecVars:\n', SecVars

	#print "Functions Created"

	Constraints = [eq.subs(func_subs) for eq in Constraints]
	if p: print 'Constraints:\n', Constraints

	DConstraints_sub = dict(
		[(const.lhs, const.rhs) for const in Constraints]
		+[(const.lhs.diff(t), const.rhs.diff(t)) for const in Constraints if const.lhs.diff(t) != 0])
	if p: print 'DConstraints_sub:\n', DConstraints_sub

	St2 = [Eq(eq.lhs, eq.rhs.subs(DConstraints_sub)) for eq in StVarElEqns]
	if p: print 'St2:\n', St2

	Co2 = [eq.subs(DConstraints_sub) for eq in OtherElEqns]
	if p: print 'Co2:\n', Co2

	E3 = {}
	for eq1 in Co2:
		eq = eq1.copy()
		for eq2 in Co2:
			if eq1 != eq2:
				eq = eq.subs(eq2.lhs, eq2.rhs)
		E3[eq.lhs] = solve(eq, eq.lhs)[0]
	if p: print 'E3:\n', E3

	StateEquation = St2
	_StateEquation = None
	while StateEquation != _StateEquation:
		_StateEquation = StateEquation
		StateEquation = [eq.subs(E3) for eq in StateEquation]
	if p: print 'StateEquation:\n', StateEquation

	StateEqsFinal = [simplify(solve(eq.doit(), st.diff(t))[0]) for (eq, st) in zip(StateEquation, StVars)]
	if p: print 'StateEqsFinal:\n', StateEqsFinal

	OutputSubs = dict([(st.diff(t), eq) for (eq, st) in zip(StateEqsFinal, StVars)])
	OutputSubs.update(DConstraints_sub)
	OutputSubs.update(E3)
	if p: print 'OutputSubs:\n', OutputSubs

	OutputEqsFinal = OutputVars
	_OutputEqsFinal = None
	while OutputEqsFinal != _OutputEqsFinal:
		_OutputEqsFinal = OutputEqsFinal
		OutputEqsFinal = [eq.subs(OutputSubs) for eq in OutputEqsFinal]
	if p: print 'OutputEqsFinal:\n', OutputEqsFinal

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

if __name__ == '__main__':
	find(
		"vS",
		"vMB' = 1/MB * fMB, vMW' = 1/MW * fMW, fKS' = KS * vKS, fKT' = KT * vKT",
		"fBS = BS * vBS, fBT = BT * vBT",
		"fMB = fKS + fBS, fMW = fKT + fBT - fKS - fBS, vKS = vMW - vMB, vKT = vS - vMW, vBS = vMW - vMB, vBT = vS - vMW",
		"vMB, vMW, fKS, fKT, fBS, fBT")
