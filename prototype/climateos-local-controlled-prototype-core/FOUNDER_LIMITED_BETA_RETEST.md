# Founder Task1199 Gap Patch Retest

1. Run `start_climateos_local_beta.ps1` in PowerShell.
2. Open `http://127.0.0.1:8765`, go to **Alpha Review**, and create one synthetic candidate. Copy its Evidence ID.
3. In **Record a human action**, paste the ID and select **Challenge / dispute**. Enter a declared reviewer label and reason, then record the action.
4. Paste the same ID and choose **Load existing record for correction**. Change the corrected title, summary, or uncertainty, then record the correction.
5. Confirm the readable result has a higher `revision`, retains `revision_history` and `review_history`, and remains a candidate rather than an approved fact.
6. Select **Load Alpha Audit** and confirm both the dispute and correction remain present.
7. In **Evidence Cards**, **Audit Trail**, and the Alpha loaded list, try Date/time and Name/title with both directions. Confirm this changes display order only and does not show a score or scientific ranking.
8. Set browser zoom to 200% and use keyboard navigation; confirm sorting and correction controls remain reachable without horizontal page scrolling.
9. Restart the local service and reload the Evidence ID; confirm its current revision and history recover.

Pass evidence must record browser, Windows version, test date, Evidence ID, final revision number, restart result and any confusing wording. This retest does not authorize real data, public use, scientific conclusions, PR merge or Task1200 work.
