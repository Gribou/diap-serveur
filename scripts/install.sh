#!/bin/bash

set -e;

if [ "$1" == "-h" ] ; then
    echo "Termine l'installation de Diapason."
    echo
    echo "Syntaxe: install.sh [-h] [SERVICES...]"
    echo "'all' pour tous les services sans confirmation"
    echo "options:"
    echo "h     Afficher l'aide."
    echo
    echo "Lancer depuis le dossier 'Diapason' : ./scripts/install.sh"
    exit 0
fi

echo "Création de .setting.override s'il n'existe pas"
touch .settings.override
if [ -f ".env" ]; then
  :
else
  echo "Création de .env"
  cp .env.template .env
fi

chmod -R +x ./scripts/*.sh

source .settings
source .settings.override 2> /dev/null

if [ $# -eq 0 ]; then
  echo "Tous les modules vont être installés (${APPS})."
  read -p "Confirmer [O/N]? " -n 1 -r
  echo ""

  if [[ $REPLY =~ ^[Oo]$ ]]; then
    CHOICES="$APPS"
  else
    exit 0
  fi
else
  if [ "$@" == "all" ]; then
    CHOICES="$APPS"
  else
    CHOICES="$@"
  fi
fi


for APP in $CHOICES; do
  INSTALL_SCRIPT="modules/${APP}/install.sh"
  echo "###########################################"
  echo "#      Installation de ${APP}              "
  echo "###########################################"
  if [ -f "$INSTALL_SCRIPT" ]; then
    $INSTALL_SCRIPT
  else
    mkdir -p "data/${APP}/backups"
    mkdir -p "data/${APP}/media"
    echo
    echo " --> ${APP} est prêt"
    echo "-------------------------------------------"
  fi
done

echo " --> DONE"
echo "Vous pouvez ensuite télécharger les images docker à jour avec ./scripts/update.sh"
echo "puis lancer les services avec ./scripts/start.sh"
