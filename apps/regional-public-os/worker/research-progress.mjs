// Frozen public-safe evidence contract. A new evidence batch needs an explicit review/update.
export const evidenceCommit = '9a2f31660889e6272cdeb8a21d34583c838947c3';
export const evidenceRepository = 'simon947161/eco-agent-system';
export const taskDirectory = 'docs/tasks/climateos_regional_public_os_001/';
export const evidenceFiles = {
  execution: ['EXECUTION_STATE.json', '2026-10-31'],
  p02: ['P02_SITES_PRIVATE_ACCEPTANCE.md', '2026-10-26'],
  p03: ['P03_ACCEPTANCE_20261026.md', '2026-10-26'],
  p03_reference: ['P03_MONTHLY_REFERENCE_ACCEPTANCE.json', '2026-10-26'],
  soil: ['P04_AWRA_REPRODUCTION_20261031.md', '2026-10-31'],
  soil_result: ['P04_AWRA_REPRODUCTION_RESULT_20261031.json', '2026-10-31'],
  rainfall: ['P04_RAINFALL_LINEAGE_REVIEW_20261031.md', '2026-10-31'],
  rainfall_result: ['evidence/p04_rain_lineage_20261031/candidate-result.json', '2026-10-31'],
};
const cardContracts = [
  ['P02', 'VERIFIED_HISTORICAL_RECORD', 'PUBLISHED_PRIVATE_V2', ['p02', 'execution'], '2026-10-26'],
  ['P03', 'VERIFIED_REFERENCE_ONLY', 'NOT_ON_SITES', ['p03', 'p03_reference', 'execution'], '2026-10-26'],
  ['P04', 'PARTIAL_EMPIRICAL_ONLY', 'NOT_ON_SITES', ['soil', 'soil_result', 'rainfall', 'rainfall_result', 'execution'], '2026-10-31'],
];
const requireValue = (condition, message) => { if (!condition) throw new Error(message); };
const isoDay = value => {
  requireValue(typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value), 'Unknown evidence date');
  const time = Date.parse(value + 'T00:00:00Z');
  requireValue(Number.isFinite(time) && new Date(time).toISOString().slice(0, 10) === value, 'Invalid evidence date');
  return time;
};

export function evaluateProgress(manifest, now = Date.now()) {
  requireValue(manifest.schema === 'climateos.owner_research_progress.v1', 'Unknown manifest schema');
  requireValue(manifest.source_commit === evidenceCommit && manifest.repository === evidenceRepository, 'Wrong source binding');
  requireValue(manifest.deployment_status === 'NOT_DEPLOYED' && manifest.automation_status === 'NOT_ESTABLISHED' && manifest.scientific_admission === false, 'Unknown release or gate state');
  requireValue(manifest.evidence_as_of === '2026-10-31' && manifest.generated_on === '2026-11-01', 'Unreviewed snapshot date');
  const asOf = isoDay(manifest.evidence_as_of), generated = isoDay(manifest.generated_on);
  requireValue(Number.isFinite(now) && now >= generated && generated >= asOf, 'Future snapshot or unknown clock');
  requireValue(Object.keys(manifest.evidence).sort().join() === Object.keys(evidenceFiles).sort().join(), 'Missing or unknown evidence');
  for (const [id, [file, date]] of Object.entries(evidenceFiles)) {
    const evidence = manifest.evidence[id], sourcePath = taskDirectory + file;
    requireValue(evidence.commit === evidenceCommit && evidence.path === sourcePath && evidence.recorded_on === date, 'Incorrect evidence binding: ' + id);
    requireValue(/^[a-f0-9]{64}$/.test(evidence.sha256) && Number.isSafeInteger(evidence.bytes) && evidence.bytes > 0, 'Invalid evidence receipt');
    requireValue(evidence.url === `https://github.com/${evidenceRepository}/blob/${evidenceCommit}/${sourcePath}`, 'Unpinned evidence link');
  }
  requireValue(Array.isArray(manifest.cards) && manifest.cards.length === cardContracts.length, 'Missing or unknown workstream');
  for (const [i, [id, state, publication, refs, date]] of cardContracts.entries()) {
    const card = manifest.cards[i];
    requireValue(card.id === id && card.recorded_status === state && card.publication_status === publication, 'Unknown workstream state');
    requireValue(JSON.stringify(card.evidence_ids) === JSON.stringify(refs) && card.evidence_date === date, 'Wrong card evidence association');
    requireValue(typeof card.scope === 'string' && card.scope.length > 0 && typeof card.summary === 'string' && Array.isArray(card.limits) && card.limits.length > 0, 'Missing scope or limits');
  }
  // Seven days is a manual status-review window, not a source freshness/scientific rule.
  const ageDays = Math.floor((now - asOf) / 86400000), stale = ageDays > 7;
  return {...manifest, review_window_days: 7, snapshot_age_days: ageDays,
    snapshot_status: stale ? 'STALE_SNAPSHOT' : 'RECORDED_SNAPSHOT',
    live_status_verified: false,
    cards: manifest.cards.map(card => ({...card, display_status: stale ? 'STALE_SNAPSHOT' : card.recorded_status}))};
}
