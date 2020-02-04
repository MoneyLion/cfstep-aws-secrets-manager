# Codefresh custom step for AWS Secrets Manager

A custom step to fetch secrets from AWS Secrets Manager.

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

To update the step after modification to step source is done:

```
codefresh replace step-type <STEP_NAME> -f step.yaml
```

For step testing, it can be convenient to run the step directly on the command line:

```
codefresh run <PROJECT>/<PIPELINE>
```
