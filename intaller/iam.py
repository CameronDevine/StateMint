import boto3
import json

LambdaPolicyData = '''{
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

AssumeRolePolicyData = '''{
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

iamResource = boto3.resource('iam')
iamClient = boto3.client('iam')

print 'Finding IAM Policy'
policies = iamClient.list_policies(MaxItems = 500)
if policies['IsTruncated']:
	print 'Truncated Response! Increase Max Items!'
policyArn = ''
for policy in policies['Policies']:
	if policy['PolicyName'] == 'StateModelRnDLambdaPolicy':
		print 'Found IAM Policy'
		policyArn = policy['Arn']
		break

if policyArn == '':
	print 'IAM Policy not found'
	print 'Creating IAM Policy'
	LambdaPolicy = iamResource.create_policy(
		PolicyName = 'StateModelRnDLambdaPolicy',
		PolicyDocument = LambdaPolicyData,
		Description = 'Allows write access to CloudWatch logs for the StateModelRnD lambda function')
else:
	LambdaPolicy = iamResource.Policy(policyArn)
	if LambdaPolicy.default_version.document == json.loads(LambdaPolicyData):
		print 'Policy up to date'
	else:
		print 'Updating IAM Policy'
		LambdaPolicy.create_version(
			PolicyDocument = LambdaPolicyData,
			SetAsDefault = True)
		for version in LambdaPolicy.versions.all():
			if not version.is_default_version:
				version.delete()

print 'Finding IAM Role'
try:
	role = iamResource.Role('StateModelRnDLambda')
	role.arn
	print 'Found IAM Role'
	print 'Checking IAM Assume Role Policy'
	if role.assume_role_policy_document == json.loads(AssumeRolePolicyData):
		print 'IAM Assume Role Policy up to date'
	else:
		print 'Updating IAM Assume Role Policy'
		role.AssumeRolePolicy().update(PolicyDocument = AssumeRolePolicyData)
except iamResource.meta.client.exceptions.NoSuchEntityException:
	print 'IAM Role not found'
	print 'Creating IAM Role'
	role = iamResource.create_role(
		RoleName = 'StateModelRnDLambda',
		AssumeRolePolicyDocument = AssumeRolePolicyData)

print 'Checking for Attached IAM Policy'
policyFound = False
for policy in role.attached_policies.all():
	if policy.policy_name == 'StateModelRnDLambdaPolicy':
		print 'Found Attached IAM Policy'
		policyFound = True
	else:
		print 'Deataching incorrect IAM Policy'
		policy.detach_role(RoleName = 'StateModelRnDLambda')
if not policyFound:
	print 'Attaching IAM Policy'
	role.attach_policy(PolicyArn = LambdaPolicy.arn)
