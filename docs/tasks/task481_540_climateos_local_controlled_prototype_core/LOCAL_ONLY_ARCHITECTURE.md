# Local-Only Architecture

## Runtime Shape

```text
Human reviewer
  -> localhost browser
  -> FastAPI local service
  -> SQLite local database
  -> local JSON / Markdown archive export
```

## Localhost Rule

The service accepts only:

```text
127.0.0.1
localhost
```

No startup command, configuration, or documentation instructs a public interface bind.

## No External Connectivity

The prototype does not retrieve external sources, call model providers, synchronize with GitHub, open pull requests, deploy, or publish archive outputs.

## Same-Origin Rule

FastAPI serves both the local frontend and local API from the same localhost origin. No wildcard CORS configuration is used.
