import boto3

def update(session,
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

	region = session.region_name

	modified = False

	apigClient = session.client('apigateway')

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
		modified = True
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
			modified = True
			apigClient.delete_resource(
				restApiId = apiId,
				resourceId = item['id'])

	if resourceId == '':
		print 'Resource not found'
		print 'Creating Resource'
		modified = True
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
		if resp['authorizationType'] != 'NONE':
			modified = True
			apigClient.update_method(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'POST',
				patchOperations = [{
					'op': 'replace',
					'path': '/authorizationType',
					'value': 'NONE'}])
			print 'Updated Authorization Type'
		if resp['apiKeyRequired'] != False:
			modified = True
			apigClient.update_method(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'POST',
				patchOperations = [{
					'op': 'replace',
					'path': '/apiKeyRequired',
					'value': False}])
			print 'Updated Authorization Type'
		print 'POST Method up to date'
	except apigClient.exceptions.NotFoundException:
		print 'POST Method not found'
		print 'Creating POST Method'
		modified = True
		apigClient.put_method(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'POST',
			authorizationType = 'NONE',
			apiKeyRequired = False)

	print 'Finding POST Method 200 response'
	try:
		resp = apigClient.get_method_response(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'POST',
			statusCode = '200')
		print 'POST Method 200 response found'
		if resp['responseParameters'] != {'method.response.header.Access-Control-Allow-Origin': False}:
			modified = True
			apigClient.update_method_response(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'POST',
				statusCode = '200',
				patchOperations = [{
					'op': 'replace',
					'path': '/responseParameters',
					'value': "{'method.response.header.Access-Control-Allow-Origin': False}"}])
			print 'POST Method 200 response Response Parameters updated'
		if resp['responseModels'] != {'application/json': 'Empty'}:
			modified = True
			apigClient.update_method_response(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'POST',
				statusCode = '200',
				patchOperations = [{
					'op': 'replace',
					'path': '/responseModels',
					'value': "{'application/json': 'Empty'}"}])
			print 'POST Method 200 response Response Parameters updated'
		print 'POST Method 200 response up to date'
	except apigClient.exceptions.NotFoundException:	
		print 'POST Method 200 response not found'
		print 'Creating POST Method 200 response'
		modified = True
		apigClient.put_method_response(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'POST',
			statusCode = '200',
			responseParameters = {
				'method.response.header.Access-Control-Allow-Origin': False},
			responseModels = {
				'application/json': 'Empty'})

	print 'Finding POST Method 400 response'
	try:
		resp = apigClient.get_method_response(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'POST',
			statusCode = '400')
		print 'POST Method 400 response found'
		if resp['responseParameters'] != {'method.response.header.Access-Control-Allow-Origin': False}:
			modified = True
			apigClient.update_method_response(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'POST',
				statusCode = '400',
				patchOperations = [{
					'op': 'replace',
					'path': '/responseParameters',
					'value': "{'method.response.header.Access-Control-Allow-Origin': False}"}])
			print 'POST Method 400 response Response Parameters updated'
		if resp['responseModels'] != {'application/json': 'Empty'}:
			modified = True
			apigClient.update_method_response(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'POST',
				statusCode = '400',
				patchOperations = [{
					'op': 'replace',
					'path': '/responseModels',
					'value': "{'application/json': 'Empty'}"}])
			print 'POST Method 400 response Response Parameters updated'
		print 'POST Method 400 response up to date'
	except apigClient.exceptions.NotFoundException:	
		print 'POST Method 400 response not found'
		print 'Creating POST Method 400 response'
		modified = True
		apigClient.put_method_response(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'POST',
			statusCode = '400',
			responseParameters = {
				'method.response.header.Access-Control-Allow-Origin': False},
			responseModels = {
				'application/json': 'Empty'})

	print 'Finding Integration'
	uri = 'arn:aws:apigateway:' + region + ':lambda:path/2015-03-31/functions/' + LambdaArn + '/invocations'
	try:
		resp = apigClient.get_integration(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'POST')
		print 'Integration Found'
		if resp['type'] != 'AWS_PROXY':
			modified = True
			apigClient.update_integration(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'POST',
				patchOperations = [{
					'op': 'replace',
					'path': '/type',
					'value': 'AWS_PROXY'}])
			print 'Integration Type up to date'
		if resp['uri'] != uri:
			modified = True
			apigClient.update_integration(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'POST',
				patchOperations = [{
					'op': 'replace',
					'path': '/uri',
					'value': uri}])
			print 'Integration URI updated'
		if resp['passthroughBehavior'] != 'WHEN_NO_MATCH':
			modified = True
			apigClient.update_integration(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'POST',
				patchOperations = [{
					'op': 'replace',
					'path': '/passthroughBehavior',
					'value': 'WEHN_NO_MATCH'}])
			print 'Integration Passthrough Behavior updated'
		if resp['contentHandling'] != 'CONVERT_TO_TEXT':
			modified = True
			apigClient.update_integration(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'POST',
				patchOperations = [{
					'op': 'replace',
					'path': '/contentHandling',
					'value': 'CONVERT_TO_TEXT'}])
			print 'Integration Content Handling updated'
		print 'Integration up to date'
	except apigClient.exceptions.NotFoundException:
		print 'Integration not found'
		print 'Creating Integration'
		modified = True
		apigClient.put_integration(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'POST',
			type = 'AWS_PROXY',
			uri = uri,
			passthroughBehavior = 'WHEN_NO_MATCH',
			contentHandling = 'CONVERT_TO_TEXT',
			integrationHttpMethod = 'POST')

	print 'Finding 200 Integration Response'
	try:
		resp = apigClient.get_integration_response(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'POST',
			statusCode = '200')
		print '200 Integration Response found'
		if resp['responseParameters'] != {'method.response.header.Access-Control-Allow-Origin': "'*'"}:
			modified = True
			apigClient.update_integration_response(
				restApiI = apiId,
				resourceId = resourceId,
				httpMethod = 'POST',
				statusCode = '200',
				patchOperations = [{
					'op': 'replace',
					'path': '/responesParameters',
					'value': "{'method.response.header.Access-Control-Allow-Origin': '*'}"}])
			print '200 Intagration Response Response Parameters updated'
		if resp['responseTemplates'] != {'application/json': 'None'}:
			modified = True
			apigClient.update_integration_response(
				restApiI = apiId,
				resourceId = resourceId,
				httpMethod = 'POST',
				statusCode = '200',
				patchOperations = [{
					'op': 'replace',
					'path': '/responseTemplates',
					'value': "{'application/json': 'None'}"}])
			print '200 Intagration Response Response Templates updated'
		print '200 Integration Response up do date'
	except apigClient.exceptions.NotFoundException:
		print '200 Integration Response not found'
		print 'Creating 200 Integration Response'
		modified = True
		apigClient.put_integration_response(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'POST',
			statusCode = '200',
			responseParameters = {
				'method.response.header.Access-Control-Allow-Origin': "'*'"},
			responseTemplates = {
				'application/json': 'None'})

	print 'Finding OPTIONS Method'
	try:
		resp = apigClient.get_method(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'OPTIONS')
		print 'Found OPTIONS Method'
		if resp['authorizationType'] != 'NONE':
			modified = True
			apigClient.update_method(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'OPTIONS',
				patchOperations = [{
					'op': 'replace',
					'path': '/authorizationType',
					'value': 'NONE'}])
			print 'Updated Authorization Type'
		if resp['apiKeyRequired'] != False:
			modified = True
			apigClient.update_method(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'OPTIONS',
				patchOperations = [{
					'op': 'replace',
					'path': '/apiKeyRequired',
					'value': False}])
			print 'Updated Authorization Type'
		print 'OPTIONS Method up to date'
	except apigClient.exceptions.NotFoundException:
		print 'OPTIONS Method not found'
		print 'Creating OPTIONS Method'
		modified = True
		apigClient.put_method(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'OPTIONS',
			authorizationType = 'NONE',
			apiKeyRequired = False)

	print 'Finding OPTIONS Method 200 Response'
	try:
		resp = apigClient.get_method_response(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'OPTIONS',
			statusCode = '200')
		print 'Found OPTIONS Method 200 Response'
		if resp['responseParameters'] != {'method.response.header.Access-Control-Allow-Origin': False, 'method.response.header.Access-Control-Allow-Methods': False, 'method.response.header.Access-Control-Allow-Headers': False}:
			modified = True
			apigClient.update_method_response(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'OPTIONS',
				statusCode = '200',
				patchOperations = [
					{
						'op': 'add',
						'path': '/responseParameters/method.response.header.Access-Control-Allow-Origin',
						'value': 'False'},
					{
						'op': 'add',
						'path': '/responseParameters/method.response.header.Access-Control-Allow-Methods',
						'value': 'False'},
					{
						'op': 'add',
						'path': '/responseParameters/method.response.header.Access-Control-Allow-Headers',
						'value': 'False'}])
			print 'OPTIONS Method 200 Response Response Paramaters updated'
		if resp['responseModels'] != {'application/json': 'Empty'}:
			modified = True
			apigClient.update_method_response(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'OPTIONS',
				statusCode = '200',
				patchOperations = [{
					'op': 'replace',
					'path': '/responseModels',
					'value': "{'application/json': 'Empty'}"}])
			print 'OPTIONS Method 200 Response Response Models updated'
		print 'OPTIONS Method 200 Response up to date'
	except apigClient.exceptions.NotFoundException:
		print 'OPTIONS Method 200 Response not found'
		print 'Creating OPTIONS Method 200 Response'
		modified = True
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

	print 'Finding OPTIONS Method Integration'
	try:
		resp = apigClient.get_integration(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'OPTIONS')
		print 'OPTIONS Method Integration found'
		if resp['type'] != 'MOCK':
			modified = True
			apigClient.update_integration(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'OPTIONS',
				patchOperations = [{
					'op': 'add',
					'path': '/type',
					'value': 'MOCK'}])
			print 'OPTIONS Method Integration Type updated'
		if resp['passthroughBehavior'] != 'WHEN_NO_MATCH':
			modified = True
			apigClient.update_integration(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'OPTIONS',
				patchOperations = [{
					'op': 'add',
					'path': '/passthroughBehavior',
					'value': 'WHEN_NO_MATCH'}])
			print 'OPTIONS Method Integration Passthrough Behavior updated'
		if resp['requestTemplates'] != {'application/json': '{"statusCode": 200}'}:
			modified = True
			apigClient.update_integration(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'OPTIONS',
				patchOperations = [{
					'op': 'add',
					'path': '/requestTemplates/application~1json/statusCode',
					'value': 200}])
			print 'OPTIONS Method Integration Request Templates updated'
		print 'OPTIONS Method Integration up to date'
	except apigClient.exceptions.NotFoundException:
		print 'OPTIONS Method Integration not found'
		print 'Createing OPTIONS Method Integration'
		modified = True
		apigClient.put_integration(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'OPTIONS',
			type = 'MOCK',
			passthroughBehavior = 'WHEN_NO_MATCH',
			requestTemplates = {'application/json': '{"statusCode": 200}'})

	print 'Finding OPTIONS Method Integration 200 Response'
	try:
		resp = apigClient.get_integration_response(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'OPTIONS',
			statusCode = '200')
		print 'OPTIONS Method Integration 200 Response found'	
		if resp['responseParameters'] != {'method.response.header.Access-Control-Allow-Origin': "'*'", 'method.response.header.Access-Control-Allow-Methods': "'POST,OPTIONS'", 'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"}:
			modified = True
			apigClient.update_integration_response(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'OPTIONS',
				statusCode = '200',
				patchOperations = [
					{
						'op': 'add',
						'path': '/responseParameters/method.response.header.Access-Control-Allow-Origin',
						'value': "'*'"},
					{
						'op': 'add',
						'path': '/responseParameters/method.response.header.Access-Control-Allow-Methods',
						'value': "'POST,OPTIONS'"},
					{
						'op': 'add',
						'path': '/responseParameters/method.response.header.Access-Control-Allow-Headers',
						'value': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"}])
			print 'OPTIONS Method Integration 200 Response Response Parameters updated'
		if resp['responseTemplates'] != {'application/json': 'None'}:
			modified = True
			apigClient.update_integration_response(
				restApiId = apiId,
				resourceId = resourceId,
				httpMethod = 'OPTIONS',
				statusCode = '200',
				patchOperations = [{
					'op': 'add',
					'path': '/responseTemplates/application~1json',
					'value': 'None'}])
			print 'OPTIONS Method Integration 200 Response Response Templates updated'
		print 'OPTIONS Method Integration 200 Response up to date'
	except apigClient.exceptions.NotFoundException:
		print 'OPTIONS Method Integration 200 Response not found'
		print 'Creating OPTIONS Method Integration 200 Response'
		modified = True
		apigClient.put_integration_response(
			restApiId = apiId,
			resourceId = resourceId,
			httpMethod = 'OPTIONS',
			statusCode = '200',
			responseParameters = {
				'method.response.header.Access-Control-Allow-Origin': "'*'",
				'method.response.header.Access-Control-Allow-Methods': "'POST,OPTIONS'",
				'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"},
			responseTemplates = {
				'application/json': 'None'})

	if modified:
		resp = apigClient.get_deployments(restApiId = apiId)
		maxDeployment = 0
		for item in resp['items']:
			maxDeployment = max(maxDeployment, int(item['description'][-1]))
		DeploymentNumber = maxDeployment + 1
		apigClient.create_deployment(
			restApiId = apiId,
			stageName = 'stage' + str(DeploymentNumber),
			description = 'deployment' + str(DeploymentNumber),
			cacheClusterEnabled = False)
		return {'modified': modified, 'apiId': apiId, 'stageName': 'stage' + str(DeploymentNumber)}
	else:
		return {'modified': modified}
