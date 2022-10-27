#!/bin/bash

set -e;

if [ "$1" == "-h" ] ; then
    echo "Restaure les données à partir du contenu de diapason/data/"
    echo
    echo "Syntaxe: restore.sh [-h] [MODULE_NAME] [DUMP_FILE]"
    echo "MODULE_NAME nom du module à restaurer"
    echo "DUMP_FILE nom du fichier dump à restaurer (ex : perfos_20222222_222222.json)."
    echo "\t Ce fichier doit obligatoirement être placé dans diapason/data/{MODULE_NAME}/backups/database_dumps/"
    echo
    echo "options:"
    echo "h     Afficher l'aide."
    echo
    exit 0
fi

docker exec -it "$(basename $PWD)_${1}_web_1" /app/scripts/restore.sh $2
