# Task687 Security Privacy And Misuse Threat Model

## Assets To Protect

- evidence and provenance;
- human decisions and identities;
- sensitive ecological locations;
- organizational and personal data;
- credentials and future secrets;
- audit history;
- Founder-reserved private assets.

## Threats

- unauthorized access or disclosure;
- prompt injection and tool misuse;
- fabricated or poisoned evidence;
- model-output laundering into claims;
- privilege escalation;
- silent record modification;
- unsafe automation;
- sensitive-species exposure;
- false assurance, scoring, or certification;
- dependency and supply-chain compromise.

## Future Controls Required

Least privilege, authentication, authorization, encryption, secrets separation, sandboxing, signed/audited changes, backups, incident response, dependency review, rate/cost limits, refusal, and human escalation.

## Important Limitation

Hashes and signatures support integrity and accountability; they do not prove scientific truth. Task687 implements no security control.
