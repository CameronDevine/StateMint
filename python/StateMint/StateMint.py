r'''
This package finds the state-space model of a lumped-parameter dynamic system
from its elemental and constraint equations. The `Solve` function takes the
equations in the forms specified by Rowell and Wormley in "System Dynamics: An
Introduction" (1997), chapter 5: state-variable elemental equations solved for
the derivative of each state variable, the other elemental equations solved for
their primary variables, and the constraint (continuity and compatibility)
equations solved for the secondary variables. It eliminates every variable that
is neither a state nor an input and returns the state and output equations,
their matrices, and (for linear systems) the transfer function matrix.

A `tutorial <https://github.com/CameronDevine/StateMint/blob/master/tutorial.md>`_
covers how to prepare the equations, and an `example
<https://github.com/CameronDevine/StateMint/blob/master/python/Example.ipynb>`_
shows how to use this code. Convenience functions in `StateMint.to_numpy`
convert the symbolic matrices to NumPy arrays.

Install with ``pip install StateMint``. A web interface runs the same code in
the browser.

Equation syntax
---------------
Each equation is a string with exactly one ``=``. A prime marks a time
derivative: ``vm' = Fm/m``. Names are letters, digits and underscores, starting
with a letter. Multiplication is explicit (``2*x``); ``^`` and ``**`` both mean
a power. The functions listed in `names` (plus ``abs``) and the constant ``pi``
are available. ``t`` is time and ``s`` is the Laplace variable, so neither can
be a variable name.

Parsing never evaluates arbitrary Python: the text may contain only names,
numbers, ``+ - * / ^ ( ) , = '`` and spaces, and no attribute access or Python
keywords.
'''

import io
import keyword
import re
import tokenize

import sympy
from sympy.core.function import AppliedUndef
from sympy.parsing.sympy_parser import (
	convert_xor, parse_expr, standard_transformations)
from sympy.polys.matrices import DomainMatrix
from sympy.polys.polyerrors import CoercionFailed, PolynomialError
from sympy.solvers.solveset import NonlinearError

t, s = sympy.symbols('t s')
dummy = sympy.symbols('dummy')

names = [
	'Eq',
	'Function',
	'Symbol',
	'Integer',
	'Float',
	'Rational',
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
	're',
	'im',
	'Abs',
	'arg',
	'conjugate',
	'ceiling',
	'floor',
	'sign',
	'Min',
	'Max',
	'Heaviside',
	'pi',
]
'''Names (functions and constants) that may appear in equations.

``I`` is deliberately absent: it is a common variable name (current, inertance)
and a state-space model has no use for the imaginary unit.'''

funcs = dict((name, getattr(sympy, name)) for name in names)
funcs['abs'] = sympy.Abs

_reserved = set(funcs) | {'t', 's'}

_transformations = standard_transformations + (convert_xor,)

_allowed_chars = set(
	'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
	" \t+-*/^().,='")

_name_re = re.compile(r'^[A-Za-z][A-Za-z0-9_]*$')
_prime_re = re.compile(r"\b([A-Za-z][A-Za-z0-9_]*)\s*'")


class StateMintError(ValueError):
	'''Raised when StateMint cannot read the equations or cannot solve them.

	The message says which equation or variable is at fault and why.'''


def split_entries(text):
	'''Split a text field into entries.

	Entries are separated by new lines or by commas outside parentheses, so
	``atan2(y, x)`` stays whole. Surrounding white space is removed and blank
	entries (blank lines, trailing commas) are dropped. This is how the web
	interface reads its text boxes and its saved ``.rnd`` files.

	Args:
		text (str): The contents of one field.

	Returns:
		list of str: The entries.
	'''
	entries = []
	current = []
	depth = 0
	for ch in text:
		if ch in '([{':
			depth += 1
		elif ch in ')]}':
			depth = max(depth - 1, 0)
		if ch == '\n' or (ch == ',' and depth == 0):
			entries.append(''.join(current))
			current = []
		else:
			current.append(ch)
	entries.append(''.join(current))
	return [entry.strip() for entry in entries if entry.strip()]


def _clean(items, what):
	if items is None:
		return []
	if isinstance(items, str):
		items = split_entries(items)
	cleaned = []
	for item in items:
		if not isinstance(item, str):
			raise StateMintError(
				'{}: expected text, got {!r}'.format(what, item))
		item = item.strip()
		if item:
			cleaned.append(item)
	return cleaned


