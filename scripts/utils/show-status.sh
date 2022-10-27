#!/bin/bash

if [ "$1" == "-h" ] ; then
    echo "Affiche l'état des services docker liés à Diapason (selon .settings)."
    echo
    echo "Syntaxe: show-status.sh [-h]"
    echo "options:"
    echo "h     Afficher l'aide."
    echo
    echo "Lancer depuis le dossier 'diapason' : ./scripts/utils/show-status.sh"
    exit 0
fi

DOCKER_COMMAND=$(./scripts/utils/select-docker-compose.sh)

echo "--- ${DOCKER_COMMAND} ps ---"
$DOCKER_COMMAND ps
echo "-------------------------------------------"
