from sympy import *

t, s = symbols('t s')
dummy = symbols('dummy')

def sympify_vec(data):
	return [sympify(el + '(t)') for el in data]

def sympify_eqs(data):
	if len(data) == 0:
		return []
	return [sympify('Eq(' + el.replace("'", "(t).diff(t)").replace('=', ',') + ')') for el in data]

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

class output:
	'''
	This class is a container in which the output from :meth:`StateModelRnD.Solve` is placed. This allows
	The results of the solution to be easily accessed as members of the class.
	'''
	A = None
	'''
	The state matrix, :math:`A`, in equations such as, :math:`\dot{x}=Ax+Bu`.
	'''
	B = None
	'''
	The input matrix, :math:`B`, in equations such as, :math:`\dot{x}=Ax+Bu`.
	'''
	C = None
	'''
	The output matrix, :math:`C`, in equations such as, :math:`y=Cx+Du`.
	'''
	D = None
	'''
	The feedthrough matrix, :math:`D`, in equations such as, :math:`y=Cx+Du`.
	'''
	E = None
	'''
	The time derivative input matrix, :math:`E`, in equations such as, :math:`\dot{x}=Ax+Bu+E\dot{u}`.
	'''
	F = None
	'''
	The time derivative feedthrough matrix, :math:`F`, in equations such as, :math:`y=Cx+Du+F\dot{u}`.
	'''
	Bp = None
	'''
	The input matrix, :math:`B'`, in equations such as, :math:`\dot{x}'=Ax'+B'u`, where the time derivative of the input has been removed by modifying the state vector.
	'''
	Dp = None
	'''
	The feedthrough matrix, :math:`D'`, in equations such as, :math:`y=Ax'+D'u`, where the time derivative of the input has been removed by modifying the state vector.
	'''
	TF = None
	'''
	The transfer function of the system.
	'''
	StateVec = None
	'''
	The symbolic state vector :math:`x`.
	'''
	OutputVec = None
	'''
	The symbolic output vector :math:`y`.
	'''
	StateEq = None
	'''
	The full state equation, :math:`\dot{x}=f(x,y)`.
	'''
	OutEq = None
	'''
	The full output equation, :math:`y=h(x,u)`.
	'''
	InputVec = None
	'''
	The symbolic input vector :math:`u`.
	'''

def Solve(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars):
	'''
	This function takes the input and output variables, along with the state, elemental, and constrain equations
	as derived using the method in Rowell and Wormley. It returns a state space model, along with a transfer function
	and the state and ouput equations.

	:param InVars: A lost with the input variables
	:param StVarElEqns: A list of the state variable elemental equations with the state variables on the left hand side
	:param OtherElEqns: A list of the other elemental equations with the primary varible on the left hand side
	:param Constraints: A list of the constraint equations with the secondary variables on the left hand side
	:param OutputVars: A list of the output variables
	:type InVars: list
	:type StVarElEqns: list
	:type OtherElEqns: list
	:type Constraints: list
	:type OutputVars: list
	:returns: The model of the system in multiple forms
	:rtype: :meth:`StateModelRnD.output`
	'''

	InVars = sympify_vec(InVars)

	OutputVars = sympify_vec(OutputVars)

	StVarElEqns = sympify_eqs(StVarElEqns)

	OtherElEqns = sympify_eqs(OtherElEqns)

	Constraints = sympify_eqs(Constraints)

	StVars = [integrate(eq.lhs, t) for eq in StVarElEqns]

	PriVars = [eq.lhs for eq in OtherElEqns]

	SecVars = [eq.lhs for eq in Constraints]

	func_subs = dict([(sympify(str(var).replace('(t)', '')), var) if '(t)' in str(var) else (var, sympify(str(var) + '(t)')) for var in InVars + StVars + PriVars + SecVars])

	StVarElEqns = [eq.subs(func_subs) for eq in StVarElEqns]

	OtherElEqns = [eq.subs(func_subs) for eq in OtherElEqns]

	StVars = [eq.subs(func_subs) for eq in StVars]

	PriVars = [eq.subs(func_subs) for eq in PriVars]

	SecVars = [eq.subs(func_subs) for eq in SecVars]

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

	A = make_matrix(StateEqsFinal, StVars)
	B = make_matrix(StateEqsFinal, InVars)
	C = make_matrix(OutputEqsFinal, StVars)
	D = make_matrix(OutputEqsFinal, InVars)
	E = make_matrix(StateEqsFinal, InVars, True)
	F = make_matrix(OutputEqsFinal, InVars, True)

	Bp = A * E + B
	Dp = C * E + D

	TF = Matrix([C * (s * eye(A.shape[0]) - A)**-1 * Bp + Dp + F * s]).T

	StVec = make_vec(StVars)
	OutVec = make_vec(OutputVars)
	InVec = make_vec(InVars)
	
	StateEqsFinalMat = Matrix([StateEqsFinal]).T
	OutputEqsFinalMat = Matrix([OutputEqsFinal]).T

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
	result.StateVec = Matrix(StVec)
	result.OutputVec = Matrix(OutVec)
	result.StateEq = StateEqsFinalMat
	result.OutEq = OutputEqsFinalMat
	result.InputVec = Matrix(InVec)

	return result
