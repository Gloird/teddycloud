# TeddyCloud AI Coding Instructions

## Project Overview
TeddyCloud is an alternative server for Toniebox devices written in C. It intercepts Toniebox-to-cloud communication to enable local hosting of audio content, caching, custom audio encoding, and device management via a web UI.

## Architecture

### Core Components (Backend - C)
- **HTTP/HTTPS Server** (`src/server.c`): Multi-port server handling web UI (port 80/8443) and Toniebox API (port 443)
- **Request Handlers** (`src/handler_*.c`): Route-based handlers for different functionality:
  - `handler_api.c`: Web frontend REST API endpoints (`/api/*`)
  - `handler_cloud.c`: Toniebox cloud API emulation (`/v1/*`, `/v2/*`)
  - `handler_rtnl.c`: Real-time notification logging (RTNL binary protocol)
  - `handler_sse.c`: Server-Sent Events for live updates
- **Settings System** (`src/settings.c`, `include/settings.h`): INI-based config with overlay support for per-box settings
- **Toniefile Encoder** (`src/toniefile.c`): Opus/OGG encoding to TAF format (Tonie Audio File)

### Frontend (React/TypeScript - `teddycloud_web/`)
- **Framework**: Vite + React + TypeScript + Ant Design (AntD)
- **Architecture**: Topic-based structure organized by feature domains (`tonies`, `tonieboxes`, `settings`, `community`)
- **API Client**: `src/api/apis/TeddyCloudApi.ts` (manually maintained, NOT auto-generated - listed in `.openapi-generator-ignore`)
- **State Management**: React Context (`TeddyCloudContext`, `AudioContext`)
- **i18n**: `react-i18next` with translation files in `src/i18n/`

### Key Data Flows
1. **Toniebox → TeddyCloud**: HTTPS requests on port 443 with client certificate authentication
2. **Web UI → TeddyCloud**: REST API on ports 80/8443, responses in JSON (cJSON library)
3. **Cloud Passthrough**: Optional forwarding to original Tonie cloud via `cloud_request.c`

### Directory Structure
```
src/                 # Main C source files (backend)
include/             # Header files - each .c has matching .h
src/cyclone/         # LOCAL modifications to Cyclone library (NOT in cyclone/ submodule)
cyclone/             # TCP/SSL/Crypto library (submodule - DO NOT modify directly)
proto/               # Protocol Buffer definitions for Toniebox communication
src/proto/           # Generated protobuf C files (via protoc-c)
src/platform/        # Platform-specific code (platform_linux.c, platform_windows.c)
wasm/                # WebAssembly TAF encoder for browser-based encoding
contrib/             # Runtime data (certs, config templates, web assets)
teddycloud_web/      # React frontend (separate submodule)
  src/pages/         # Route pages - thin, layout + composition only
  src/components/    # Topic-specific UI (tonies/, tonieboxes/, settings/, community/)
  src/api/apis/      # API client (TeddyCloudApi.ts - do NOT regenerate!)
  src/contexts/      # React contexts (TeddyCloudContext, AudioContext)
  src/hooks/         # Shared generic hooks only (useDebounce, useMediaQuery)
  src/utils/         # Pure helper functions (validators, formatters)
  src/constants/     # URLs (urls.ts), numbers, shared constants
```

## Build System

### Backend Build Commands
```bash
# Linux (default)
make build                    # Standard build with AddressSanitizer
make build NO_SANITIZERS=1    # Release build without sanitizers
make build OPTI_LEVEL=-Og     # Debug-optimized build

# Windows (requires VS Developer Command Prompt via vcvars.bat first)
make PLATFORM=windows build

# Clean builds
make clean
make submodules               # Initialize/update git submodules
```

### Frontend Build Commands
```bash
cd teddycloud_web/
npm install                   # Install dependencies
npm start                     # Dev server (http://localhost:3000, https://localhost:3443)
npm run build                 # Production build to dist/
npm run preview               # Test production build locally
```

### Key Build Targets
- `make all` - Full build including web frontend
- `make wasm` - Build WebAssembly TAF encoder (requires emcc)
- `make cppcheck` - Static analysis
- `make auto` - Watch mode with valgrind (Linux)

### Dependencies
- `protoc-c` (Protocol Buffers compiler)
- `gcc` with AddressSanitizer support
- `npm` (for web frontend)
- `ffmpeg` (runtime, for audio transcoding)

## Code Patterns

