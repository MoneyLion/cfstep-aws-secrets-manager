# Codefresh custom step for AWS Secrets Manager

A Codefresh custom step to fetch secrets from AWS Secrets Manager.

## Development note

Ensure the following is installed:

  - Docker
  - Codefresh CLI

Create a Codefresh API key and set it up on local machine. The API key should have the following scopes:

  - `Step-type:write`, for creating the step on Codefresh.
  - `Pipeline:run`, for running the pipeline directly on the command line.

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

## Publishing

Steps for publishing the custom step:

  1. Bump the custom step version and Docker image version in [step.yaml](./step.yaml).

  1. Make a commit.

  1. Create an annotated tag.

  1. Build the Docker image with the new version in its tag.

  1. Push the Docker image to registry.

  1. Now publish the new step to Codefresh. Run `codefresh replace step-type <STEP_NAME> -f step.yaml`.
