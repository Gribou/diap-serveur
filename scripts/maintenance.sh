#!/bin/bash

set -e;

if [ "$1" == "-h" ] ; then
    echo "Active/désactive le mode maintenance (code 503)."
    echo
    echo "Syntaxe: maintenance.sh [-h] [on|off]"
    echo "options:"
    echo "h     Afficher l'aide."
    echo "on    Activer la maintenance"
    echo "off   Désactiver la maintenance"
    echo
    echo "Lancer depuis le dossier 'diapason' : ./scripts/maintenance.sh on"
    exit 0
fi

MAINTENANCE_LOCK=./nginx/utils/maintenance.lock

if [[ $1 =~ ^(on|ON)$ ]]; then
    touch $MAINTENANCE_LOCK
    exit 0
fi
if [[ $1 =~ ^(off|OFF)$ ]]; then
    rm $MAINTENANCE_LOCK
    exit 0
fi
echo "Réponse invalide. Indiquez 'on' ou 'off' en argument : 'maintenance.sh on'."