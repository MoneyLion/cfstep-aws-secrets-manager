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
