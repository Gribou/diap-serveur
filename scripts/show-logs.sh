#!/bin/bash

SEP="-------------------------------------------"

if [ "$1" == "-h" ] ; then
    echo "Affiche les logs du service en argument ou choisi interactivement."
    echo
    echo "Syntaxe: show-logs.sh [-h] [SERVICE]"
    echo "options:"
    echo "h     Afficher l'aide."
    echo
    echo "Lancer depuis le dossier 'Diapason' : ./scripts/show-logs.sh"
    exit 0
fi

ROOT_PATH="$(dirname "$(dirname "$(realpath "$0")")")"
cd $ROOT_PATH

DOCKER_COMMAND=$(./scripts/utils/select-docker-compose.sh)

if [ $# -eq 0 ]; then
  echo "$(./scripts/utils/show-services.sh)"
  echo "Indiquez le service dont vous voulez voir les logs."
  echo "(rien pour quitter)"
  read -p " >> " SERVICE
  if [ -z "$SERVICE" ]; then
    exit 1
  fi
else
  SERVICE="$@"
fi

$DOCKER_COMMAND logs --follow $SERVICE
