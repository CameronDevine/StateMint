import boto3
import os
import uuid

def function(
	Name = None,
	RoleArn = None,
	Handler = None,
	Description = '',
	Timeout = 10,
	MemorySize = 768,
	ZipLocation = None):

	if Name is None:
		raise ValueError('Name not set')
	if RoleArn is None:
		raise ValueError('RoleArn not set')
	if Handler is None:
		raise ValueError('Handler not set')
	if ZipLocation is None:
		raise ValueError('ZipLocation not set')

	lambdaClient = boto3.client('lambda')

	print 'Finding Lambda function'
	try:
		lambdaFunction = lambdaClient.get_function(FunctionName = Name)
		print 'Lambda function found'
		print 'Checking Lambda function'
		if lambdaFunction['Configuration']['Handler'] != Handler:
			lambdaClient.update_function_configuration(
				FunctionName = Name,
				Handler = Handler)
			print 'Updated handler'
		if lambdaFunction['Configuration']['MemorySize'] != MemorySize:
			lambdaClient.update_function_configuration(
				FunctionName = Name,
				MemorySize = MemorySize)
			print 'Updated memory size'
		if lambdaFunction['Configuration']['Role'] != RoleArn:
			lambdaClient.update_function_configuration(
				FunctionName = Name,
				Role = RoleArn)
			print 'Updated IAM Role'
		if lambdaFunction['Configuration']['Runtime'] != 'python2.7':
			lambdaClient.update_function_configuration(
				FunctionName = Name,
				Runtime = 'python2.7')
			print 'Updated runtime'
		if lambdaFunction['Configuration']['Timeout'] != Timeout:
			lambdaClient.update_function_configuration(
				FunctionName = Name,
				Timeout = Timeout)
			print 'Updated timeout'
		if lambdaFunction['Configuration']['CodeSize'] != os.path.getsize(ZipLocation):
			print 'Updating function code'
			zipfile = open(ZipLocation, 'r')
			zipcontents = zipfile.read()
			zipfile.close()
			lambdaClient.update_function_code(
				FunctionName = Name,
				ZipFile = zipcontents,
				Publish = True)
			print 'Function code updated'
		print 'Lambda function up to date'
	except lambdaClient.exceptions.ResourceNotFoundException:
		print 'Lambda function not found'
		print 'Creating Lambda function'
		zipfile = open(ZipLocation, 'r')
		zipcontents = zipfile.read()
		zipfile.close()
		lambdaClient.create_function(
			FunctionName = Name,
			Runtime = 'python2.7',
			Role = RoleArn,
			Handler = Handler,
			Code = {'ZipFile': zipcontents},
			Description = Description,
			Timeout = Timeout,
			MemorySize = MemorySize,
			Publish = True)
		print 'Lambda function created'

	return lambdaFunction['Configuration']['FunctionArn']

def permission(
	Name = None):

	if Name is None:
		raise ValueError('Name not set')

	lambdaClient = boto3.client('lambda')

	print 'Setting Lambda function invoke permissions'
	lambdaClient.add_permission(
		FunctionName = Name,
		StatementId = uuid.uuid4().hex,
		Action = 'lambda:InvokeFunction',
		Principal = 'apigateway.amazonaws.com')
