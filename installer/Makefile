SHELL := bash
.PHONY: zip package deploy sdk clean remove

all: depends zip package deploy sdk

depends:
	mkdir -p lambda
	pip install --upgrade sympy mpmath -t lambda/	

zip:
	mkdir -p lambda
	cp -r ../python/StateModelRnD lambda/
	cp ../python/StateModelLambda.py lambda/
	cd lambda; zip -r ../lambda.zip *

package:
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
		envsubst '$$account $$region' < api-template.yml > api.yml)"
	aws cloudformation package --template-file StateModelRnD.yml --s3-bucket statemodelrnd --output-template-file package.yml

deploy:
	aws cloudformation deploy --stack-name statemodelrnd --template-file package.yml --capabilities CAPABILITY_IAM

sdk:
	aws apigateway get-sdk --rest-api-id $$(aws cloudformation describe-stacks --stack-name statemodelrnd | grep OutputValue | cut -d '"' -f 4) --stage-name Stage2 --sdk-type javascript ../HTML/sdk.zip
	cd ../HTML; unzip -o sdk.zip; rm sdk.zip; rm apiGateway-js-sdk/README.md

clean:
	rm -rf lambda
	rm -f lambda.zip
	rm -f package.yml
	rm -f api.yml
	rm -rf ../HTML/apiGateway-js-sdk
	for line in $$(aws s3 ls); do \
		if [ "$$line" == "statemodelrnd" ]; then \
			aws s3 rb s3://statemodelrnd --force; \
			break; \
		fi; \
	done

remove:
	aws cloudformation delete-stack --stack-name statemodelrnd
