#!/bin/bash

if [ "$1" == "-h" ] ; then
    echo "Ouvre une console dans le container passé en argument ou choisi interactivement."
    echo
    echo "Syntaxe: open-shell.sh [-h] [SERVICE]"
    echo "options:"
    echo "h     Afficher l'aide."
    echo
    echo "Lancer depuis le dossier 'Diapason' : ./scripts/open-shell.sh"
    exit 0
fi

ROOT_PATH="$(dirname "$(dirname "$(realpath "$0")")")"
cd $ROOT_PATH

if [ $# -eq 0 ]; then
  echo "$(./scripts/utils/show-status.sh)"
  echo "Indiquez le container souhaité (rien pour quitter) :"
  read -p " >> " SERVICE
  if [ -z "$SERVICE" ]; then
    exit 1
  fi
  echo "Shell pour le container $SERVICE :"
else
  SERVICE="$1"
fi

docker exec -ti $SERVICE /bin/sh
