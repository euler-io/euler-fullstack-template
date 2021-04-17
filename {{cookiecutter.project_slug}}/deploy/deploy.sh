#!/bin/bash

set -e

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

docker image build -t {{ cookiecutter.project_slug }}-deploy:latest -f $SCRIPT_DIR/deploy.dockerfile $SCRIPT_DIR
docker container run -u $(id -u):$(id -g) -it --rm -v $(pwd):/template -v $1:/output {{ cookiecutter.project_slug }}-deploy:latest cookiecutter -o /output /template
#CURRENT_UID=$(id -u) CURRENT_GID=$(id -g) OUTPUT=$1 docker-compose -f $SCRIPT_DIR/docker-compose.yml up