### Handler Registration
Handlers are registered in `request_paths[]` array in `server.c`:
```c
{REQ_POST, "/api/fileUpload", SERTY_WEB, &handleApiFileUpload},
{REQ_GET, "/v1/content", SERTY_BOTH, &handleCloudContentV1},
```
- `SERTY_WEB`: Web UI only, `SERTY_API`: Toniebox API only, `SERTY_BOTH`: Both

### Handler Signature
```c
error_t handleXxx(HttpConnection *connection, const char_t *uri, 
                  const char_t *queryString, client_ctx_t *client_ctx);
```

### Settings Definition (in `src/settings.c`)
Settings use macro-based declaration with `OPTION_*` macros in `option_map_init()`:
```c
OPTION_BOOL("cloud.enabled", &settings->cloud.enabled, TRUE, "Enable cloud", "...", LEVEL_BASIC)
OPTION_STRING("core.contentdir", &settings->core.contentdir, "default", "Content dir", "...", LEVEL_DETAIL)
OPTION_UNSIGNED("log.level", &settings->log.level, 4, 0, 6, "Loglevel", "0=off - 6=verbose", LEVEL_DETAIL)
```
- Levels: `LEVEL_NONE`, `LEVEL_BASIC`, `LEVEL_DETAIL`, `LEVEL_EXPERT`, `LEVEL_SECRET`

### JSON Responses
Use cJSON library for all JSON handling:
```c
cJSON *json = cJSON_CreateObject();
cJSON_AddStringToObject(json, "key", value);
char *jsonStr = cJSON_PrintUnformatted(json);
// ... send response
cJSON_Delete(json);
```

### Memory Management
- Use `osAllocMem`/`osFreeMem` for Cyclone-compatible allocation
- Use `custom_asprintf` for formatted string allocation
- Always null-check allocations and handle cleanup

### Path Handling
- Use `PATH_SEPARATOR` macro for cross-platform paths
- `sanitizePath()` in `handler_api.c` normalizes paths and prevents traversal
- Paths stored in settings are relative, resolved via `settings->internal.*dirfull`

## Debugging
- Set breakpoint on `__asan::ReportGenericError` to catch sanitizer errors
- Log levels configured via `log.level` setting (0=off to 6=verbose)
- Use `TRACE_INFO`, `TRACE_DEBUG`, `TRACE_ERROR`, `TRACE_WARNING` macros for logging

## Protocol Buffers
Proto files in `proto/` define Toniebox communication formats:
- `toniebox.pb.taf-header.proto`: TAF audio file header
- `toniebox.pb.rtnl.proto`: Real-time notification log format
- `toniebox.pb.freshness-check.*.proto`: Content freshness protocol
- Generated files go to `src/proto/` via `protoc-c`

## Testing
- No formal test framework; validation via integration with actual Tonieboxes
- `wasm/taf_encoder_test.c` for native TAF encoder testing
- `tests/requests.py` for HTTP endpoint testing

## Important Conventions

### Backend (C)
1. **Error handling**: Return `error_t` (NO_ERROR on success), use `error2text()` for logging
2. **String formatting**: Use `osSnprintf`, `osSprintf` (Cyclone wrappers)
3. **Platform code**: Platform-specific code in `src/platform/platform_*.c`
4. **Modified libraries**: Cyclone modifications live in `src/cyclone/` (NOT in `cyclone/` submodule)
5. **Header pairing**: Each `src/*.c` has a matching `include/*.h`

### Frontend (React/TypeScript)
1. **API Client**: Do NOT regenerate `TeddyCloudApi.ts` - it's manually maintained and listed in `.openapi-generator-ignore`
2. **API Methods**: Use existing helpers (`apiGetTeddyCloudApiRaw`, `apiPostTeddyCloudRaw`, etc.) or add new ones to `TeddyCloudApi.ts`
3. **Design Framework**: Always use AntD components, not custom HTML
4. **Colors**: Use `token.*` from AntD theme (e.g., `token.colorTextDisabled`), never hardcoded colors
5. **Translations**: Always use `t("...")` from react-i18next, never hardcoded strings. Add translations to EN/DE/FR/ES JSON files
6. **URLs**: Check/add URLs in `src/constants/urls.ts` before hardcoding
7. **Hooks**: Feature-specific hooks stay in feature folder (e.g., `src/components/tonies/encoder/hooks/`). Only generic hooks in `src/hooks/`
8. **Pages**: Keep thin - layout + composition only, no business logic
9. **Modals**: State controlled by parent, modal receives data via props
10. **Changelog**: Update `teddycloud_web/CHANGELOG.md` for all frontend changes
