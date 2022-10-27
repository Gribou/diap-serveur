#!/bin/bash

source .settings
source .settings.override 2> /dev/null

SEP="-------------------------------------------"

echo $SEP
echo "Connexion au registre ASAP"
docker login -u $DEPLOY_TOKEN_USERNAME -p $DEPLOY_TOKEN_PASSWORD registry.asap.dsna.fr
echo $SEP
