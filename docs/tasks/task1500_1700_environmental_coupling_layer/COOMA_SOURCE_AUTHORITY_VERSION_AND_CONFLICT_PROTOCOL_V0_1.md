# Cooma Source Authority, Version and Conflict Protocol v0.1

## Authority tiers

1. Statutory primary: instrument identity and visible in-force version state.
2. State government primary: published regional-plan and implementation status.
3. Council primary: Council-published service, planning and local-context pages.
4. Scientific agency primary: station, catchment and scientific metadata within
   the agency's declared scope.
5. Project proponent primary: authoritative only for what the proponent publicly
   states about its own project.
6. Official news discovery: a dated lead requiring corroboration before any
   evidentiary use.

The tiers are purpose-specific, not a universal ranking. A Council page may be
the best source for Council publication identity while a statutory site is the
better source for an in-force instrument version.

## Version handling

- Record access date separately from publication, update, effective and version
  dates.
- When a current plan and a draft replacement coexist, retain both states.
- `current` in a URL is a point-in-time observation and must be rechecked before
  future use.
- Absence of a visible revision date becomes an explicit unknown state.
- Linked PDFs and datasets remain unreviewed until a separate content-acquisition
  and licence gate is approved.

## Conflict handling

Conflicts are recorded without silent resolution. Later review should compare:

- publisher role and authority for the particular claim;
- publication, effective, update and access dates;
- declared geographic coverage;
- instrument or document version;
- whether the statement is statutory, administrative, scientific, proponent or
  news content;
- whether a later primary source supersedes an earlier one.

No source is promoted merely because it is newer, easier to access or more
detailed.

## Incompleteness handling

The public web is an observable publication surface, not a complete Council or
regional database. Missing material is recorded as `UNKNOWN` or `DEFERRED`, not
inferred from interview context, search absence or news reporting.

## ClimateOS–WorkOS handoff

ClimateOS may later accept legally reusable, reviewed public environmental
evidence. Private operational records remain in the separate WorkOS. A future
handoff may provide de-identified evidence metadata or aggregates only after a
separate privacy, authority and purpose review.
