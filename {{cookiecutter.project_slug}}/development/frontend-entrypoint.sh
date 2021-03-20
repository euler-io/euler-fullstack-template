#!/bin/sh

set -e

yarn install --ignore-scripts
REACT_APP_BASE_URL=$REACT_APP_BASE_URL \
	PORT=$PORT \
	yarn run start \
    --cwd $WORKING_DIR