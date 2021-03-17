#!/bin/bash

set -e

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

CURRENT_UID=$(id -u) CURRENT_GID=$(id -g) docker-compose -f $SCRIPT_DIR/development/docker-compose-certificates.yml --project-directory $SCRIPT_DIR up
CURRENT_UID=$(id -u) CURRENT_GID=$(id -g) docker-compose -f $SCRIPT_DIR/development/docker-compose.yml --project-directory $SCRIPT_DIR up