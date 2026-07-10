# Risk Flag Matrix

Risk flags are governance controls, not scores.

| Risk flag ID | Risk | Trigger | Required handling | Stop condition |
| --- | --- | --- | --- | --- |
| RF-001 | Source verification risk | Official or candidate citation path not directly verified. | Human source review before future use. | Block final evidence status. |
| RF-002 | Translation / language risk | Chinese-language source or translated paraphrase. | Bilingual human review before future use. | Block external-facing paraphrase. |
| RF-003 | Political sensitivity risk | Public authority, policy, regional governance, or disaster response framing. | Human review and Founder Gate for external use. | Block political conclusion. |
| RF-004 | Compliance / ESG overclaim risk | Any wording implying compliance, ESG performance, carbon performance, assurance, or certification. | Remove wording or escalate to Founder Gate. | Block conclusion. |
| RF-005 | Standards / framework interpretation risk | Any attempt to interpret standards or frameworks from source material. | Stop and defer. | Block standards or framework conclusion. |
| RF-006 | Timeliness risk | Old source, unclear update cycle, or event/source-date mismatch. | Record date and require freshness review. | Block current-state conclusion. |
| RF-007 | News-source caution risk | Event source is news-based or not case-specific. | Treat as event discovery only. | Block evidence admission. |
| RF-008 | Runtime creep risk | Requirements note drifts toward architecture, runtime, API, database, MCP, n8n, automation, or implementation. | Reframe as question or defer. | Block future-work execution. |
