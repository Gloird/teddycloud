# TeddyCloud

## Features
TeddyCloud is an alternative server for your Toniebox, allowing you to host the cloud services locally.
This gives you control over which data is sent to the manufacturer's cloud and allows you to host your own figurine audio files on e.g. your NAS or any other server.

Currently implemented are:
* Provide audio content over the air
* Cache original tonie audio content
* Simulate live content (.live)
* Passthrough original tonie audio content
* Convert any audio file to a tonie audio file (web)
* On-the-fly convert audio streams via ffmpeg for webradio and streams
* Basic Web frontend
* Filter custom tags to prevent deletion (.nocloud)
* Configure maximum volume for speaker and headphones
* Configure LED
* Configure slapping
* Customize original box sounds (ex. jingle) over the air
* Extract/Inject certificates on an esp32 firmware dump
* Decode RTNL logs
* MQTT client
* Home Assistant integration (MQTT)
* [Web frontend](https://github.com/toniebox-reverse-engineering/teddycloud_web) (full stack developers welcome)

[![Codecov](https://codecov.io/gh/Gloird/teddycloud/branch/main/graph/badge.svg)](https://codecov.io/gh/Gloird/teddycloud)

If your repository is private, add the `CODECOV_TOKEN` secret in GitHub to allow coverage uploads from CI.

## Planned
* teddyBench integration

## Where to start?
If you want to get started, please follow our [guide on our website](https://toniebox-reverse-engineering.github.io/docs/tools/teddycloud/).

## Development and building
Please use the `develop` branch for your development and pull requests. Stable builds are available from the `master` branch. Don't forget to clone the submodules with `--recurse-submodules`.
To catch sanitizer in your IDE set a breakpoint on `__asan::ReportGenericError`.

## Recent changes
The CI and Docker publishing workflows were extended to support multi-architecture builds.

- GitHub Actions now builds and publishes images for `linux/arm64` in addition to `linux/amd64`.
- The Docker workflows use `docker/setup-qemu-action` and `docker/setup-buildx-action` for cross-building and testing.

These changes ensure official images are available for ARM64-based hosts (Raspberry Pi 64-bit, cloud ARM instances, etc.).

## Attribution
The icons used are from here:
* img_empty.png: https://www.flaticon.com/free-icon/ask_1372671
* img_unknown.png: https://www.flaticon.com/free-icon/ask_1923795
* img_custom.png/favicon.ico: https://www.flaticon.com/free-icon/dog_2829818

Thanks for the original authors for these great icons.
