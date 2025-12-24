
# TeddyCloud

> Fork du projet original: [toniebox-reverse-engineering/teddycloud](https://github.com/toniebox-reverse-engineering/teddycloud)

[![Codecov](https://codecov.io/gh/Gloird/teddycloud/branch/main/graph/badge.svg)](https://codecov.io/gh/Gloird/teddycloud)

Si votre dépôt est privé, ajoutez le secret `CODECOV_TOKEN` dans les secrets GitHub pour permettre le téléversement des rapports de couverture depuis la CI.


## Fonctionnalités
TeddyCloud est un serveur alternatif pour votre Toniebox, permettant d'héberger les services cloud localement.
Cela vous donne le contrôle sur les données envoyées au cloud du fabricant et permet d'héberger vos propres fichiers audio de figurines, par exemple sur un NAS ou tout autre serveur.

Fonctionnalités actuellement implémentées :
- Fournir du contenu audio en over-the-air
- Mettre en cache le contenu audio original des Tonies
- Simuler du contenu en direct (.live)
- Réacheminement (passthrough) du contenu audio original
- Conversion de n'importe quel fichier audio en fichier Tonie (web)
- Conversion à la volée des flux audio via ffmpeg (webradio, streams)
- Interface Web basique
- Filtrage des tags personnalisés pour empêcher la suppression (.nocloud)
- Configuration du volume maximal pour haut-parleur et casque
- Configuration des LEDs
- Configuration du "slapping"
- Personnalisation des sons originaux de la box (ex. jingle) via OTA
- Extraction/injection de certificats sur un dump de firmware ESP32
- Décodage des logs RTNL
- Client MQTT
- Intégration Home Assistant (MQTT)
- Interface Web : https://github.com/toniebox-reverse-engineering/teddycloud_web (contributeurs full-stack bienvenus)

## À venir
- Intégration teddyBench

## Où commencer ?
Pour démarrer, suivez notre guide sur le site : https://toniebox-reverse-engineering.github.io/docs/tools/teddycloud/.

## Développement et compilation
Utilisez la branche `develop` pour vos développements et pull requests. Les builds stables sont disponibles sur la branche `master`. N'oubliez pas de cloner les sous-modules avec `--recurse-submodules`.
Pour attraper les erreurs d'AddressSanitizer dans votre IDE, placez un breakpoint sur `__asan::ReportGenericError`.

## Modifications récentes
Les workflows CI et de publication Docker ont été étendus pour supporter les builds multi-architectures.

- GitHub Actions construit et publie désormais des images pour `linux/arm64` en plus de `linux/amd64`.
- Les workflows Docker utilisent `docker/setup-qemu-action` et `docker/setup-buildx-action` pour le cross-build et les tests.

Ces changements permettent d'avoir des images officielles pour des hôtes ARM64 (Raspberry Pi 64-bit, instances ARM cloud, etc.).

Autres évolutions récentes (résumé des commits) :

- Ajout d'APIs pour la gestion d'URL permettant la récupération de métadonnées et le téléchargement audio.
- Images Docker : ajout de Python3 et `yt-dlp`; les Dockerfiles ont été mis à jour pour installer `yt-dlp` directement.
- Le build Docker inclut maintenant `nodejs` et construit le frontend web dans l'image pour les besoins du CI/preview.
- Ajout d'un test smoke CI pour valider les images Docker après build et tester le support cross-architecture.
- Meilleure gestion du sous-module `teddycloud_web` : les workflows tentent maintenant de checkout la branche correspondante.
- Corrections pour éviter la troncation JSON/sortie dans `handleApiUrlFetch` et augmentation des tailles de buffers temporaires.
- Amélioration de la sélection des formats audio pour permettre un fallback sur la meilleure qualité.

Consultez `CHANGELOG.md` pour la liste complète des changements non publiés.

## Attribution
Les icônes utilisées proviennent de :
- img_empty.png : https://www.flaticon.com/free-icon/ask_1372671
- img_unknown.png : https://www.flaticon.com/free-icon/ask_1923795
- img_custom.png/favicon.ico : https://www.flaticon.com/free-icon/dog_2829818

Merci aux auteurs originaux pour ces icônes.

