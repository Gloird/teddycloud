- Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

## Unreleased

### Ajoutées
- APIs de gestion d'URL pour la récupération de métadonnées et le téléchargement audio.
- Images Docker : ajout de Python3 et de `yt-dlp` pour améliorer le téléchargement et le traitement audio.
- CI : test smoke pour construire et valider le fonctionnement des images Docker.
- Support des builds Docker multi-architectures (`linux/arm64` en complément de `linux/amd64`).

### Changées
- Dockerfiles mis à jour pour installer `yt-dlp` directement et construire le frontend dans l'image.
- Gestion du sous-module `teddycloud_web` améliorée : synchronisation de branche dans les workflows CI.

### Corrigées
- Éviter la troncation JSON / sortie dans `handleApiUrlFetch` et chemins associés ; augmentation des tailles des buffers.
- Amélioration de la sélection du format audio pour permettre un fallback vers la meilleure qualité disponible.

---

Les notes de version seront ajoutées ici pour les futures releases.

---

Release notes will be added here for future releases.