def _check_text(text, where):
	bad = sorted(set(text) - _allowed_chars)
	if bad:
		raise StateMintError('{}: unexpected character{} {} in "{}"'.format(
			where, 's' if len(bad) > 1 else '',
			' '.join(repr(ch) for ch in bad), text))
	try:
		tokens = list(tokenize.generate_tokens(
			io.StringIO(text.replace("'", ' ')).readline))
	except (tokenize.TokenError, SyntaxError, IndentationError):
		raise StateMintError(
			'{}: unbalanced parentheses in "{}"'.format(where, text))
	for tok in tokens:
		if tok.type == tokenize.NAME:
			if keyword.iskeyword(tok.string) or '__' in tok.string:
				raise StateMintError(
					'{}: "{}" cannot be used as a name (in "{}")'.format(
						where, tok.string, text))
		elif tok.type == tokenize.OP and tok.string == '.':
			raise StateMintError(
				'{}: misplaced "." in "{}"'.format(where, text))
		elif tok.type == tokenize.ERRORTOKEN and tok.string.strip():
			raise StateMintError(
				'{}: cannot read "{}"'.format(where, text))


def _parse(text, where):
	'''Parse one side of an equation, or an expression, into sympy.'''
	_check_text(text, where)
	code = _prime_re.sub(r'\1(t).diff(t)', text)
	if "'" in code:
		raise StateMintError(
			"{}: a prime (') must follow a variable name, as in x', "
			'and only first derivatives are allowed (in "{}")'.format(
				where, text))
	try:
		expr = parse_expr(
			code, global_dict=dict(funcs), transformations=_transformations)
	except Exception as err:
		raise StateMintError(
			'{}: cannot read "{}" ({}: {})'.format(
				where, text, type(err).__name__, err))
	if not isinstance(expr, sympy.Expr):
		raise StateMintError(
			'{}: "{}" is not an expression. Names of functions and constants '
			'(sin, sign, pi, ...) and t and s are reserved.'.format(
				where, text))
	return expr


def _parse_eq(text, where):
	if text.count('=') != 1:
		raise StateMintError(
			'{}: "{}" must contain exactly one "="'.format(where, text))
	lhs, rhs = [side.strip() for side in text.split('=')]
	if not lhs or not rhs:
		raise StateMintError(
			'{}: "{}" needs something on both sides of "="'.format(
				where, text))
	return sympy.Eq(_parse(lhs, where), _parse(rhs, where), evaluate=False)


def _name_of(expr):
	'''The variable name of a bare symbol or of a function of time.'''
	if isinstance(expr, sympy.Symbol):
		return expr.name
	if isinstance(expr, AppliedUndef) and expr.args == (t,):
		return expr.func.__name__
	return None


def _function_names(expr):
	return set(f.func.__name__ for f in expr.atoms(AppliedUndef))


def _derivatives(expr):
	return expr.atoms(sympy.Derivative)


def make_matrix(eqs, vars, D=False):
	'''Jacobian of `eqs` with respect to `vars` (or, if `D`, with respect to
	their time derivatives).'''
	M = sympy.zeros(len(eqs), len(vars))
	for i in range(len(eqs)):
		# Freeze derivatives so that x(t) and dx/dt are independent.
		dreps = dict((d, sympy.Dummy()) for d in _derivatives(eqs[i]))
		back = dict((v, k) for k, v in dreps.items())
		e = eqs[i].xreplace(dreps)
		for j in range(len(vars)):
			if D:
				y = dreps.get(vars[j].diff(t))
				if y is None:
					continue
				entry = e.diff(y)
			else:
				y = sympy.Dummy()
				entry = e.xreplace({vars[j]: y}).diff(y).xreplace({y: vars[j]})
			M[i, j] = sympy.simplify(entry.xreplace(back))
	return M


def _symbolic(expr):
	'''Replace each x(t) by the symbol x and each dx/dt by the symbol x'.'''
	reps = {}
	for d in _derivatives(expr):
		name = _name_of(d.expr)
		if name is not None and d.variables == (t,):
			reps[d] = sympy.Symbol(name + "'")
	expr = expr.xreplace(reps)
	return expr.xreplace(dict(
		(f, sympy.Symbol(f.func.__name__)) for f in expr.atoms(AppliedUndef)
		if f.args == (t,)))


