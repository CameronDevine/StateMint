import boto3

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

iam = boto3.resource('iam')

role = iam.Role('StateModelRnDLambda')

try:
	for policy in role.policies.all():
		if policy.policy_document == LambdaPolicyData:
			print 'StateModelRnDLambda IAM policy up to date'
		else:
			print 'update policy'
except iam.meta.client.exceptions.NoSuchEntityException:
	LambdaPolicy = iam.create_policy(
		PolicyName = 'StateModelRnDLambdaPolicy',
		PolicyDocument = LambdaPolicyData,
		Description = 'Allows write access to CloudWatch logs for the StateModelRnD lambda function')
	role = iam.create_role(
		RoleName = 'StateModelRnDLambda',
		AssumeRolePolicyDocument = AssumeRolePolicyData)
	role.attach_policy(
		PolicyArn = LambdaPolicy.arn)
