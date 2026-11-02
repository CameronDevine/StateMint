'''Tests for input handling, error reporting and the elimination methods.'''

import functools

import pytest
import sympy
from sympy import Matrix, Symbol, simplify, sympify, zeros

import StateMint
from StateMint import StateMintError, Solve, split_entries

import test_suite


def assert_matrix(got, expected):
	expected = sympify(expected)
	assert got.shape == expected.shape, (got, expected)
	assert simplify(got - expected) == zeros(*expected.shape), (got, expected)


# A force source drives a mass, a spring and a damper in parallel.
MSD = dict(
	InVars=['Fs'],
	StVarElEqns=["vm' = Fm/m", "FK' = K*vK"],
	OtherElEqns=['FB = B*vB'],
	Constraints=['Fm = Fs - FK - FB', 'vK = vm', 'vB = vm'],
	OutputVars=['vm'])


def solve(**changes):
	args = dict(MSD)
	args.update(changes)
	return Solve(**args)


class TestSplitEntries:

	def test_newlines_and_commas(self):
		assert split_entries("a = b,\nc = d\n\n, e") == ['a = b', 'c = d', 'e']

	def test_commas_inside_parentheses(self):
		assert split_entries('y = atan2(a, b), z = Max(a, b)') == [
			'y = atan2(a, b)', 'z = Max(a, b)']

	def test_blank(self):
		assert split_entries('') == []
		assert split_entries(' ,\n ,') == []


class TestInputs:

	def test_basic(self):
		sys = solve()
		assert_matrix(sys.A, 'Matrix([[-B/m, -1/m], [K, 0]])')
		assert_matrix(sys.B, 'Matrix([[1/m], [0]])')
		assert sys.Linear and not sys.Nonstandard
		assert [str(p) for p in sys.Parameters] == ['B', 'K', 'm']

	def test_output_expression(self):
		# The bug this fixes: "FK + FB" was parsed as FK + FB(t) and the
		# FK term was silently dropped.
		sys = solve(OutputVars=['FK + FB', 'm*vm'])
		assert_matrix(sys.C, 'Matrix([[B, 1], [m, 0]])')
		assert_matrix(sys.D, 'Matrix([[0], [0]])')
		assert sys.OutputVec[0] == Symbol('FK') + Symbol('FB') or \
			simplify(sys.OutputVec[0] - Symbol('FB') - Symbol('FK')) == 0

	def test_output_derivative(self):
		sys = solve(OutputVars=["vm'"])
		assert_matrix(sys.C, 'Matrix([[-B/m, -1/m]])')
		assert_matrix(sys.D, 'Matrix([[1/m]])')

	def test_empty_list_and_blank_entries(self):
		# No damper: the web app sent [''] for the empty field.
		sys = Solve(['Fs'], ["vm' = Fm/m", "FK' = K*vK"], [''],
			['Fm = Fs - FK', 'vK = vm', ''], ['vm', ' '])
		assert_matrix(sys.A, 'Matrix([[0, -1/m], [K, 0]])')
		sys = Solve(['Fs'], ["vm' = Fm/m", "FK' = K*vK"], [],
			['Fm = Fs - FK', 'vK = vm'], ['vm'])
		assert_matrix(sys.A, 'Matrix([[0, -1/m], [K, 0]])')

	def test_text_fields_with_trailing_commas(self):
		sys = Solve('Fs,', "vm' = Fm/m,\nFK' = K*vK,", 'FB = B*vB,',
			'Fm = Fs - FK - FB,\nvK = vm,\nvB = vm,', 'vm,')
		assert_matrix(sys.A, 'Matrix([[-B/m, -1/m], [K, 0]])')

	def test_I_is_a_variable(self):
		sys = Solve(['Vs'], ["I' = vL/L"], ['vR = R*iR'],
			['vL = Vs - vR', 'iR = I'], ['I'])
		assert_matrix(sys.A, 'Matrix([[-R/L]])')

	def test_caret_is_power_and_abs(self):
		a = Solve(['Fp'], ["vm' = Fm/m"], ['Fd = cd*vd^2'],
			['Fm = Fp - Fd', 'vd = vm'], ['vm'])
		b = Solve(['Fp'], ["vm' = Fm/m"], ['Fd = cd*vd**2'],
			['Fm = Fp - Fd', 'vd = vm'], ['vm'])
		assert simplify(a.StateEq - b.StateEq) == zeros(1, 1)
		assert not a.Linear and a.TF is None
		c = Solve(['Fp'], ["vm' = Fm/m"], ['Fd = cd*vd*abs(vd)'],
			['Fm = Fp - Fd', 'vd = vm'], ['vm'])
		assert c.StateEq[0].has(sympy.Abs)

	def test_pi_and_functions(self):
		sys = Solve(['u'], ["x' = q"], ['q = 2*pi*f*sin(x) + u'], [], ['x'])
		assert sys.StateEq[0].has(sympy.pi)
		assert not sys.Linear

	def test_affine_is_not_linear(self):
		# A constant term can't be written as Ax + Bu.
		sys = Solve(['u'], ["x' = q"], ['q = -a*x + u + g'], [], ['x'])
		assert not sys.Linear