def make_vec(vars):
	return [_symbolic(v) for v in vars]


class output:
	r'''A container for the resulting differential equation.

	This class is a container in which the output from `StateMint.Solve` is
	placed. This allows the results of the solution to be easily accessed as
	members of the class.
	'''

	A = None
	r'''sympy.Matrix: The state matrix, :math:`A`.

	This matrix is found in state space formulations of dynamic systems such
	as, :math:`\dot{x}=Ax+Bu`.
	'''

	B = None
	r'''sympy.Matrix: The input matrix, :math:`B`.

	This matrix is found in state space formulations of dynamics systems such
	as, :math:`\dot{x}=Ax+Bu`.
	'''

	C = None
	r'''sympy.Matrix: The output matrix, :math:`C`.

	This matrix is found in a linear output equation of the form,
	:math:`y=Cx+Du`.
	'''

	D = None
	r'''sympy.Matrix: The feedthrough matrix, :math:`D`.

	This matrix is found in a linear output equation of the form,
	:math:`y=Cx+Du`.
	'''

	E = None
	r'''sympy.Matrix: The time derivative input matrix, :math:`E`.

	This matrix is found state space formulations of dynamic systems such as,
	:math:`\dot{x}=Ax+Bu+E\dot{u}`.
	'''

	F = None
	r'''sympy.Matrix: The time derivative feedthrough matrix, :math:`F`.

	This matrix is found in linear output equations of the form,
	:math:`y=Cx+Du+F\dot{u}`.
	'''

	Bp = None
	r'''sympy.Matrix: The input matrix, :math:`B' = AE + B`.

	This matrix is found in equations such as, :math:`\dot{x}'=Ax'+B'u`,
	where the time derivative of the input has been removed by the change of
	state :math:`x' = x - Eu`.
	'''

	Dp = None
	r'''sympy.Matrix: The feedthrough matrix, :math:`D' = CE + D`.

	This matrix is found in equations such as, :math:`y=Cx'+D'u+F\dot{u}`,
	where the time derivative of the input has been removed from the state
	equation by the change of state :math:`x' = x - Eu`.
	'''

	TF = None
	r'''sympy.Matrix: The transfer function matrix of the system,
	:math:`H(s) = C(sI-A)^{-1}B' + D' + Fs`, with one column per input. None
	if the system is not linear.'''

	StateVec = None
	r'''sympy.Matrix: The symbolic state vector :math:`x`.'''

	OutputVec = None
	r'''sympy.Matrix: The symbolic output vector :math:`y`.'''

	StateEq = None
	r'''sympy.Matrix: The full state equation, :math:`\dot{x}=f(x,u)`.'''

	OutEq = None
	r'''sympy.Matrix: The full output equation, :math:`y=h(x,u)`.'''

	InputVec = None
	r'''sympy.Matrix: The symbolic input vector :math:`u`.'''

	Parameters = None
	r'''list of sympy.Symbol: The symbols left in the model that are not
	states or inputs (masses, stiffnesses, ...). A variable you meant to
	eliminate but forgot to give an equation shows up here.'''

	Linear = None
	r'''bool: Whether the state and output equations are linear, so that the
	matrices describe them completely.'''

	Nonstandard = None
	r'''bool: Whether the model has input derivatives (nonzero E or F).'''

	def __repr__(self):
		return '<StateMint model: {} states, {} inputs, {} outputs{}>'.format(
			len(self.StateVec), len(self.InputVec), len(self.OutputVec),
			'' if self.Linear else ', nonlinear')


def _resolve_constraints(constraints, secondary):
	'''Substitute the constraints into each other until every right-hand side
	is free of secondary variables.'''
	sub = dict((eq.lhs, eq.rhs) for eq in constraints)
	for _ in range(len(sub) + 1):
		new = dict((k, v.xreplace(sub)) for k, v in sub.items())
		if new == sub:
			return sub
		sub = new
	loop = sorted(_name_of(k) for k, v in sub.items()
		if any(f in v.atoms(AppliedUndef) for f in secondary))
	raise StateMintError(
		'Constraint equations: the constraints for {} refer to each other in '
		'a loop. Each constraint should give its secondary variable in terms '
		'of primary variables.'.format(', '.join(loop)))


