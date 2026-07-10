# Technical Stack Record

## Python Version

```text
Python 3.12.13
```

## Authorized Stack

| Layer | Tool | Boundary |
| --- | --- | --- |
| Language | Python | Local prototype only. |
| Application | FastAPI | Localhost-only service. |
| Runner | Uvicorn | Manual startup only. |
| Persistence | SQLite | Local mutable database; not committed. |
| Validation | Pydantic / FastAPI | Request and response boundary validation. |
| Frontend | Local HTML / CSS / JavaScript | Served by the local app; no external assets. |
| Testing | pytest and FastAPI TestClient | Local tests only. |
| Export | JSON and Markdown | Local archive review package only. |

## Dependency Boundary

Dependencies are declared in:

```text
prototype/climateos-local-controlled-prototype-core/requirements.txt
```

No cloud framework, production infrastructure framework, cloud ORM, distributed database abstraction, model SDK, GitHub SDK, scheduler framework, or deployment framework is introduced.
