# Installation

[Documentation Diapason](https://infogenestatique.page.asap.dsna.fr/diapason/doc/docs/maintenance/installation)

# Mise à jour

[Documentation Diapason](https://infogenestatique.page.asap.dsna.fr/diapason/doc/docs/maintenance/mettre-a-jour)

# Documentation

## .settings

Contient le paramétrage global du projet : quels modules seront montés et comment. Il ne modifie pas le paramétrage _interne_ des containers.

Peut être changé au cas par cas via `.settings.override`

## .env

Contient le paramétrage partagé par les différents services créés par docker-compose (y compris Nginx).

Il n'existe pas par défaut (les valeurs par défaut sont choisies par docker-compose). S'il existe, ces valeurs sont utilisées par docker-compose à la place des valeurs par défaut.

Les valeurs possibles, leur usage et les valeurs par défaut sont décrits dans `.env.template`

## Fichiers docker-compose.yml

Décrivent les différents services qui seront lancés et leurs interactions.

Les fichiers à utiliser sont fonction du contenu de `.settings` et `.settings.override`:

- `docker-compose.yml` est toujours chargé
- `docker-compose.ssl.yml` est chargé si le site doit être servi en https (NO_SSL=0)
- Les fichiers par modules sont chargés en fonction des services à démarrer (variable APPS)
- Chaque fichier surcharge le précédent donc un fichier ne peut pas fonctionner seul.

Ces fichiers sont utilisés par les scripts du dossier `./scripts`.

Utiliser le script `./utils/select-docker-compose.sh` pour obtenir la commande docker-compose à utiliser avec les .settings actuels.

## scripts/

Contient les scripts pour lancer, arrêter, mettre à jour... les services.

[Documentation Diapason](https://infogenestatique.page.asap.dsna.fr/diapason/doc/docs/maintenance/superviser)

# Intégrer un nouveau module

- créer un dossier `data/mon-module`où pourront être montés par Docker les volumes du module devant être accessible aisément (fichiers statiques à servir, sauvegardes, media, etc)
- créer un dossier `modules/mon-module` avec
  - fichier `docker-compose.yml` décrivant les containers à monter pour le nouveau module. Ce fichier peut également surcharger le service "nginx" pour lui permettre de servir les fichiers statiques par exemple
  - éventuellement créer des scripts `install.sh` `update.sh` `backup.sh` `restore.sh`
- créer un fichier `nginx/locations/modules/nginx.mon-module.locations.template` décrivant la façon dont NGINX doit servir le module
  - inclure ce fichier dans `nginx/modules/nginx.diapason.locations.template` en le précédant d'une variable d'environnement `<MONMODULE>_MOUNT`
  - ajouter cette variable au service nginx dans `docker-compose.yml` avec la valeur '#' (par défaut, votre module n'est pas servi par Nginx)
  - surcharger cette variable dans `modules/mon-module/docker-compose.yml` avec la valeur '' (votre module est servi par Nginx si votre docker-compose est utilisé)
- mettre à jour `.env.template` et compléter `.env` selon les besoins
- ajouter le nom du module dans la variable APPS de `.settings`
- Arrêter **tous les services** avec `./scripts/stop.sh` (pour que nginx utilise la nouvelle configuration en redémarrant)
- mettre à jour le module avec `./scripts/update.sh <mon-module>`
- Démarrer **tous les services** avec `./scripts/start.sh`
