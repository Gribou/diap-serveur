#!/bin/bash

SEP="-------------------------------------------"

ROOT_PATH="$(dirname "$(dirname "$(realpath "$0")")")"
cd $ROOT_PATH

if [ "$1" == "-h" ] ; then
    echo "Stoppe les services docker listés en arguments ou sélectionnés interactivement."
    echo
    echo "Syntaxe: stop.sh [-h] [SERVICES...]"
    echo "'all' pour tous les services sans confirmation"
    echo "options:"
    echo "h     Afficher l'aide."
    echo
    echo "Lancer depuis le dossier 'Diapason' : ./scripts/stop.sh"
    exit 0
fi

DOCKER_COMMAND=$(./scripts/utils/select-docker-compose.sh)

if [ $# -eq 0 ]; then
  echo "$(./scripts/utils/show-status.sh)"
  echo "$(./scripts/utils/show-services.sh)"
  echo "Indiquez la liste des services à stopper séparée par des espaces."
  echo "('all' pour tous les services, rien pour quitter)"
  read -p " >> " SERVICES
  echo
  if [ -z "$SERVICES" ]; then
    exit 1
  fi
else
  SERVICES="$@"
fi

if [ "${SERVICES}" == "all" ]; then
  echo "Tous les services vont être stoppés :"
  $DOCKER_COMMAND stop && $DOCKER_COMMAND rm -f
else
  echo "Les services ${SERVICES} vont être stoppés :"
  $DOCKER_COMMAND stop $SERVICES && $DOCKER_COMMAND rm -f
fi
