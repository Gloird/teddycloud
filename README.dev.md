Development quickstart
======================

Prerequisites
- Node.js 18+, npm
- gcc (or build tools on Windows), protoc-c if you plan to build backend

Quickstart (Linux/macOS)

1) Install dependencies and start frontend dev server:

```bash
cd teddycloud_web
npm ci
npm run start
```

2) In another terminal build the backend in debug mode:

```bash
make build OPTI_LEVEL=-Og
```

3) To run linting and formatting locally:

```bash
cd teddycloud_web
npm run lint
npm run format
```

Husky pre-commit
---------------
After running `npm ci`, Husky hooks are installed via the `prepare` script. Commit hooks run `lint-staged` to lint and format staged files.
