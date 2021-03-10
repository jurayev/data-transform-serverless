FROM python:3.8-alpine

RUN apk update && apk add curl
RUN apk add --update nodejs nodejs-npm

ENV WAITFORIT_VERSION="v2.4.1"
RUN curl -o /usr/local/bin/waitforit -sSL https://github.com/maxcnunes/waitforit/releases/download/$WAITFORIT_VERSION/waitforit-linux_amd64 \
    && chmod +x /usr/local/bin/waitforit

RUN npm install -g serverless
RUN npm install serverless-localstack
RUN mkdir -p /usr/src/data-transform-serverless
WORKDIR /usr/src/data-transform-serverless

COPY requirements.txt .
COPY scripts ./scripts
COPY src ./src
COPY test ./test

# install dependencies
RUN pip install -r requirements.txt

RUN chmod +x scripts/execute-pipeline.sh
CMD waitforit -address=http://$LOCALSTACK_HOSTNAME:4566 -timeout=120 -- echo "STARTING PIPELINE" && . scripts/execute-pipeline.sh
