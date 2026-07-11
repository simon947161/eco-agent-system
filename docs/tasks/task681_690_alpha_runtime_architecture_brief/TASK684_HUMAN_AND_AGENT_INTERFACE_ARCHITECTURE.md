# Task684 Human And Agent Interface Architecture

## Human Interface

Supports questions, evidence inspection, uncertainty, counter-evidence, consent, approval, refusal, correction, and action records.

## Agent Interface

Supports bounded capability discovery, scoped requests, evidence-candidate return, challenge, escalation, and explicit inability to decide.

## Internal API

A future internal contract between runtime components. It is not a public or external API authorization.

## Administrative CLI

A future local operator surface for diagnostics, replay, export, integrity checks, and maintenance. It is not the public user interface.

## Future MCP

MCP may expose approved capabilities to agents only after tool schemas, permissions, evidence return, audit, and human approval are separately authorized.

## Boundary

These interfaces are distinct. Task684 creates no UI, API, CLI, MCP server, or agent.
