SHELL := bash
.PHONY: zip package deploy sdk clean remove check

all: depends zip package deploy sdk

depends:
	pip install --upgrade sympy mpmath -t aws/lambda/
	cp -r ../python/StateModelRnD aws/lambda/

zip:
	cd aws/lambda; zip -r ../lambda.zip *

package: check
	found="false"; \
	for line in $$(aws s3 ls); do \
		if [ "$$line" == "statemodelrnd" ]; then \
			found="true"; \
			break; \
		fi; \
	done; \
	if [ "$$found" == "false" ]; then \
		aws s3 mb s3://statemodelrnd; \
	fi
	echo "$(shell \
		export account=$$(aws sts get-caller-identity | grep Account | cut -d '"' -f 4); \
		export region=`aws configure get region`; \
		envsubst '$$account $$region' < aws/api-template.yml > aws/api.yml)"
	aws cloudformation package --template-file aws/StateModelRnD.yml --s3-bucket statemodelrnd --output-template-file aws/package.yml

deploy: check
	aws cloudformation deploy --stack-name statemodelrnd --template-file aws/package.yml --capabilities CAPABILITY_IAM

sdk: check
	aws apigateway get-sdk --rest-api-id $$(aws cloudformation describe-stacks --stack-name statemodelrnd | grep OutputValue | cut -d '"' -f 4) --stage-name Stage2 --sdk-type javascript HTML/assets/sdk.zip
	cd HTML/assets/; unzip -o sdk.zip; rm sdk.zip; rm apiGateway-js-sdk/README.md

clean: check
	cd aws/lambda; ls | grep -v StateModelLambda.py | xargs rm -r
	rm -f aws/lambda.zip
	rm -f aws/package.yml
	rm -f aws/api.yml
	rm -rf HTML/assets/apiGateway-js-sdk
	for line in $$(aws s3 ls); do \
		if [ "$$line" == "statemodelrnd" ]; then \
			aws s3 rb s3://statemodelrnd --force; \
			break; \
		fi; \
	done

remove: check
	aws cloudformation delete-stack --stack-name statemodelrnd

check:
	if [ $$(which aws) == "" ]; then \
		pip install awscli; \
	fi
	if ! aws sts get-caller-identity; then \
		aws configure; \
	fi