FROM python:3.8.1-alpine3.10

ARG BOTO_3_VERSION=1.10.45

ENV AWS_ACCESS_KEY_ID ""
ENV AWS_SECRET_ACCESS_KEY ""
ENV AWS_DEFAULT_REGION ""
ENV AWS_IAM_ROLE_ARN ""

LABEL alpine=3.10
LABEL python=3.8.1
LABEL boto3=${BOTO_3_VERSION}

# Install AWS SDK

RUN pip install --no-cache-dir boto3==${BOTO_3_VERSION}

COPY entrypoint.py /entrypoint.py

CMD ["/entrypoint.py"]
