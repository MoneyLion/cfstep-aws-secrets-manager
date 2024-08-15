.SUFFIXES:

.PHONY: dev
dev:
	podman build --platform linux/amd64 . -t moneylioneng/cfstep-aws-secrets-manager
	podman push moneylioneng/cfstep-aws-secrets-manager
	codefresh replace step-type moneylion/aws-secrets-manager-dev -f step-dev.yaml

.PHONY: testdev
testdev:
	codefresh run security/security-cfstep-dev

.PHONY: prod
prod:
	podman build --platform linux/amd64 . -t moneylioneng/cfstep-aws-secrets-manager:$$TAG
	podman push moneylioneng/cfstep-aws-secrets-manager:$$TAG
	codefresh replace step-type moneylion/aws-secrets-manager -f step.yaml

.PHONY: testprod
testprod:
	codefresh run security/security-cfstep
