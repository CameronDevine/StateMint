SHELL := bash
.PHONY: zip package deploy sdk clean remove test check

all: depends zip package deploy sdk

depends:
	pip install --upgrade sympy mpmath -t aws/lambda/
	cp -r ../python/Statum aws/lambda/

zip:
	cd aws/lambda; zip -r ../lambda.zip *

package: check
	found="false"; \
	for line in $$(aws s3 ls); do \
		if [ "$$line" == "statum" ]; then \
			found="true"; \
			break; \
		fi; \
	done; \
	if [ "$$found" == "false" ]; then \
		aws s3 mb s3://statum; \
	fi
	echo "$(shell \
		export account=$$(aws sts get-caller-identity | grep Account | cut -d '"' -f 4); \
		export region=`aws configure get region`; \
		envsubst '$$account $$region' < aws/api-template.yml > aws/api.yml)"
	aws cloudformation package --template-file aws/Statum.yml --s3-bucket statum --output-template-file aws/package.yml

deploy: check
	aws cloudformation deploy --stack-name statum --template-file aws/package.yml --capabilities CAPABILITY_IAM

sdk: check
	aws apigateway get-sdk --rest-api-id $$(aws cloudformation describe-stacks --stack-name statum | grep OutputValue | cut -d '"' -f 4) --stage-name Stage2 --sdk-type javascript HTML/assets/sdk.zip
	cd HTML/assets/; unzip -o sdk.zip; rm sdk.zip; rm apiGateway-js-sdk/README.md

clean: check
	cd aws/lambda; ls | grep -v StatumLambda.py | xargs rm -r
	rm -f aws/lambda.zip
	rm -f aws/package.yml
	rm -f aws/api.yml
	rm -rf HTML/assets/apiGateway-js-sdk
	for line in $$(aws s3 ls); do \
		if [ "$$line" == "statum" ]; then \
			aws s3 rb s3://statum --force; \
			break; \
		fi; \
	done

remove: check
	aws cloudformation delete-stack --stack-name statum

test:
	sudo env "PATH=$$PATH" python tests.py $(tests)

check:
	if [ $$(which aws) == "" ]; then \
		pip install awscli; \
	fi
	if ! aws sts get-caller-identity; then \
		aws configure; \
	fi
