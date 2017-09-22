import iam

print "======== Installing StateModelRnD ========"

print "-------- Adding an IAM Rule for the Lambda function --------"

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

iam.role(
	RoleName = 'StateModelRnDLambda',
	PolicyName = 'StateModelRnDLambda',
	PolicyDocument = LambdaPolicyDocument,
	AssumeRolePolicyDocument = LambdaAssumeRolePolicyDocument,
	PolicyDescription = 'Allows write access to CloudWatch logs for the StateModelRnD Lambda function')

print "-------- Adding an IAM Rule for the API Gateway --------"

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

iam.role(
	RoleName = 'StateModelRnDAPIG',
	PolicyName = 'StateModelRnDAPIG',
	PolicyDocument = APIGPolicyDocument,
	AssumeRolePolicyDocument = APIGAssumeRolePolicyDocument,
	PolicyDescription = 'Allows write access to CloudWatch logs for the StateModelRnD API Gateway')

print "======== Complete ========"
