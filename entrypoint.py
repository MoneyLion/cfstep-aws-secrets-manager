#!/usr/bin/env python3

import io
import json
import os
import pathlib
import sys

import boto3

AWS_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'
AWS_DEFAULT_REGION = 'AWS_DEFAULT_REGION'
AWS_IAM_ROLE_ARN = 'AWS_IAM_ROLE_ARN'
SECRETS = 'SECRETS'
CF_VOLUME_PATH = 'CF_VOLUME_PATH'
ENV_VARS = [
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY,
        AWS_DEFAULT_REGION,
        AWS_IAM_ROLE_ARN
]


def echo(message):
    print(message)


def die(message):
    echo('Error: {}'.format(message))
    sys.exit(1)


def checkenv(name):
    if os.environ.get(name) is None or os.environ[name] == '':
        die('Please provide {}'.format(name))


def unsetenv(name):
    del os.environ[name]


def env(name):
    return os.environ[name]


def prepare_config():
    directory = pathlib.Path.home() / '.aws'

    if not os.path.exists(directory):
        os.mkdir(directory)

    with io.open(directory / 'config', 'w') as config_file:
        lines = [
            '[default]\n',
            'aws_access_key_id = {}\n'.format(env(AWS_ACCESS_KEY_ID)),
            'aws_secret_access_key = {}\n'.format(env(AWS_SECRET_ACCESS_KEY)),
            'region = {}\n'.format(env(AWS_DEFAULT_REGION)),
            'role_arn = {}\n'.format(env(AWS_IAM_ROLE_ARN)),
            'source_profile = default\n',
            'duration_seconds = 900\n',
        ]
        config_file.writelines(lines)


def write_to_cf_volume(results):
    file = pathlib.Path(env(CF_VOLUME_PATH)) / 'env_vars_to_export'
    with io.open(file, 'a') as f:
        f.writelines(results)


def main():
    for var in ENV_VARS:
        checkenv(var)

    prepare_config()

    # Unset all supplied environment variable values so
    # values in AWS CLI config file are used instead
    for var in ENV_VARS:
        unsetenv(var)

    secrets = env(SECRETS)

    client = boto3.client('secretsmanager')

    results = []
    for secret in secrets.split('|'):
        arn, key, store_to = secret.split('#')

        echo('Getting secrets for {}'.format(arn))
        response = client.get_secret_value(SecretId=arn)

        echo("Storing secret from key '{}' into ${}".format(key, store_to))
        secret_string = json.loads(response['SecretString'])
        value = secret_string[key]

        results.append('{}={}\n'.format(store_to, value))

    write_to_cf_volume(results)


if __name__ == '__main__':
    main()
