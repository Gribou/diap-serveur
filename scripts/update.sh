#!/bin/bash

set -e;

if [ "$1" == "-h" ] ; then
    echo "Mets à jours les projets listés en arguments ou sélectionnés interactivement."
    echo "(Télécharge les nouveaux fichiers, 'pull' les images docker distantes les plus récentes, 'build' les images docker locales)"
    echo
    echo "Syntaxe: update.sh [-h] [SERVICES...]"
    echo "'all' pour tous les services sans confirmation, y compris db, redis, ..."
    echo "options:"
    echo "h     Afficher l'aide."
    echo
    echo "Lancer depuis le dossier 'Diapason' : ./scripts/update.sh"
    exit 0
fi

source .settings
source .settings.override 2> /dev/null

if ! [ -x "$(command -v docker-compose)" ]; then
  # uses new docker compose plugin
  MAIN_DOCKER_COMMAND="docker compose --compatibility"
else
  # uses legacy docker-compose
  MAIN_DOCKER_COMMAND="docker-compose"
fi

echo "Veuillez arrêter les containers concernés avant de mettre à jour."

if [ $# -eq 0 ]; then
  echo "Tous les modules Diapason vont être mis à jour (${APPS})."
  read -p "Confirmer [O/N]? " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Oo]$ ]]; then
    CHOICES="$APPS"
    ALL=1
  else
    exit 0
  fi
else
  if [ "$@" == "all" ]; then
    CHOICES="$APPS"
    ALL=1
    echo "###########################################"
    echo "#    Mise à jour des images partagées     #"
    echo "###########################################"
    # update nginx and redis and postgres as well
    DOCKER_COMMAND="$MAIN_DOCKER_COMMAND -f docker-compose.yml"
    $DOCKER_COMMAND pull
  else
    CHOICES="$@"
  fi
fi

for APP in $CHOICES; do
  echo "###########################################"
  echo "#      Mise à jour de ${APP}               #"
  echo "###########################################"
  UPDATE_SCRIPT="modules/${APP}/update.sh"
  if [ -f "$UPDATE_SCRIPT" ]; then
    $UPDATE_SCRIPT
    echo
  fi
  if [ -f "modules/${APP}/docker-compose.yml" ]; then
    DOCKER_COMMAND="$MAIN_DOCKER_COMMAND -f docker-compose.yml -f modules/${APP}/docker-compose.yml"
    if [ "$ALL" == "1" ]; then
        $DOCKER_COMMAND pull
    else
        $DOCKER_COMMAND pull "${APP}_web"
    fi
  fi
  echo "-------------------------------------------"
done

echo " --> DONE"
echo "Vous pouvez relancer les services avec ./scripts/start.sh"
