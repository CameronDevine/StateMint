import boto3
import StringIO
import zipfile

def download(session,
	apiId = None,
	stageName = None):

	if apiId is None:
		raise ValueError('apiId not set')
	if stageName is None:
		raise ValueError('stageName not set')

	apigClient = session.client('apigateway')

	print 'Downloading API Gateway SDK'
	resp = apigClient.get_sdk(
		restApiId = apiId,
		stageName = stageName,
		sdkType = 'javascript')

	zipdata = StringIO.StringIO(resp['body'].read())

	print 'Unzipping API Gateway SDK'
	apiZip = zipfile.ZipFile(zipdata)
	apiZip.extractall(path = '../HTML/')
