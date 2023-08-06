#!/bin/bash

export DOCKER_BUILDKIT=1

if [ "$1" != "" ]; then
  PROCESSOR_IMAGE="$1"
else
  echo Please provide target image name:version
  exit 9
fi

BUILD_IMAGE_BASE="769057607614.dkr.ecr.us-east-2.amazonaws.com/base:38"
DEPLOY_IMAGE_BASE="769057607614.dkr.ecr.us-east-2.amazonaws.com/python:3.8-slim"

docker build -t ${PROCESSOR_IMAGE} --target evaluation_image --file Dockerfile \
    --build-arg BUILD_IMAGE_SOURCE=${BUILD_IMAGE_BASE} \
    --build-arg GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS} \
    --build-arg DEPLOY_IMAGE_SOURCE=${DEPLOY_IMAGE_BASE} .