def _derivative_closure(St2, Co2, primary, secondary_sub):
	'''Derivatives of primary variables can appear (e.g. when a constraint
	with a derivative is substituted). Add the derivative of each such primary
	variable's elemental equation as a further equation.'''
	pri_eq = dict((eq.lhs, eq.rhs) for eq in Co2)
	extra = []
	have = set()
	while True:
		needed = set()
		for eq in St2 + Co2 + extra:
			for d in _derivatives(eq.rhs):
				if d.expr in pri_eq and d.variables == (t,) and d not in have:
					needed.add(d)
		if not needed:
			return extra
		for d in needed:
			have.add(d)
			extra.append(sympy.Eq(
				d, pri_eq[d.expr].diff(t).xreplace(secondary_sub).doit()))


def _solve_linear(eqs, unknowns):
	'''Solve equations that are linear in the unknowns simultaneously.

	Returns a dict unknown -> solution, or raises NonlinearError.'''
	syms = [sympy.Dummy('u{}'.format(i)) for i in range(len(unknowns))]
	derivs = [(u, y) for u, y in zip(unknowns, syms)
		if isinstance(u, sympy.Derivative)]
	funcs_ = [(u, y) for u, y in zip(unknowns, syms)
		if not isinstance(u, sympy.Derivative)]
	exprs = [(eq.lhs - eq.rhs).xreplace(dict(derivs)).xreplace(dict(funcs_))
		for eq in eqs]
	M, b = sympy.linear_eq_to_matrix(exprs, syms)
	solutions = sympy.linsolve((M, b), syms)
	if solutions == sympy.EmptySet or len(solutions) == 0:
		raise StateMintError(
			'The equations are inconsistent: no solution exists. Check the '
			'signs and for duplicated or contradictory equations.')
	solution = list(solutions)[0]
	free = set().union(*(e.free_symbols for e in solution)) & set(syms)
	if free:
		undetermined = [unknowns[syms.index(y)] for y in free]
		raise StateMintError(
			'The equations do not determine {} (they are not independent). '
			'Check for a missing equation or for a loop of only state-variable '
			'elements.'.format(', '.join(sorted(
				str(_symbolic(u)) for u in undetermined))))
	back = dict((y, u) for u, y in zip(unknowns, syms))
	return dict((u, e.xreplace(back)) for u, e in zip(unknowns, solution))


def _solve_substitution(St2, Co2, states):
	'''The original StateMint elimination: solve each other elemental equation
	for its primary variable, substitute until nothing changes, then solve the
	state equations for the state derivatives. Handles equations that are
	nonlinear in the eliminated variables.'''
	E3 = {}
	for eq1 in Co2:
		eq = eq1
		for eq2 in Co2:
			if eq2 is not eq1:
				eq = sympy.Eq(eq.lhs, eq.rhs.xreplace({eq2.lhs: eq2.rhs}),
					evaluate=False)
		sols = sympy.solve(sympy.Eq(eq.lhs, eq.rhs), eq1.lhs)
		if len(sols) == 0:
			raise StateMintError(
				'Other elemental equations: cannot solve "{} = {}" for '
				'{}.'.format(_symbolic(eq1.lhs), _symbolic(eq1.rhs),
					_symbolic(eq1.lhs)))
		E3[eq1.lhs] = sols[0]

	StateEquation = [eq.rhs - eq.lhs for eq in St2]
	for _ in range(len(E3) + 2):
		new = [e.xreplace(E3).doit() for e in StateEquation]
		if new == StateEquation:
			break
		StateEquation = new
	else:
		raise StateMintError(
			'Could not eliminate the variables {}: their equations depend on '
			'each other in a nonlinear loop.'.format(', '.join(sorted(
				_name_of(k) for k in E3))))
	xdots = [x.diff(t) for x in states]
	sol = sympy.solve(StateEquation, xdots, dict=True)
	if len(sol) != 1 or set(sol[0]) != set(xdots):
		raise StateMintError(
			'Could not solve the state equations for the state derivatives.')
	solution = dict(sol[0])
	for p, e in E3.items():
		solution[p] = e
	return solution


