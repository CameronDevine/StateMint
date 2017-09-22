import boto3

def update(
	Name = None,
	ResourceName = None,
	LambdaArn = None,
	Description = ''):

	if Name is None:
		raise ValueError('Name not set')
	if ResourceName is None:
		raise ValueError('ResourceName not set')
	if LambdaArn is None:
		raise ValueError('LambdaArn not set')

	session = boto3.session.Session()
	region = session.region_name

	apigClient = boto3.client('apigateway')

	print 'Finding API'
	resp = apigClient.get_rest_apis()
	apiId = ''
	for item in resp['items']:
		if item['name'] == Name:
			print 'API Found'
			apiId = item['id']
			break

	if apiId == '':
		print 'API not found'
		print 'Creating API'
		resp = apigClient.create_rest_api(
			name = Name,
			description = Description)
		apiId = resp['id']

	print 'Finding Resource'
	resp = apigClient.get_resources(
		restApiId = apiId)
	resourceId = ''
	rootResourceId = ''
	for item in resp['items']:
		if item['path'] == '/' + ResourceName:
			print 'Resource Found'
			resourceId = item['id']
		elif item['path'] == '/':
			rootResourceId = item['id']
		else:
			print 'Deleting Unused Resource'
			apigClient.delete_resource(
				restApiId = apiId,
				resourceId = item['id'])

	if resourceId == '':
		print 'Resource not found'
		print 'Creating Resource'
		resp = apigClient.create_resource(
			restApiId = apiId,
			parentId = rootResourceId,
			pathPart = ResourceName)
		resourceId = resp['id']

	print 'Finding POST Method'
	try:
		resp = apigClient.get_method(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'POST')
		print 'Found POST Method'
		print 'CHECK'
	except apigClient.exceptions.NotFoundException:
		print 'POST Method not found'
		print 'Creating POST Method'
		apigClient.put_method(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'POST',
			authorizationType = 'NONE',
			apiKeyRequired = False)

	try:
		apigClient.put_method_response(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'POST',
			statusCode = '200',
			responseParameters = {
				'method.response.header.Access-Control-Allow-Origin': False},
			responseModels = {
				'application/json': 'Empty'})
	except apigClient.exceptions.ConflictException:
		print 'already exists'

	try:
		apigClient.put_method_response(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'POST',
			statusCode = '400',
			responseParameters = {
				'method.response.header.Access-Control-Allow-Origin': False},
			responseModels = {
				'application/json': 'Empty'})
	except apigClient.exceptions.ConflictException:
		print 'already exists'

	try:
		apigClient.put_integration(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'POST',
			type = 'AWS_PROXY',
			uri = 'arn:aws:apigateway:' + region + ':lambda:path/2015-03-31/functions/' + LambdaArn + '/invocations',
			passthroughBehavior = 'WHEN_NO_MATCH',
			contentHandling = 'CONVERT_TO_TEXT',
			integrationHttpMethod = 'POST')
	except apigClient.exceptions.ConflictException:
		print 'already exists'

	try:
		apigClient.put_integration_response(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'POST',
			statusCode = '200',
			responseParameters = {
				'method.response.header.Access-Control-Allow-Origin': "'*'"},
			responseTemplates = {
				'application/json': 'None'})
	except apigClient.exceptions.ConflictException:
		print 'already exists'


	print 'Finding OPTIONS Method'
	try:
		resp = apigClient.get_method(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'OPTIONS')
		print 'Found OPTIONS Method'
		print 'CHECK'
	except apigClient.exceptions.NotFoundException:
		print 'OPTIONS Method not found'
		print 'Creating OPTIONS Method'
		apigClient.put_method(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'OPTIONS',
			authorizationType = 'NONE',
			apiKeyRequired = False,
			)

	try:
		apigClient.put_method_response(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'OPTIONS',
			statusCode = '200',
			responseParameters = {
				'method.response.header.Access-Control-Allow-Origin': False,
				'method.response.header.Access-Control-Allow-Methods': False,
				'method.response.header.Access-Control-Allow-Headers': False},
			responseModels = {
				'application/json': 'Empty'})
	except apigClient.exceptions.ConflictException:
		print 'already exists'

	try:
		apigClient.put_integration(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'OPTIONS',
			type = 'MOCK',
			passthroughBehavior = 'WHEN_NO_MATCH',
			requestTemplates = {'application/json': '{"statusCode": 200}'})
	except apigClient.exceptions.ConflictException:
		print 'already exists'

	try:
		apigClient.put_integration_response(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'OPTIONS',
			statusCode = '200',
			responseParameters = {
				'method.response.header.Access-Control-Allow-Origin': "'*'",
				'integration.response.header.Access-Control-Allow-Methods': "'POST,OPTIONS'",
				'integration.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"},
			responseTemplates = {
				'application/json': 'None'})
	except apigClient.exceptions.ConflictException:
		print 'already exists'
