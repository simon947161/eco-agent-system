# Reliability Requirements

## Required Local Reliability Controls

- Manual local backup creation must validate database integrity before copying.
- Backup output must include a manifest, checksum, schema version, and human-readable report.
- Restore must validate backup checksum and integrity before replacing a target database.
- Restore must preserve an existing target database before replacement.
- SQLite integrity checks must be available through a foreground command and local route.
- Data diagnostics must identify missing tables, invalid statuses, duplicate relationships, orphan review records, Founder Gate reference problems, archive-state inconsistencies, and supersession linkage warnings.
- Schema migration must support preflight, dry-run, migration backup, current-version reporting, and unsupported-version rejection.
- Human Review transitions must reject invalid jumps and record blocked transition audits.
- Founder Gate history must support manual supersession references and decision versions.
- Local request and import limits must reject oversized or conflicting inputs.

## Reliability Non-Claims

These controls make the local prototype more reviewable. They do not make it operational, production-ready, compliant, assured, certified, automated, deployed, or externally integrated.