def _substitute(expr, solution, secondary_sub, limit):
	'''Replace eliminated variables in expr until only states and inputs
	remain.'''
	derivs = dict((k, v) for k, v in solution.items()
		if isinstance(k, sympy.Derivative))
	others = dict((k, v) for k, v in solution.items()
		if not isinstance(k, sympy.Derivative))
	for _ in range(limit):
		new = expr.xreplace(secondary_sub).doit()
		new = new.xreplace(derivs).xreplace(others).doit()
		if new == expr:
			break
		expr = new
	return expr


def _transfer_function(A, Bp, C, Dp):
	'''H(s) = C (sI - A)^-1 B' + D', entry by entry as a ratio of
	determinants (Schur complement):

	    H_ij = det([[sI - A, B'_j], [-C_i, D'_ij]]) / det(sI - A),

	computed over polynomials in s whose coefficients are rational functions
	of the parameters, then cancelled (and factored, up to four states). This is fast and keeps
	every entry a single fraction; inverting sI - A symbolically is not.'''
	n = A.shape[0]
	rows, cols = C.shape[0], Bp.shape[1]
	if n == 0:
		return Dp.applyfunc(sympy.factor)
	# The coefficient field: rational functions of the parameters and of any
	# other generators, such as cos(theta), that the matrices contain.
	parts = []
	for M in (A, Bp, C, Dp):
		for e in M:
			parts.extend(sympy.together(e).as_numer_denom())
	try:
		gens = sympy.parallel_poly_from_expr(parts)[1]['gens']
	except PolynomialError:
		gens = ()
	gens = sorted((g for g in gens if g != s), key=str)
	K = sympy.ZZ.frac_field(*gens) if gens else sympy.QQ
	R = K[s]

	def det(M):
		try:
			D = DomainMatrix(
				[[R.from_sympy(e) for e in row] for row in M.tolist()],
				M.shape, R)
			return R.to_sympy(D.det())
		except (CoercionFailed, ValueError):
			return sympy.expand(M.det(method='berkowitz'))

	sI_A = s * sympy.eye(n) - A
	den = det(sI_A)
	H = sympy.zeros(rows, cols)
	for i in range(rows):
		for j in range(cols):
			num = det(sympy.Matrix.vstack(
				sympy.Matrix.hstack(sI_A, Bp[:, j]),
				sympy.Matrix.hstack(-C[i, :], Dp[i:i + 1, j:j + 1])))
			H[i, j] = sympy.cancel(num / den)
	# Factoring makes small transfer functions readable but dominates the
	# time for large ones, whose factors are long polynomials anyway.
	if n <= 4:
		H = H.applyfunc(sympy.factor)
	return H


