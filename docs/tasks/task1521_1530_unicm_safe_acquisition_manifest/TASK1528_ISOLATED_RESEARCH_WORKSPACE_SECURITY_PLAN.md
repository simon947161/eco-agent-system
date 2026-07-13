# Task1528 — UniCM Isolated Research Workspace Security Plan

Date: 2026-07-14

Status: DESIGN ONLY / WORKSPACE NOT CREATED

## Isolation objective

Any future UniCM acquisition must remain outside the ClimateOS core runtime and must be reversible.

Preferred logical separation:

```text
authoritative metadata
    ↓
quarantined source archive
    ↓
verified immutable source tree
    ↓
isolated dependency environment
    ↓
read-only datasets
    ↓
bounded experiment outputs
    ↓
evidence-only adapter export
```

No stage may silently promote code, dependencies or model output into ClimateOS.

## Proposed workspace zones

| Zone | Purpose | Write policy |
|---|---|---|
| `00_metadata` | DOI, release, licence, checksums, manifests | controlled |
| `01_quarantine` | unopened downloaded archives | append-only |
| `02_source_verified` | checksum-verified immutable source | read-only |
| `03_environment` | isolated Conda/container definition | rebuildable |
| `04_data_raw` | provider-native data | read-only |
| `05_data_derived` | deterministic transformed data | replaceable |
| `06_checkpoints` | verified weights only | read-only |
| `07_runs` | bounded execution outputs | writable |
| `08_evidence` | hashes, logs, reports, provenance | append-only |
| `09_export` | approved model-neutral evidence records | controlled |

The actual filesystem location remains undecided and is not created by this batch.

## Source controls

- acquire only from the verified GitHub release or Zenodo record;
- pin `v1.0` / commit `67fe4c183df351d5039c5b3b80ae86a68b627398`;
- verify Zenodo MD5 and preferably calculate SHA-256 after any future authorized download;
- preserve the MIT licence;
- compare extracted tree with the pinned Git tree;
- prohibit automatic execution on extraction;
- record Software Heritage identifier.

## Dependency controls

- do not install from the upstream environment file without review;
- generate a fully pinned lock proposal;
- record direct and transitive packages in an SBOM;
- review PyTorch/CUDA compatibility and known vulnerabilities;
- prohibit changes to the existing ClimateOS environment;
- disable environment activation by default;
- use least-privilege outbound network rules;
- record all package indexes and hashes where available.

## Checkpoint controls

No official checkpoint is currently available.

If one is later identified:

- verify maintainer-controlled source;
- record licence, size and cryptographic checksum;
- quarantine before use;
- inspect serialization format;
- avoid unsafe pickle loading where possible;
- do not load with unrestricted privileges;
- reject third-party mirrors without independent authentication.

## Data controls

- acquire only manifest-approved subsets;
- keep raw data immutable;
- record terms and citation per provider;
- preserve units, calendars, masks and coordinates;
- hash derived products and transformation scripts;
- prohibit personal, confidential or operational customer data;
- define retention and deletion before download.

## Runtime controls

A later execution plan must:

- set CPU/GPU, memory, disk and time ceilings;
- disable operational endpoints;
- prohibit live API calls;
- prevent automated publishing;
- write only to the run zone;
- capture commands, environment hashes and random seeds;
- stop on unexpected network access or unbounded disk growth;
- retain failure as valid evidence.

## Rollback and cleanup

- delete environment and derived/run zones without touching raw evidence records;
- retain source, licence, checksum and experiment summaries as required;
- revoke temporary credentials;
- document incomplete deletion where provider caches exist;
- never delete or alter the authoritative ClimateOS branch as cleanup.

## Human authority

Only the Founder may authorize acquisition or execution.

A qualified climate scientist must review any future regional or consequential interpretation. Infrastructure security review does not substitute for scientific authority.

## Task1528 decision

The isolation design is sufficient for a future source-only acquisition proposal.

No workspace, environment, archive, dataset or checkpoint has been created or acquired.
