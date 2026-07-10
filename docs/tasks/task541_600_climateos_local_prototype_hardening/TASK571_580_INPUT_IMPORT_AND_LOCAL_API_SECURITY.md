# Task571-580 Input, Import, And Local API Security

## Purpose

Harden local input handling, import behavior, and local prototype route controls.

## Completed Work

- Local host guard added for request handling.
- Request-size limit added.
- JSON-safe validation error response added.
- Security headers added.
- Candidate list filters added.
- Model import preview added.
- Duplicate model response and duplicate suggestion validation preserved and expanded.
- Duplicate relationship conflict behavior added.
- Maintenance routes added for local integrity, diagnostics, backup, restore, and migration.

## Boundary

These changes harden existing local prototype routes only. They are not production API, public API, external API, authentication, authorization, deployment, automation, or operational Evidence Passport.
