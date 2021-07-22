#!/usr/bin/env python3

"""Main entrypoint"""

import io
import functools
import json
import os
import sys

import boto3

AWS_IAM_ROLE_ARN = 'AWS_IAM_ROLE_ARN'
SECRETS = 'SECRETS'


def echo(message):
    print(message)


def die(message):
    echo('Error: {}'.format(message))
    sys.exit(1)


def assume_role(role_arn):
    client = boto3.client('sts')
    response = client.assume_role(
            RoleArn=role_arn,
            RoleSessionName='cfstep-aws-secrets-manager'
        )
    return (
            response['Credentials']['AccessKeyId'],
            response['Credentials']['SecretAccessKey'],
            response['Credentials']['SessionToken']
        )


@functools.lru_cache
def get_secret_value(creds, secret_arn):
    echo('Getting secrets for {}'.format(secret_arn))

    client = boto3.client('secretsmanager')

    if creds:
        client = boto3.client(
            'secretsmanager',
            aws_access_key_id=creds[0],
            aws_secret_access_key=creds[1],
            aws_session_token=creds[2]
        )

    return client.get_secret_value(SecretId=secret_arn)


def write_to_cf_volume(results):
    file = '/meta/env_vars_to_export'
    with io.open(file, 'a') as f:
        f.writelines(results)


def main():
    creds = ()

    if aws_iam_role_arn := os.environ.get(AWS_IAM_ROLE_ARN):
        creds = assume_role(aws_iam_role_arn)

    secrets = os.environ.get(SECRETS) or []

    results = []

    for secret in secrets.split('|'):
        arn, key, store_to = secret.split('#')

        response = get_secret_value(creds, arn)

        echo("Storing secret value for key '{}' into ${}".format(key, store_to))
        secret_string = json.loads(response['SecretString'])
        value = secret_string[key]

        results.append('{}={}\n'.format(store_to, value))

    write_to_cf_volume(results)


if __name__ == '__main__':
    main()
