.SUFFIXES:

.PHONY: dev
dev:
	docker build . -t moneylioneng/cfstep-aws-secrets-manager
	docker push moneylioneng/cfstep-aws-secrets-manager
	codefresh replace step-type moneylion/aws-secrets-manager-dev -f step-dev.yaml

.PHONY: testdev
testdev:
	codefresh run security/security-cfstep-dev

.PHONY: prod
prod:
	docker build . -t moneylioneng/cfstep-aws-secrets-manager:$$TAG
	docker push moneylioneng/cfstep-aws-secrets-manager:$$TAG
	codefresh replace step-type moneylion/aws-secrets-manager -f step.yaml

.PHONY: testprod
testprod:
	codefresh run security/security-cfstep
