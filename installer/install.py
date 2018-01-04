import iam
import Lambda
import apig
import sdk

import boto3

import sys

try:
	profile_name = sys.argv[1]
except IndexError:
	profile_name = None

session = boto3.session.Session(profile_name = profile_name)

print "======== Installing StateModelRnD ========"

print "======== Getting IAM set up ========"

print "-------- Adding IAM Rule for the Lambda function --------"

LambdaPolicyDocument = '''{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }
    ]
}'''

LambdaAssumeRolePolicyDocument = '''{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}'''

lambdaRoleArn = iam.role(session,
	RoleName = 'StateModelRnDLambda',
	PolicyName = 'StateModelRnDLambda',
	PolicyDocument = LambdaPolicyDocument,
	AssumeRolePolicyDocument = LambdaAssumeRolePolicyDocument,
	PolicyDescription = 'Allows write access to CloudWatch logs for the StateModelRnD Lambda function')

print "-------- Adding IAM Rule for API Gateway --------"

APIGPolicyDocument = '''{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Stmt1491535610000",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:FilterLogEvents",
                "logs:GetLogEvents",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}'''

APIGAssumeRolePolicyDocument = '''{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "apigateway.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}'''

APIGRoleArn = iam.role(session,
	RoleName = 'StateModelRnDAPIG',
	PolicyName = 'StateModelRnDAPIG',
	PolicyDocument = APIGPolicyDocument,
	AssumeRolePolicyDocument = APIGAssumeRolePolicyDocument,
	PolicyDescription = 'Allows write access to CloudWatch logs for the StateModelRnD API Gateway')

print "======== Getting the Lambda function set up ========"

LambdaArn = Lambda.function(session,
	Name = 'StateModelRnDtest',
	RoleArn = lambdaRoleArn,
	Handler = 'StateModelLambda.handler',
	Description = 'The Lambda function for StateModelRnD',
	ZipLocation = '../python/StateModelRnD.zip')

print "======== Getting API Gateway set up ========"

apigResp = apig.update(session,
	Name = 'StateModelRnDtest',
	Description = 'The StateModelRnD API',
	LambdaArn = LambdaArn,
	ResourceName = 'StateModelRnD')

if apigResp['modified']:
	print "======== Getting API SDK files ========"

	sdk.download(session,
		apiId = apigResp['apiId'],
		stageName = apigResp['stageName'])

print "======== Complete ========"
