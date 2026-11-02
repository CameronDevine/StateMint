'''Tests for the web interface's formatter, StateMint.web.'''

import json

from StateMint.web import FIELDS, solve_fields, solve_json

# The web interface's built-in example 2 (as typed, with ",\n" separators).
EXAMPLE2 = {
	'InVars': 'Fs',
	'StVarElEqns': "vm' = Fm/m,\nFK1' = K1 * vK1",
	'OtherElEqns': "FB2 = B2 * vB2,\nvB1 = FB1/B1,\nvK2 = FK2' / K2",
	'Constraints': 'vK1 = vK2 - vB1,\nvB2 = vm,\nFK2 = Fs - FK1,\nFB1 = FK1,\n'
		'Fm = Fs - FB2',
	'OutputVars': 'vB1',
}


def test_example2_nonstandard():
	body = solve_fields(EXAMPLE2)
	assert 'error' not in body
	assert body['Nonstandard'] and not body['Nonlinear']
	for lang in ('LaTeX', 'Matlab', 'Mathematica', 'Python'):
		for key in ('A', 'B', 'C', 'D', 'E', 'F', 'Bp', 'Dp'):
			assert body[lang][key]
	assert 'TF' in body['LaTeX'] and 'TF' not in body['Matlab']
	assert sorted(body['Parameters']) == ['B_{1}', 'B_{2}', 'K_{1}', 'K_{2}', 'm']
	json.dumps(body)


def test_empty_field_is_not_an_error():
	# A force source, a mass and a spring: no other elemental equations.
	# The old AWS backend answered this with HTTP 400 "Failed".
	body = solve_fields({
		'InVars': 'Fs', 'StVarElEqns': "vm' = Fm/m,\nFK' = K*vK",
		'OtherElEqns': '', 'Constraints': 'Fm = Fs - FK,\nvK = vm,',
		'OutputVars': 'vm'})
	assert 'error' not in body
	assert body['Python']['A'] == '[[0, -1/m], [K, 0]]'


def test_nonlinear_example3():
	body = solve_fields({
		'InVars': 'Fp, Fr', 'StVarElEqns': "vm' = Fm / m",
		'OtherElEqns': 'Fd = cd * vd**2',
		'Constraints': 'Fm = Fp - Fr - Fd,\nvd = vm', 'OutputVars': 'vm'})
	assert body['Nonlinear']
	assert 'Matlab' not in body and 'TF' not in body['LaTeX']
	assert 'StateEq' in body['LaTeX']


def test_error_message():
	body = solve_fields(dict(EXAMPLE2, OutputVars='vX'))
	assert 'vX' in body['error']


def test_json_round_trip():
	body = json.loads(solve_json(json.dumps(EXAMPLE2)))
	assert body['Nonstandard']


def test_missing_fields():
	body = solve_fields({'InVars': 'u', 'OtherElEqns': 'y = k*u',
		'OutputVars': 'y'})
	assert body['Python']['D'] == '[[k]]'
	assert set(FIELDS) >= {'InVars', 'OutputVars'}
