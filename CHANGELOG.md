# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

### Added
- URL handling APIs for metadata retrieval and audio fetching.
- Docker images: added Python3 and `yt-dlp` for enhanced audio download/processing.
- CI: smoke test to build and validate Docker image functionality.
- Support for multi-architecture Docker builds (linux/arm64 alongside linux/amd64).

### Changed
- Dockerfiles updated to install `yt-dlp` directly and build the frontend inside the Docker image.
- Submodule handling for `teddycloud_web` improved; CI checks sync the submodule branch with the parent.

### Fixed
- Prevent JSON and buffer truncation in `handleApiUrlFetch` and related code paths; increased buffer sizes.
- Improve audio format selection with a fallback to best quality when needed.

---

Release notes will be added here for future releases.
