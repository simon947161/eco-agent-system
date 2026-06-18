# Task Dependencies

Dependencies show the normal review order. They do not automatically start or
approve later tasks.

## Repository Factory Sequence

```text
Task46 - Repository Control
  |
  v
Task47 - Master Directory Scaffold
  |
  v
Task48 - Codex Batch Queue System
  |
  v
Task49 - Agent Template Standard
  |
  v
Task50 - CarbonOS Foundation
```

## CarbonOS and ESG Sequence

```text
Task50 - CarbonOS Foundation
  |
  v
Task51 - Green Power Accounting Agent
  |
  v
Task52 - Carbon Budget Agent
  |
  v
Task53 - ESG Disclosure Auditor Agent
```

Task51-Task53 should not be treated as implementation-ready until Task50
defines shared CarbonOS evidence and governance boundaries.

## ParkOS Demonstration Sequence

```text
Task54 - Zero Carbon Park Agent
  |
  v
Task55 - Demo Integration: Batlow + Datong + Shanghai
```

## Independent Planning Task

```text
Task56 - Independent Business Layer Planning
```

Task56 may be planned independently because it is documentation-only. It must
not implement payments, transactions, wallets, crypto, or financial advice.

## Dependency Review Questions

- Are all predecessor tasks reviewed?
- Are required files present?
- Are status and architecture terms consistent?
- Are tests passing?
- Is the next task small enough for one Codex session?
