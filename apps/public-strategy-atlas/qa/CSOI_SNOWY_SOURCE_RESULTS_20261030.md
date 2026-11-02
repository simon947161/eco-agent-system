# Snowy River DCP intake — verified batch, partial corpus

Continued from Draft PR130 remote `c1b43911b40aec1dc69cb2171e04b10951c2e09a` after reading its latest Founder continuation instruction. Effective runtime policy was unrestricted/enforced, current observations, revision1; no settings or credentials were changed. Ordinary inherited HTTPS/TLS returned HTTP200 for the exact lead in `smrc-dcp-snowy-page`, one selected request/one HTTP exchange, with a50MiB bound. Jindabyne was not requested.

Original: Snowy River DCP2013 Amendment3 observed,16,569,676bytes,465PDFpages, SHA256 `f17fca90befb888b50dbc20f80e38c8e0458ee09b693e1f38f9241b5e18efe9d`. PDFp2 records Amendment3/Issue4, adoption16March2023, resolution58/23, commencement29March2023. A1§3 (PDFp16/printed1) references Snowy River LEP2013 land with the T2Tyrolean Village Stage3 exception. A1§5 (PDFp17/printed2) states LEP precedence. These are historical document observations, not an independently current all-LGA rule or parcel decision. Original bytes stay under `/tmp` and are absent from Git.

The existing register now has **52records/31families;33successful byte receipts (13PDF/20HTML)**,26retrieved document revisions,7directories,17requirements,25bounded own notes across23sources. One source receipt and one own factual note were appended. All previous51source records/147events/37observation records are unchanged. The new content-addressed prefix proof is named in `csoi/snowy-source-results.json`; earlier proof files remain unchanged. The offline append tool now retains a separate proof per resulting catalogue digest rather than overwriting a historical proof filename.

Gate status is deliberately separate: retained directory link PASS; exact original bytes PASS; three **research** page anchors PASS; current-as-of UNKNOWN; legal/geographic review PENDING; reuse rights UNKNOWN; authorised admission PENDING. Formal catalogue extraction/anchor/current-version/admission counts remain0, admitted official relationships0 and actual Council KPIs UNKNOWN. Page digests and a few factual anchor tokens are committed, not original page bodies. A page hash does not establish current law or reuse rights.

Executed verification:

- PASS31/31native files: `csoi/native-snowy.json` and log.
- PASS actual desktop/390px Snowy directory→receipt→note and source hierarchy; E0 independently reconstructed/verified the extended snapshot, retained the frozen legacy digest, and tested local editing/two-tab conflict rejection. `csoi/browser-snowy.log`, `browser-snowy-source.json`, refreshed screenshots.
- PASS independent original-byte/465page/research-anchor verifier: `tools/verify-document-anchors.py` with `sources/snowy-dcp-research-anchors.json`; result `csoi/snowy-anchor-verification.json`.
- PASS four original/anchor corruption negatives: rawdigest, pagehash, missingtoken and out-of-bounds page rejected; `csoi/snowy-anchor-negative.json`.
- PASS immutable proof naming/path checks and retained historical-prefix tests. No PDF/HTML original body committed.

Generated outputs: `tools/fetch-csoi-document.py` fetches only one exact registered Council PDF lead, with bounded streaming, default TLS/proxy, same-host redirect checks, explicit exchange counts and failure classification; originals/receipts go only to `/tmp`. `tools/csoi-append-receipts.cjs TEMP_BATCH.json --apply` verifies the temporary originals and appends metadata/events plus an immutable content-addressed proof. JSON/JS source mirrors and own notes are committed. The Python anchor verifier independently reads the temporary original and emits metadata/digests only. Missing originals, mismatched hashes or unsupported parser versions fail explicitly. No automatic budget, legal or admission action occurs.

Full-system acceptance remains PARTIAL:49VERIFIED/28PARTIAL/3BLOCKED. Next batch is recursive source-pinned chapter/clause decomposition, followed by typed path-set comparison and research-work/calendar links. COI-002/031/040 remain deferred for separately authorised private WCOS access. No deploy, merge, paid service, main/PR129 change or Council nonpublic data.