class TestErrors:

	@pytest.mark.parametrize('bad', [
		"x = __import__('os').system('echo hi')",
		'x = (1).__class__',
		'x = y.real',
		'x = lambda',
		'x = [1, 2]',
		'x = "a"',
		'x = a; import os',
	])
	def test_rejects_code(self, bad):
		with pytest.raises(StateMintError):
			solve(OtherElEqns=['FB = B*vB', bad])

	def test_state_lhs_must_be_derivative(self):
		with pytest.raises(StateMintError, match='derivative'):
			solve(StVarElEqns=['vm = Fm/m', "FK' = K*vK"])

	def test_one_equals_sign(self):
		with pytest.raises(StateMintError, match='exactly one'):
			solve(OtherElEqns=['FB == B*vB'])
		with pytest.raises(StateMintError, match='exactly one'):
			solve(OtherElEqns=['FB B*vB'])

	def test_defined_twice(self):
		with pytest.raises(StateMintError, match='defined twice'):
			solve(Constraints=['Fm = Fs - FK - FB', 'vK = vm', 'vB = vm',
				'FB = 0'])

	def test_reserved_name(self):
		with pytest.raises(StateMintError, match='reserved'):
			solve(OtherElEqns=['sin = B*vB'])

	def test_unknown_output(self):
		with pytest.raises(StateMintError, match='vX'):
			solve(OutputVars=['vX'])

	def test_undetermined(self):
		with pytest.raises(StateMintError, match='not independent'):
			Solve(['u'], ["x' = p1"], ['p1 = p2 + x', 'p2 = p1 - x'], [],
				['x'])

	def test_unbalanced(self):
		with pytest.raises(StateMintError, match='parenthes'):
			solve(OtherElEqns=['FB = B*(vB'])

	def test_bad_input_name(self):
		with pytest.raises(StateMintError, match='not a variable name'):
			solve(InVars=['2Fs'])

	def test_no_equations(self):
		with pytest.raises(StateMintError):
			Solve(['u'], [], [], [], ['u'])


class TestElimination:

	def test_algebraic_loop_of_three(self):
		sys = Solve(['u'], ["x' = p1"],
			['p1 = a*p2 + x', 'p2 = b*p3', 'p3 = c*p1 + u'], [], ['p1'])
		assert_matrix(sys.A, 'Matrix([[1/(1 - a*b*c)]])')
		assert_matrix(sys.B, 'Matrix([[a*b/(1 - a*b*c)]])')

	def test_dependent_mass(self):
		# Two masses moving together: m2 is a dependent storage element.
		sys = Solve(['Fs'], ["v1' = F1/m1"], ["F2 = m2*v2'"],
			['F1 = Fs - F2', 'v2 = v1'], ['v1', 'F2'])
		assert_matrix(sys.A, 'Matrix([[0]])')
		assert_matrix(sys.B, 'Matrix([[1/(m1 + m2)]])')
		assert_matrix(sys.D, 'Matrix([[0], [m2/(m1 + m2)]])')

	def test_derivative_of_primary_variable(self):
		sys = Solve(['u'], ["x' = q + u"], ['p = k*x'], ["q = -p'"], ['x'])
		assert_matrix(sys.B, 'Matrix([[1/(1 + k)]])')

	def test_input_derivative(self):
		# A spring driven by a velocity source through a damper's force:
		# the output picks up the input's derivative.
		sys = Solve(['vs'], ["FK' = K*vK"], ['vB = FB/B'],
			['vK = vs - vB', 'FB = FK'], ['FK', "FK'"])
		assert_matrix(sys.A, 'Matrix([[-K/B]])')
		assert_matrix(sys.B, 'Matrix([[K]])')

	def test_no_states(self):
		sys = Solve(['u'], [], ['y = k*u'], [], ['y'])
		assert_matrix(sys.D, 'Matrix([[k]])')
		assert_matrix(sys.TF, 'Matrix([[k]])')

	def test_methods_agree_on_example(self):
		a = solve(method='linear')
		b = solve(method='substitution')
		for name in 'ABCDEF':
			assert simplify(getattr(a, name) - getattr(b, name)) == \
				zeros(*getattr(a, name).shape)

	def test_bad_method(self):
		with pytest.raises(ValueError):
			solve(method='magic')


class TestTransferFunction:

	def test_msd(self):
		sys = solve(OutputVars=['vm'])
		s = StateMint.StateMint.s
		assert simplify(sys.TF[0] - s / (m * s**2 + B * s + K)) == 0


m, B, K = sympy.symbols('m B K')


class TestSuiteBySubstitution(test_suite.TestStateMint):
	'''Every system in the suite, solved by the original substitution method.
	'''

	def setUp(self):
		self._solve = StateMint.Solve
		StateMint.Solve = functools.partial(self._solve, method='substitution')

	def tearDown(self):
		StateMint.Solve = self._solve


class TestSuiteByLinear(test_suite.TestStateMint):
	'''Every system in the suite that is linear in the eliminated variables,
	solved by the simultaneous linear method alone.'''

	def setUp(self):
		self._solve = StateMint.Solve
		StateMint.Solve = functools.partial(self._solve, method='linear')

	def tearDown(self):
		StateMint.Solve = self._solve
