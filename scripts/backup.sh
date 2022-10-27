#!/bin/bash

set -e;

if [ "$1" == "-h" ] ; then
    echo "Crée une sauvegarde des projets listés en arguments ou sélectionnés interactivement."
    echo
    echo "Syntaxe: backup.sh [-h] [SERVICES...]"
    echo "'all' pour tous les services sans confirmation"
    echo "options:"
    echo "h     Afficher l'aide."
    echo
    echo "Lancer depuis le dossier 'Diapason' : ./scripts/backup.sh"
    exit 0
fi

source .settings
source .settings.override 2> /dev/null

echo "Les containers doivent être démarrés (./scripts/start.sh)."

if [ $# -eq 0 ]; then
  echo "Tous les projets vont être sauvegardés (${APPS})."
  read -p "Confirmer [O/N]? " -n 1 -r
  echo
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
  BACKUP_SCRIPT="modules/${APP}/backup.sh"
  echo "###########################################"
  echo "     Sauvegarde de ${APP}"
  echo "###########################################"
  if [ -f "$BACKUP_SCRIPT" ]; then
    $BACKUP_SCRIPT
  else
    docker exec "$(basename $PWD)_${APP}_web_1" /app/scripts/backup.sh
  fi
  echo "-------------------------------------------"
done

echo " --> DONE"