def Solve(InVars, StVarElEqns, OtherElEqns, Constraints, OutputVars,
		method='auto', transfer_function=True):
	r'''Find the differential equations of a dynamic system from elemental and
	constraint equations.

	This function takes the input and output variables, along with the state,
	elemental, and constraint equations. It returns a state space model, along
	with a transfer function and the state and output equations.

	Each argument is a list of strings. A single string is also accepted and
	split into entries at new lines and at commas outside parentheses (see
	`split_entries`). Blank entries are ignored, so any list may be empty.

	Args:
		InVars (list of str): The system's input variables.
		StVarElEqns (list of str): The state variable elemental equations, each
			solved for the derivative of its state variable, e.g.
			``"vm' = Fm/m"``.
		OtherElEqns (list of str): The other elemental equations, each solved
			for its primary variable, e.g. ``"FB = B*vB"``.
		Constraints (list of str): The constraint (continuity and
			compatibility) equations, each solved for a secondary variable,
			e.g. ``"Fm = Fs - FB"``.
		OutputVars (list of str): The system's outputs: variable names or
			expressions in the system's variables, e.g. ``"FK + FB"``.
		method (str): How to eliminate the variables that are neither states
			nor inputs. ``'linear'`` solves the equations simultaneously as a
			linear system in those variables (Rowell and Wormley section 5.5);
			``'substitution'`` substitutes equation into equation (the
			original StateMint method, which can handle equations nonlinear in
			those variables); ``'auto'`` (the default) uses ``'linear'`` when
			it applies and ``'substitution'`` otherwise.
		transfer_function (bool): Whether to compute the transfer function
			matrix `output.TF`. It is the slowest part for large systems;
			with False, TF is None.

	Returns:
		output: The symbolically determined differential equation describing
		the system.

	Raises:
		StateMintError: If an equation cannot be read, a variable is defined
		twice, or the variables cannot be eliminated.
	'''
	if method not in ('auto', 'linear', 'substitution'):
		raise ValueError('method must be "auto", "linear" or "substitution"')

	InVars = _clean(InVars, 'Input variables')
	StVarElEqns = _clean(StVarElEqns, 'State-variable elemental equations')
	OtherElEqns = _clean(OtherElEqns, 'Other elemental equations')
	Constraints = _clean(Constraints, 'Constraint equations')
	OutputVars = _clean(OutputVars, 'Output variables')

	if not StVarElEqns and not OtherElEqns and not Constraints:
		raise StateMintError('There are no equations.')

	# Read the equations and find the variables each one defines.
	in_names = []
	for v in InVars:
		if not _name_re.match(v):
			raise StateMintError(
				'Input variables: "{}" is not a variable name'.format(v))
		in_names.append(v)

	st_eqs, st_names = [], []
	for text in StVarElEqns:
		eq = _parse_eq(text, 'State-variable elemental equation')
		lhs = eq.lhs
		if not (isinstance(lhs, sympy.Derivative) and lhs.variables == (t,)
				and _name_of(lhs.expr) is not None):
			raise StateMintError(
				'State-variable elemental equation "{}": the left side must be '
				"the derivative of the state variable, as in vm' = Fm/m".format(
					text))
		st_eqs.append(eq)
		st_names.append(_name_of(lhs.expr))

	def defining(texts, what):
		eqs, defined = [], []
		for text in texts:
			eq = _parse_eq(text, what)
			name = _name_of(eq.lhs)
			if name is None:
				raise StateMintError(
					'{} "{}": the left side must be a single variable'.format(
						what, text))
			eqs.append(eq)
			defined.append(name)
		return eqs, defined

	other_eqs, pri_names = defining(OtherElEqns, 'Other elemental equation')
	con_eqs, sec_names = defining(Constraints, 'Constraint equation')

	roles = {}
	for role, group in (('an input', in_names), ('a state', st_names),
			('a primary variable', pri_names),
			('a secondary variable', sec_names)):
		for name in group:
			if name in _reserved:
				raise StateMintError(
					'"{}" is reserved (a function, a constant, time t or the '
					'Laplace variable s) and cannot be a variable name'.format(
						name))
			if name in roles:
				raise StateMintError(
					'"{}" is defined twice: as {} and as {}. Each variable '
					'should be an input or appear on the left side of exactly '
					'one equation.'.format(name, roles[name], role))
			roles[name] = role

	F = dict((n, sympy.Function(n)(t)) for n in roles)
	to_func = dict((sympy.Symbol(n), F[n]) for n in roles)

	def fn(expr):
		return expr.xreplace(to_func)

	inputs = [F[n] for n in in_names]
	states = [F[n] for n in st_names]
	primary = [F[n] for n in pri_names]
	secondary = [F[n] for n in sec_names]

	St = [sympy.Eq(fn(eq.lhs), fn(eq.rhs), evaluate=False) for eq in st_eqs]
	Co = [sympy.Eq(fn(eq.lhs), fn(eq.rhs), evaluate=False) for eq in other_eqs]
	Cons = [sympy.Eq(fn(eq.lhs), fn(eq.rhs), evaluate=False) for eq in con_eqs]

	# A variable used with a prime must be one of the system's variables.
	for eq in St + Co + Cons:
		for f in eq.atoms(AppliedUndef):
			if f.func.__name__ not in roles:
				raise StateMintError(
					'"{}" is used with a derivative but is not an input, a '
					'state, or defined by an equation.'.format(
						f.func.__name__))

	# Step 1: eliminate the secondary variables using the constraints.
	sec_sub = _resolve_constraints(Cons, secondary)
	St2 = [sympy.Eq(eq.lhs, eq.rhs.xreplace(sec_sub).doit(), evaluate=False)
		for eq in St]
	Co2 = [sympy.Eq(eq.lhs, eq.rhs.xreplace(sec_sub).doit(), evaluate=False)
		for eq in Co]
	extra = _derivative_closure(St2, Co2, primary, sec_sub)

	# Step 2: eliminate the primary variables and solve for the derivatives.
	unknowns = [x.diff(t) for x in states] + primary + [e.lhs for e in extra]
	solution = None
	if method in ('auto', 'linear'):
		try:
			solution = _solve_linear(St2 + Co2 + extra, unknowns)
		except (NonlinearError, PolynomialError):
			if method == 'linear':
				raise StateMintError(
					'The equations are not linear in the variables to be '
					'eliminated; use method="substitution".')
	if solution is None:
		solution = _solve_substitution(St2, Co2, states)

	limit = len(roles) + 3
	StateEqsFinal = [sympy.simplify(
		_substitute(x.diff(t), solution, sec_sub, limit)) for x in states]

	# Outputs may be names or expressions in the system's variables.
	outputs = []
	for text in OutputVars:
		if _name_re.match(text) and text not in roles:
			raise StateMintError(
				'Output "{}" is not an input, a state, or defined by an '
				'equation.'.format(text))
		expr = fn(_parse(text, 'Output variable'))
		for f in expr.atoms(AppliedUndef):
			if f.func.__name__ not in roles:
				raise StateMintError(
					'Output "{}": "{}" is not one of the system\'s '
					'variables'.format(text, f.func.__name__))
		outputs.append(expr)
	OutputEqsFinal = [sympy.simplify(
		_substitute(y, solution, sec_sub, limit)) for y in outputs]

	# Every remaining variable must be a state or an input.
	allowed = set(st_names) | set(in_names)
	input_derivs = set(u.diff(t) for u in inputs)
	for label, exprs in (('state equations', StateEqsFinal),
			('output equations', OutputEqsFinal)):
		for e in exprs:
			left = _function_names(e) - allowed
			bad_d = set(d for d in _derivatives(e) if d not in input_derivs)
			if left or bad_d:
				what = sorted(left | set(str(_symbolic(d)) for d in bad_d))
				raise StateMintError(
					'Could not eliminate {} from the {}. Check that each of '
					'these is an input or is defined by exactly one '
					'equation.'.format(', '.join(what), label))

	A = make_matrix(StateEqsFinal, states)
	B = make_matrix(StateEqsFinal, inputs)
	C = make_matrix(OutputEqsFinal, states)
	D = make_matrix(OutputEqsFinal, inputs)
	E = make_matrix(StateEqsFinal, inputs, True)
	F_ = make_matrix(OutputEqsFinal, inputs, True)

	Bp = A * E + B
	Dp = C * E + D

	matrices = (A, B, C, D, E, F_)
	linear = all(not M.atoms(AppliedUndef) and t not in M.free_symbols
		for M in matrices)
	if linear:
		x = sympy.Matrix(len(states), 1, states)
		u = sympy.Matrix(len(inputs), 1, inputs)
		du = sympy.Matrix(len(inputs), 1, [v.diff(t) for v in inputs])
		f = sympy.Matrix(len(StateEqsFinal), 1, StateEqsFinal)
		h = sympy.Matrix(len(OutputEqsFinal), 1, OutputEqsFinal)
		residual = list(f - A * x - B * u - E * du) \
			+ list(h - C * x - D * u - F_ * du)
		linear = all(sympy.cancel(r) == 0 or sympy.simplify(r) == 0
			for r in residual)

	TF = None
	if linear and transfer_function:
		TF = _transfer_function(A, Bp, C, Dp + F_ * s)

	params = set()
	for e in StateEqsFinal + OutputEqsFinal:
		params |= e.free_symbols
	params.discard(t)
	if s in params:
		raise StateMintError(
			'"s" is the Laplace variable and cannot be a parameter name.')

	result = output()
	result.A = A
	result.B = B
	result.C = C
	result.D = D
	result.E = E
	result.F = F_
	result.Bp = Bp
	result.Dp = Dp
	result.TF = TF
	result.StateVec = sympy.Matrix(len(states), 1, make_vec(states))
	result.OutputVec = sympy.Matrix(len(outputs), 1, make_vec(outputs))
	result.StateEq = sympy.Matrix(len(StateEqsFinal), 1, StateEqsFinal)
	result.OutEq = sympy.Matrix(len(OutputEqsFinal), 1, OutputEqsFinal)
	result.InputVec = sympy.Matrix(len(inputs), 1, make_vec(inputs))
	result.Parameters = sorted(params, key=str)
	result.Linear = linear
	result.Nonstandard = any(e != 0 for e in E) or any(f != 0 for f in F_)
	return result
