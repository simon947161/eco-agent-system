# Task1535–1536 — Archive Safety and File Inventory

Date: 2026-07-14

Status: COMPLETE / PASS

## Pre-extraction checks

| Check | Result |
|---|---|
| ZIP entries | 21 |
| Regular files | 17 |
| Directory entries | 4 |
| Compressed archive size | 1,103,721 bytes |
| Reported compressed payload | 1,098,967 bytes |
| Uncompressed file bytes | 1,256,256 bytes |
| Absolute paths | NONE |
| Parent-directory traversal | NONE |
| Symbolic links | NONE |
| Unexpected top-level roots | NONE |

The sole top-level directory was:

tsinghua-fib-lab-UniCM-Global-Climate-Modes-67fe4c1/

Extraction occurred only after these checks passed.

## File inventory

| Mode | Bytes | Path |
|---|---:|---|
| 100644 | 601 | .gitignore |
| 100644 | 1,085 | LICENSE |
| 100644 | 7,556 | README.md |
| 100644 | 1,131,775 | assets/framework.png |
| 100644 | 365 | environment.yml |
| 100644 | 3,244 | src/Embed.py |
| 100644 | 40,199 | src/LoadData.py |
| 100644 | 21,414 | src/Trainer.py |
| 100644 | 4,978 | src/app_ensemble.py |
| 100644 | 2,610 | src/app_test.py |
| 100644 | 1,337 | src/app_train.py |
| 100644 | 6,098 | src/config.py |
| 100644 | 13,847 | src/models.py |
| 100644 | 7,809 | src/my_tools.py |
| 100644 | 693 | src/script/test.sh |
| 100755 | 282 | src/script/train.sh |
| 100644 | 12,363 | src/settings.py |

## Static-only handling

The executable bit on src/script/train.sh was recorded as metadata only. Neither that file nor src/script/test.sh, any Python module, environment.yml, or any other upstream content was executed or interpreted as an installation instruction.

## Archive-risk decision

The archive did not present path traversal, symlink extraction or expansion-size concerns within this bounded inspection.

This result is not a malware-clearance claim and is not authorization to install or execute the contents.
