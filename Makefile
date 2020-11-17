.SUFFIXES:

.PHONY: all
all: publish replace run

.PHONY: publish
publish:
	@docker build . -t cfstep
	@docker tag cfstep raphx/cfstep-aws-secrets-manager
	@docker push raphx/cfstep-aws-secrets-manager

.PHONY: run
run:
	@codefresh run default/FirstPipeline

.PHONY: replace
replace:
	@codefresh replace step-type moneylion/aws-secrets-manager -f step.yaml

.PHONY: create
create:
	@codefresh create step-type moneylion/aws-secrets-manager -f step.yaml
