#!/bin/bash

SEP="-------------------------------------------"

if [ "$1" == "-h" ] ; then
    echo "Démarre les modules listés dans .settings."
    echo
    echo "Syntaxe: start.sh [-h|y]"
    echo "options:"
    echo "h     Afficher l'aide."
    echo "y     Ne pas demander confirmation."
    echo
    echo "Lancer depuis le dossier 'Diapason' : ./scripts/start.sh"
    exit 0
fi


ROOT_PATH="$(dirname "$(dirname "$(realpath "$0")")")"
cd $ROOT_PATH

DOCKER_COMMAND=$(./scripts/utils/select-docker-compose.sh)

echo "$(./scripts/utils/show-services.sh)"
echo "Tous ces services vont être démarrés."

if [ "$1" == '-y' ]; then
  $DOCKER_COMMAND up -d
  exit 1
fi

read -p "Confirmer [O/N]? " -n 1 -r
echo
if [[ $REPLY =~ ^[Oo]$ ]]
then
    $DOCKER_COMMAND up -d
fi
