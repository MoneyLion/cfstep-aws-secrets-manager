# Codefresh custom step for AWS Secrets Manager

A Codefresh custom step to fetch secrets from AWS Secrets Manager.

## Development note

Ensure the following is installed:

  - Docker
  - Codefresh CLI

Build and push the docker image:

```
docker build . -t <tag>
docker push <tag>
```

Create the Codefresh custom step:

```
codefresh create step-type <STEP_NAME> -f step.yaml
```

If the custom step is already created, and the step implementation is amended, run instead:

```
codefresh replace step-type <STEP_NAME> -f step.yaml
```

For step testing, it can be convenient to run the pipeline containing the step directly on the command line:

```
codefresh run <PROJECT>/<PIPELINE>
```
