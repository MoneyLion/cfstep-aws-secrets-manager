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
      AWS_ACCESS_KEY_ID: ${{AWS_ACCESS_KEY_ID}}
      AWS_SECRET_ACCESS_KEY: ${{AWS_SECRET_ACCESS_KEY}}
      AWS_DEFAULT_REGION: a-region-1
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
  AWS_ACCESS_KEY_ID: ${{AWS_ACCESS_KEY_ID}}
  AWS_SECRET_ACCESS_KEY: ${{AWS_SECRET_ACCESS_KEY}}
  AWS_DEFAULT_REGION: a-region-1
  secrets:
    - secret_arn: arn:aws:secret-1
      key: username
      store_in: USERNAME
```

Fetches the secret, retrieves the JSON value under the key `username`, and store that value in the `USERNAME` environment variable. `$USERNAME` will now contain the value `admin`.

### Authenticating with AWS

The custom step uses AWS SDK for Python (Boto3) with the default configuration. This means for authenticating with AWS, you may:

  - Use static AWS credentials via environment variable, e.g. `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
  - Specify AWS region via `AWS_DEFAULT_REGION`.

By default, the step will read these environment variables as input from the pipeline variables, but it is still recommended to reference them explicitly in the step's argument.

To assume an IAM role before fetching secrets, you may specify the role's ARN via `AWS_IAM_ROLE_ARN` pipeline variable, or set it through the step's argument:

```yaml
arguments:
  AWS_ACCESS_KEY_ID: ${{AWS_ACCESS_KEY_ID}}
  AWS_SECRET_ACCESS_KEY: ${{AWS_SECRET_ACCESS_KEY}}
  AWS_DEFAULT_REGION: a-region-1
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

Create a Codefresh API key under the MoneyLion Codefresh account. The key should have the following scopes:

  - `step-type:write`, for creating and updating custom steps on Codefresh.
  - `build:read`
  - `pipeline:read`; and
  - `pipeline:run`, for the convenience of triggering pipeline runs directly from local machine.

Once the API key is ready, create an authentication context on your local machine:

```
codefresh auth create-context moneylion --api-key <CODEFRESH_API_KEY>
```

### Working with development version of custom step

The custom step has two versions, a development version, and an official release version. Ensure you are always working with the development version while you are testing your changes.

Whenever code changes are made, you can build the Docker image and update the development custom step by running this command:

```
make dev
```

To test the custom step, you can conveniently run a pipeline that uses the step, from your local machine:

```
make testdev
```

## Publishing

Steps for publishing the custom step:

  1. Bump the custom step version and Docker image version in [step.yaml](./step.yaml).

  1. Make a commit.

  1. Create an annotated tag.

  1. Push the commits and tags.

  1. Build a new tagged Docker image and update the step (update `x.x.x` to the actual version):

      ```
      TAG=x.x.x make prod
      ```

  1. Test the new version of custom step:

      ```
      make testprod
      ```
