'''Format a StateMint model for the web interface.

`solve_fields` takes the five text fields of the web interface (as typed, or as
stored in a saved ``.rnd`` file or a share link), solves the system and returns
a JSON-serializable dict with the model written in LaTeX, MATLAB/Octave,
Mathematica and Python. The web interface runs it in the browser with Pyodide;
it is equally usable on a server.
'''

import json

import sympy

from .StateMint import Solve, StateMintError, split_entries

FIELDS = ('InVars', 'StVarElEqns', 'OtherElEqns', 'Constraints', 'OutputVars')
'''The names of the five text fields, in the order `Solve` takes them.'''

MATRICES = ('A', 'B', 'C', 'D', 'E', 'F', 'Bp', 'Dp')
VECTORS = ('StateVec', 'InputVec', 'OutputVec')
EQUATIONS = ('StateEq', 'OutEq')

_nocode = {
	'LaTeX': (),
	'Matlab': ('StateVec', 'OutputVec', 'TF', 'OutEq', 'StateEq', 'InputVec'),
	'Mathematica': ('StateVec', 'OutputVec', 'TF', 'InputVec'),
	'Python': ('StateVec', 'OutputVec', 'TF', 'InputVec'),
}


def _python(m):
	return str(m.tolist())


def _mathematica(m):
	return sympy.mathematica_code(m.tolist())


_converters = {
	'LaTeX': sympy.latex,
	'Matlab': sympy.octave_code,
	'Mathematica': _mathematica,
	'Python': _python,
}


def _convert(lang, m):
	if 0 in m.shape:
		return {
			'LaTeX': r'\left[\right]',
			'Matlab': 'zeros({}, {})'.format(*m.shape),
			'Mathematica': '{}',
			'Python': '[]',
		}[lang]
	return _converters[lang](m)


def format_model(model):
	'''Write a solved model in each output language.

	Args:
		model (StateMint.output): The result of `StateMint.Solve`.

	Returns:
		dict: ``{'LaTeX': {...}, 'Matlab': {...}, 'Mathematica': {...},
		'Python': {...}, 'Nonstandard': bool, 'NonzeroF': bool,
		'Nonlinear': bool, 'Parameters': [...]}``, where each language maps the names of
		`StateMint.output`'s members (A, B, ..., TF, StateEq, ...) to code.
		MATLAB is omitted for nonlinear models, and TF for nonlinear ones.
	'''
	keys = MATRICES + VECTORS + EQUATIONS + (('TF',) if model.TF is not None
		else ())
	# MATLAB code is only offered for linear models: the matrices of a
	# nonlinear one contain functions of time that it has no notation for.
	langs = [lang for lang in _converters
		if model.Linear or lang != 'Matlab']
	body = {}
	for lang in langs:
		body[lang] = dict((key, _convert(lang, getattr(model, key)))
			for key in keys if key not in _nocode[lang])
	body['Nonstandard'] = bool(model.Nonstandard)
	body['NonzeroF'] = any(f != 0 for f in model.F)
	body['Nonlinear'] = not model.Linear
	body['Parameters'] = [sympy.latex(p) for p in model.Parameters]
	return body


def solve_fields(fields, transfer_function=True):
	'''Solve a system given the web interface's five text fields.

	Args:
		fields (dict or str): Maps each name in `FIELDS` to the text of that
			field, in which entries are separated by new lines or by commas
			outside parentheses. A JSON string of such a dict is accepted
			too. Missing fields are taken as empty.
		transfer_function (bool): Whether to compute the transfer function
			(the slow part for large systems).

	Returns:
		dict: `format_model`'s result, or ``{'error': message}`` if the
		equations cannot be read or solved.
	'''
	if isinstance(fields, str):
		fields = json.loads(fields)
	try:
		lists = [split_entries(fields.get(name) or '') for name in FIELDS]
		return format_model(Solve(*lists,
			transfer_function=transfer_function))
	except StateMintError as err:
		return {'error': str(err)}
	except Exception as err:  # a bug in StateMint or SymPy
		return {'error': 'StateMint could not solve this system ({}: {}). '
			'Please report it with your equations.'.format(
				type(err).__name__, err)}


def solve_json(text, transfer_function=True):
	'''`solve_fields` with JSON in and JSON out, for calling from JavaScript.
	'''
	return json.dumps(solve_fields(text, bool(transfer_function)))
