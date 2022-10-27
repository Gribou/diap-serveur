#!/bin/bash

source .settings
source .settings.override 2> /dev/null

if ! [ -x "$(command -v docker-compose)" ]; then
  # uses new docker compose plugin
  DOCKER_COMMAND="docker compose --compatibility"
else
  # uses legacy docker-compose
  DOCKER_COMMAND="docker-compose"
fi

DOCKER_COMMAND="$DOCKER_COMMAND -f docker-compose.yml"

if [ "$NO_SSL" == 1 ]
then
  :
else
  DOCKER_COMMAND="$DOCKER_COMMAND -f docker-compose.ssl.yml"
fi



for APP in $APPS; do
  if [ -f "modules/${APP}/docker-compose.yml" ]; then
    DOCKER_COMMAND="$DOCKER_COMMAND -f modules/${APP}/docker-compose.yml"
  fi
done

if [ -f "docker-compose.extra.yml" ]; then
  DOCKER_COMMAND="$DOCKER_COMMAND -f docker-compose.extra.yml"
fi

echo $DOCKER_COMMAND
