SHELL := bash
.PHONY: zip package deploy sdk clean remove test check tracking

trackingID = none

all: depends zip package deploy sdk tracking

depends:
	pip install --upgrade sympy mpmath -t aws/lambda/
	cp -r ../python/StateMint aws/lambda/

zip:
	cd aws/lambda; zip -r ../lambda.zip *

package: check
	found="false"; \
	for line in $$(aws s3 ls); do \
		if [ "$$line" == "statemint" ]; then \
			found="true"; \
			break; \
		fi; \
	done; \
	if [ "$$found" == "false" ]; then \
		aws s3 mb s3://statemint; \
	fi
	echo "$(shell \
		export account=$$(aws sts get-caller-identity | grep Account | cut -d '"' -f 4); \
		export region=`aws configure get region`; \
		envsubst '$$account $$region' < aws/api-template.yml > aws/api.yml)"
	aws cloudformation package --template-file aws/StateMint.yml --s3-bucket statemint --output-template-file aws/package.yml

deploy: check
	aws cloudformation deploy --stack-name StateMint --template-file aws/package.yml --capabilities CAPABILITY_IAM

sdk: check
	aws apigateway get-sdk --rest-api-id $$(aws cloudformation describe-stacks --stack-name StateMint | grep OutputValue | cut -d '"' -f 4) --stage-name StateMint --sdk-type javascript HTML/assets/sdk.zip
	cd HTML/assets/; unzip -o sdk.zip; rm sdk.zip; rm apiGateway-js-sdk/README.md

clean: check
	cd aws/lambda; ls | grep -v StateMintLambda.py | xargs rm -r
	rm -f aws/lambda.zip
	rm -f aws/package.yml
	rm -f aws/api.yml
	rm -rf HTML/assets/apiGateway-js-sdk
	for line in $$(aws s3 ls); do \
		if [ "$$line" == "statemint" ]; then \
			aws s3 rb s3://statemint --force; \
			break; \
		fi; \
	done

remove: check
	aws cloudformation delete-stack --stack-name StateMint

test:
	sudo env "PATH=$$PATH" python tests.py $(tests)

check:
	if [ $$(which aws) == "" ]; then \
		pip install awscli; \
	fi
	if ! aws sts get-caller-identity; then \
		aws configure; \
	fi

tracking:
	if [ $(trackingID) == "null" ]; then \
		sed -i "1s/.*/trackingID = null;/" HTML/assets/js/tracking.js; \
	elif [ $(trackingID) != "none" ]; then \
		sed -i "1s/.*/trackingID = '$(trackingID)';/" HTML/assets/js/tracking.js; \
	fi;
