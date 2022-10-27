#!/bin/bash

DOCKER_COMMAND=$(./scripts/utils/select-docker-compose.sh)

echo "--- $DOCKER_COMMAND config --services ---"
$DOCKER_COMMAND config --services
echo "-------------------------------------------"
