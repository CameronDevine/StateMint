# Import everything from the sympy library.
from sympy import *
# Import the copy library.
import copy

# Define the symbols t and s.
t, s = symbols('t s')
# Define a dummy variable named dummy.
dummy = symbols('dummy')

def condition_vec(string):
	string = string.replace(' ', '').split(',')
	vec = []
	for el in string:
		vec.append(sympify(el + '(t)'))
	return vec

def condition_eq(string):
	if len(string) == 0:
		return []
	else:
		string = string.replace("'", "(t).diff(t)").split(',')
		eqs = []
		for el in string:
			eqs.append(sympify('Eq(' + el.replace('=', ',') + ')'))
		return eqs

def condition_subs(string):
	string = string.replace("'", "(t).diff(t)").split(',')
	subs = []
	for el in string:
		eqn = sympify('Eq(' + el.replace('=', ',') + ')')
		subs.append([eqn.lhs, eqn.rhs])
	return subs

def sub_list_list(eqs, subs):
	eqr = []
	for eq in eqs:
		eqt = eq
		for sub in subs:
			eqt = eqt.subs(sub[0], sub[1])
		eqr.append(eqt)
	return eqr

def eq_to_sub(eqs):
	subs = []
	for eq in eqs:
		subs.append([eq.lhs, eq.rhs])
	return subs

def get_st_vars(eqns):
	vars = []
	for eqn in eqns:
		vars.append(integrate(eqn.lhs, t))
	return vars

def get_pri_vars(eqns):
	vars = []
	for eqn in eqns:
		vars.append(eqn.lhs)
	return vars

def get_sec_vars(subs):
	vars = []
	for sub in subs:
		vars.append(sub[0])
	return vars

def get_func_subs(func1, func2, var1, var2):
	subs = []
	for f in func1:
		subs.append([sympify(str(f).replace('(t)', '')), f])
	for f in func2:
		subs.append([sympify(str(f).replace('(t)', '')), f])
	for var in var1:
		subs.append([var, sympify(str(var) + '(t)')])
	for var in var2:
		subs.append([var, sympify(str(var) + '(t)')])
	return subs

def sub_sub(subs1, subs2):
	subs = []
	for sub1 in subs1:
		sub = sub1
		for sub2 in subs2:
			sub[0] = sub[0].subs(sub2[0], sub2[1])
			sub[1] = sub[1].subs(sub2[0], sub2[1])
		subs.append(sub)
	return subs

def sub_sub_to(subs):
	subs_r = []
	for i in range(len(subs)):
		sub = copy.deepcopy(subs)[i]
		for j in range(len(subs)):
			if i != j:
				sub[1] = sub[1].subs(subs[j][0], subs[j][1])
		subs_r.append(sub)
	return subs_r

def get_rhs(eqs):
	f = []
	for eq in eqs:
		f.append(eq.rhs)
	return f

def make_matrix(eqs, vars, D = False):
	n = len(eqs)
	m = len(vars)
	M = zeros(n,m)
	for i in range(n):
		for j in range(m):
			if D:
				M[i,j] = simplify(diff(eqs[i].subs(vars[j].diff(t), dummy), dummy))
			else:
				M[i,j] = simplify(diff(eqs[i], vars[j]))
	return M

def make_tf(A, Bp, C, Dp, F):
	return C * (s * eye(A.shape[0]) - A)**-1 * Bp + Dp + F * s

def solve_state(eqs, vars):
	eqr = []
	for i in range(len(vars)):
		eqr.append(simplify(solve(eqs[i].doit(), vars[i].diff(t))[0]))
	return eqr

def state_eq_subs(eqs, vars):
	subs = []
	for i in range(len(vars)):
		subs.append([vars[i].diff(t), eqs[i]])
	return subs 

def sub_solve(subs):
	rsubs = []
	for sub in subs:
		eq = solve(Eq(sub[0], sub[1]), sub[0])[0]
		rsubs.append([sub[0], eq])
	return rsubs

def make_vec(vars):
	for i in range(len(vars)):
		vars[i] = sympify(str(vars[i]).replace('(t)', ''))
	return Matrix([vars]).T

def make_mat(eqs):
	return Matrix([eqs]).T

# The main find state space model function.
def find(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars):
	# InVars: A string of input variable seperated by spaces.
	# StVarElEqns: A string of state variable elemental equations seperated by commas, using ' for derivative, and = for equality.
	# OtherElEqns: A string of non-state elemental equations seperated by commas, using ' for derivative, and = for equality.
	# Constrains: A string of constraint (continuity and compatability) equations seperated by commas.
	# 
	InVars = condition_vec(InVars)

	OutputVars = condition_vec(OutputVars)

	StVarElEqns = condition_eq(StVarElEqns)

	OtherElEqns = condition_eq(OtherElEqns)

	Constraints = condition_subs(Constraints)

	print "Symbolic Expressions Created"

	StVars = get_st_vars(StVarElEqns)

	PriVars = get_pri_vars(OtherElEqns)

	SecVars = get_sec_vars(Constraints)

	print "Variable Collected"

	func_subs = get_func_subs(StVars, InVars, PriVars, SecVars)

	StVarElEqns = sub_list_list(StVarElEqns, func_subs)

	OtherElEqns = sub_list_list(OtherElEqns, func_subs)

	StVars = sub_list_list(StVars, func_subs)

	PriVars = sub_list_list(PriVars, func_subs)

	SecVars = sub_list_list(SecVars, func_subs)

	print "Functions Created"

	Constraints = sub_sub(Constraints, func_subs)

	St2 = sub_list_list(StVarElEqns, Constraints)

	Co2 = sub_list_list(OtherElEqns, Constraints)

	E3 = sub_solve(sub_sub_to(eq_to_sub(Co2)))

	StateEquation = sub_list_list(St2, E3)

	StateEqsFinal = solve_state(StateEquation, StVars)

	OutputEqsFinal = sub_list_list(sub_list_list(sub_list_list(OutputVars, Constraints), E3), state_eq_subs(StateEqsFinal, StVars))

	print "Equations Solved"

	A = make_matrix(StateEqsFinal, StVars)
	B = make_matrix(StateEqsFinal, InVars)
	C = make_matrix(OutputEqsFinal, StVars)
	D = make_matrix(OutputEqsFinal, InVars)
	E = make_matrix(StateEqsFinal, InVars, D = True)
	F = make_matrix(OutputEqsFinal, InVars, D = True)

	Bp = A * E + B
	Dp = C * E + D

	print "Matricies Created"

	TF = make_mat(make_tf(A, Bp, C, Dp, F))

	print "Transfer Function Found"

	StVec = make_vec(StVars)
	OutVec = make_vec(OutputVars)
	
	StateEqsFinalMat = make_mat(StateEqsFinal)
	OutputEqsFinalMat = make_mat(OutputEqsFinal)

	to_print = []
	if len(to_print) != 0:
		print
		for var in to_print:
			for eq in var:
				pprint(simplify(eq))
			print "--------------------------------"

	return {'A': A, 'B': B, 'C': C, 'D': D, 'E': E, 'F': F, 'Bp': Bp, 'Dp': Dp, 'TF': TF, 'StateVec': StVec, 'OutputVec': OutVec, 'StateEq': StateEqsFinalMat, 'OutEq': OutputEqsFinalMat}
