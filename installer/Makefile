SHELL := bash
.PHONY: all zip package deploy clean remove

all:
	zip package deploy

zip:
	mkdir -p lambda
	pip install --upgrade sympy mpmath -t lambda/
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
	aws cloudformation package --template-file StateModelRnD.yml --s3-bucket statemodelrnd --output-template-file package.yml

deploy:
	aws cloudformation deploy --stack-name statemodelrnd --template-file package.yml --capabilities CAPABILITY_IAM

clean:
	rm -rf lambda
	rm -f lambda.zip
	rm -f package.yml
	for line in $$(aws s3 ls); do \
		if [ "$$line" == "statemodelrnd" ]; then \
			aws s3 rb s3://statemodelrnd --force; \
			break; \
		fi; \
	done

remove:
	aws cloudformation delete-stack --stack-name statemodelrnd
