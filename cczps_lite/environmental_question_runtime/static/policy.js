/* Public-reference metadata only; no local paths or source bodies. */
(() => {
  const byId = id => document.getElementById(id);
  const node = (tag, text) => { const item = document.createElement(tag); item.textContent = text; return item; };
  function row(parent, label, value) {
    const item = node('p', `${label}: ${value ?? 'Unknown / 待核'}`); parent.append(item);
  }
  function choices(select, items, title) {
    select.replaceChildren();
    for (const item of items) { const option = node('option', title(item)); option.value = item.id; select.append(option); }
  }
  fetch('/api/policy-context').then(async response => {
    if (!response.ok) throw new Error('Policy metadata unavailable; monthly research is still usable.');
    return response.json();
  }).then(packet => {
    choices(byId('policySource'), packet.sources, item => `${item.id} — ${item.version}`);
    choices(byId('policyLine'), packet.research_lines, item => item.title_zh);
    const renderSource = () => {
      const source = packet.sources.find(item => item.id === byId('policySource').value);
      const card = byId('policySourceCard'); card.replaceChildren(node('h3', source.id));
      for (const [label, value] of Object.entries({Version: source.version, 'Temporal status': source.temporal_status,
        'Local availability this run': source.local_copy_state, 'Prior review scope': source.review_scope,
        'Source locators': source.locators.join('; '), 'Recorded SHA256': source.sha256,
        'Republication licence': source.licence_state})) row(card, label, value);
      try { const url = new URL(source.official_url); if (url.protocol === 'https:') {
        const link = node('a', 'Open official source / 查看官方来源'); link.href = url.href;
        link.target = '_blank'; link.rel = 'noopener noreferrer'; card.append(link);
      }} catch (_) { row(card, 'Official link', 'Unavailable'); }
    };
    const renderLine = () => {
      const line = packet.research_lines.find(item => item.id === byId('policyLine').value);
      const card = byId('policyLineCard'); card.replaceChildren(node('h3', line.title_zh));
      for (const [label, value] of Object.entries({'CSP goals': line.csp.join(', '), 'LSPS actions': line.lsps.join(', '),
        'Mapping status': line.crosswalk, 'Historical DP relationship': (line.dp || []).map(item => `${item.source_id} / ${item.locator} / ${item.relationship}`).join('; ') || 'No explicit implementation mapping verified',
        Hypothesis: line.hypothesis, Metrics: line.metrics.join('; '), 'Counterevidence / stop test': line.failure_test,
        'Opportunity gate': line.opportunity_gate, 'Local evidence gaps': line.evidence_gaps.join(', ') || 'No local copy gaps; scientific validation still required',
        'Review / level': `${line.review_state}; ${line.conclusion_level}/${line.evidence_maturity}`,
        'Next check': 'Verify current DP/OP, local evidence, role owner, cost and authority before considering a trial.'})) row(card, label, value);
      const open = node('button', 'Inspect linked policy / 查看关联政策');
      open.addEventListener('click', () => { byId('policySource').value = line.source_ids[0]; renderSource(); byId('policySource').focus(); }); card.append(open);
    };
    byId('policySource').addEventListener('change', renderSource); byId('policyLine').addEventListener('change', renderLine);
    byId('policyStatus').textContent = `Register reviewed ${packet.as_of}; current DP/OP content unverified. Local access status is checked independently.`;
    byId('policyDigest').textContent = `Metadata packet SHA256: ${packet.packet_digest}. A digest verifies consistency, not environmental truth.`;
    renderSource(); renderLine();
  }).catch(error => { byId('policyStatus').textContent = error.message; });
})();

