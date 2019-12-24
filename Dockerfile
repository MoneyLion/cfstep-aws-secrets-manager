FROM python:3.8.1-alpine3.10

ARG USER=cfuser
ARG AWSCLI_VERSION=1.16.300
ARG JQ_VERSION=1.6-r0

ENV AWS_ACCESS_KEY_ID ""
ENV AWS_SECRET_ACCESS_KEY ""
ENV AWS_DEFAULT_REGION ""
ENV AWS_IAM_ROLE_ARN ""

LABEL alpine=3.10
LABEL python=3.8.1
LABEL jq=${JQ_VERSION}
LABEL aws-cli=${AWSCLI_VERSION}

# Install jq for JSON parsing

RUN apk add --update \
  jq=${JQ_VERSION} \
  && rm -rf /var/cache/apk/*

# Install AWS CLI

RUN pip install --no-cache-dir awscli==${AWSCLI_VERSION}

# Create and use non-root user

RUN addgroup -S ${USER} && adduser -S ${USER} -G ${USER}
USER ${USER}

WORKDIR /home/${USER}

COPY --chown=${USER} entrypoint ./entrypoint

ENTRYPOINT ["/bin/ash", "./entrypoint"]
