import boto3
import json

def role(
	RoleName = None,
	PolicyName = None,
	PolicyDocument = None,
	AssumeRolePolicyDocument = None,
	PolicyDescription = ''):

	if RoleName is None:
		raise ValueError('RuleName not set')
	if PolicyName is None:
		raise ValueError('PolicyName not set')
	if PolicyDocument is None:
		raise ValueError('PolicyName not set')
	if AssumeRolePolicyDocument is None:
		raise ValueError('AssumeRolePolicyDocument not set')

	iamResource = boto3.resource('iam')
	iamClient = boto3.client('iam')

	print 'Finding IAM Policy'
	policies = iamClient.list_policies(MaxItems = 500)
	if policies['IsTruncated']:
		print 'Truncated Response! Increase Max Items!'
	policyArn = ''
	for policy in policies['Policies']:
		if policy['PolicyName'] == PolicyName:
			print 'Found IAM Policy'
			policyArn = policy['Arn']
			break

	if policyArn == '':
		print 'IAM Policy not found'
		print 'Creating IAM Policy'
		policy = iamResource.create_policy(
			PolicyName = PolicyName,
			PolicyDocument = PolicyDocument,
			Description = PolicyDescription)
		policyArn = policy.arn
	else:
		policy = iamResource.Policy(policyArn)
		if policy.default_version.document == json.loads(PolicyDocument):
			print 'Policy up to date'
		else:
			print 'Updating IAM Policy'
			policy.create_version(
				PolicyDocument = PolicyDocument,
				SetAsDefault = True)
			for version in policy.versions.all():
				if not version.is_default_version:
					version.delete()

	print 'Finding IAM Role'
	try:
		role = iamResource.Role(RoleName)
		role.arn
		print 'Found IAM Role'
		print 'Checking IAM Assume Role Policy'
		if role.assume_role_policy_document == json.loads(AssumeRolePolicyDocument):
			print 'IAM Assume Role Policy up to date'
		else:
			print 'Updating IAM Assume Role Policy'
			role.AssumeRolePolicy().update(PolicyDocument = AssumeRolePolicyDocument)
	except iamClient.exceptions.NoSuchEntityException:
		print 'IAM Role not found'
		print 'Creating IAM Role'
		role = iamResource.create_role(
			RoleName = RoleName,
			AssumeRolePolicyDocument = AssumeRolePolicyDocument)

	print 'Checking for Attached IAM Policy'
	policyFound = False
	for policy in role.attached_policies.all():
		if policy.policy_name == PolicyName:
			print 'Found Attached IAM Policy'
			policyFound = True
		else:
			print 'Deataching incorrect IAM Policy'
			policy.detach_role(RoleName = RoleName)
	if not policyFound:
		print 'Attaching IAM Policy'
		role.attach_policy(PolicyArn = policyArn)

	return role.arn
