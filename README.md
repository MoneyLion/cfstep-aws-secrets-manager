# Codefresh custom step for AWS Secrets Manager

A Codefresh custom step to fetch secrets from AWS Secrets Manager.

View [changelog](./CHANGELOG.md).

## Usage

Include this step in your pipeline, for example:

```yaml
steps:
  FetchSecrets:
    title: Fetch secrets from AWS Secrets Manager
    type: moneylion/aws-secrets-manager
    arguments:
      secrets:
        - secret_arn: arn:aws:secret-1
          key: username
          store_in: USERNAME
        - secret_arn: arn:aws:secret-2
          key: password
          store_in: PASSWORD
  UseSecrets:
    title: Use the fetched secrets
    type: freestyle
    arguments:
      image: 'alpine'
      commands:
        # Access your secrets via $USERNAME and $PASSWORD
        - ...
```

This fetches the secrets, and places the referenced values into the environment variables `USERNAME` and `PASSWORD`, which can then be used in the subsequent steps within the pipeline.

### Step input

Specify the list of secrets to be fetched, under the `secrets` input parameter. Each secret is a map containing:

  - Secret's ARN
  - JSON object key
  - Environment variable to store the referenced secret value in

For example, given the secret with an ARN `arn:aws:secret-1`, and a secret value:

```json
{
  "username": "admin",
  "password": "str0ngpassword"
}
```

Specifying this as one of the secrets:

```yaml
arguments:
  secrets:
    - secret_arn: arn:aws:secret-1
      key: username
      store_in: USERNAME
```

Fetches the secret, retrieves the JSON value under the key `username`, and store that value in the `USERNAME` environment variable. `$USERNAME` will now contain the value `admin`.

### Authenticating with AWS

The custom step uses AWS SDK for Python (Boto3) with the default configuration. This means for authenticating with AWS, you may:

  - Use static AWS credentials via environment variable, e.g. `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
  - Use shared configuration files, e.g. `AWS_PROFILE`.

To assume an IAM role before fetching secrets, you may specify the role's ARN via `AWS_IAM_ROLE_ARN` input parameter:

```yaml
arguments:
  AWS_IAM_ROLE_ARN: 'arn:aws:role/some-role'  # Like this
  secrets:
    - secret_arn: arn:aws:secret-1
      key: username
      store_in: USERNAME
```

## Development note

Ensure the following is installed:

  - Docker
  - Codefresh CLI

### Setting up Codefresh CLI

Create two API keys, one for your personal account (to test your changes), and one for MoneyLion account (to deploy and release official version). The API keys should have the following scopes:

  - `Step-type:write`, for creating the step on Codefresh.
  - `Pipeline:run`, for running the pipeline directly on the command line.

Once the keys are ready, create the authentication contexts on your local machine:

```
codefresh auth create-context personal --api-key <API_KEY_FOR_PERSONAL>
codefresh auth create-context moneylion --api-key <API_KEY_FOR_MONEYLION>
```

### Docker image

Build and push the docker image:

```
docker build . -t <tag>
docker push <tag>
```

### Create and update step

For testing, ensure the `personal` authentication context is used. Check the current context via:

```
codefresh auth current-context
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

  1. Push the commits and tags.

  1. Build the Docker image with the new version in its tag.

  1. Push the Docker image to registry.

  1. Now publish the new step to Codefresh. Run `codefresh replace step-type <STEP_NAME> -f step.yaml`.
