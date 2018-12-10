from sys import exc_info
from sympy import latex, octave_code, mathematica_code, zeros, Function
from StateMint import Solve
import json

nocode = {'LaTeX': [], 'Matlab': ['StateVec', 'OutputVec', 'TF', 'OutEq', 'StateEq', 'InputVec'], 'Mathematica': ['StateVec', 'OutputVec', 'TF', 'InputVec'], 'Python': ['StateVec', 'OutputVec', 'TF', 'InputVec']}

converter = {'LaTeX': latex, 'Matlab': octave_code, 'Mathematica': (lambda x: mathematica_code(x.tolist())), 'Python': (lambda x: str(x.tolist()))}

def handler(event, context):
	try:
		data = event["queryStringParameters"]
		#print data
		model = vars(
			Solve(
				data["InVars"].split(','),
				data["StVarElEqns"].split(','),
				data["OtherElEqns"].split(','),
				data["Constraints"].split(','),
				data["OutputVars"].split(',')))
		#print "Model Created"
		body = {'LaTeX': {}, 'Matlab': {}, 'Mathematica': {}, 'Python': {}}
		for key in model:
			for lang in body:
				if key not in nocode[lang]:
					body[lang][key] = converter[lang](model[key])

		#print "Output Converted"

		body['Nonstandard'] = False
		if model['E'] != zeros(*model['E'].shape):
			body['Nonstandard'] = True
		if model['F'] != zeros(*model['F'].shape):
			body['Nonstandard'] = True

		body['Nonlinear'] = False
		if len(model['A'].atoms(Function)) != 0:
			body['Nonlinear'] = True
			del body['Matlab']

		#print "Alerts Found"

		return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}, 'body': json.dumps(body)}

	except:
		estr = ""
		for e in exc_info():
			estr += str(e) + '\n'
		print estr
		return {"statusCode": 400, 'headers': {'Access-Control-Allow-Origin': '*'}, "body": "Failed"}
