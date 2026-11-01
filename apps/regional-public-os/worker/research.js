(() => {
  const status = document.getElementById('researchStatus');
  const cards = document.getElementById('researchCards');
  const node = (tag, text, className) => {
    const result = document.createElement(tag);
    if (text !== undefined) result.textContent = text;
    if (className) result.className = className;
    return result;
  };
  const publications = {PUBLISHED_PRIVATE_V2:'已发布 · 私有 Sites v2', NOT_ON_SITES:'尚未在 Sites 展示'};
  const stages = {VERIFIED_HISTORICAL_RECORD:'历史记录已验证', VERIFIED_REFERENCE_ONLY:'补充引用已验证', PARTIAL_EMPIRICAL_ONLY:'局部验证 · 仍有阻塞', STALE_SNAPSHOT:'快照过期 · 需复核'};
  async function load() {
    try {
      const response = await fetch('/api/research-progress', {cache:'no-store'});
      if (!response.ok) throw new Error('Research evidence unavailable');
      const data = await response.json();
      if (!['RECORDED_SNAPSHOT','STALE_SNAPSHOT'].includes(data.snapshot_status) || data.deployment_status !== 'NOT_DEPLOYED' || data.cards.length !== 3) throw new Error('Unknown snapshot');
      const stale = data.snapshot_status === 'STALE_SNAPSHOT';
      status.dataset.state = data.snapshot_status;
      status.textContent = stale
        ? '快照已过期：以下仅是上次记录，不代表当前进度。需要人工复核后重新生成；不会自动刷新证据。'
        : '固定证据快照已核对。下列状态来自验收记录；没有实时检查线上网站或研究任务。';
      document.getElementById('snapshotMeta').textContent = `证据截至 ${data.evidence_as_of} · 页面清单生成 ${data.generated_on} · 人工状态复核窗口 ${data.review_window_days} 天（不是科学数据有效期）`;
      for (const card of data.cards) {
        if (!stages[card.display_status] || !publications[card.publication_status]) throw new Error('Unknown card state');
        const article = node('article', undefined, 'card');
        article.dataset.state = card.display_status;
        const heading = node('h2', card.title); heading.id = 'heading-' + card.id;
        article.setAttribute('aria-labelledby', heading.id);
        article.append(node('span', card.id, 'number'), heading);
        article.append(node('span', stale ? '上次发布记录：' + publications[card.publication_status] : publications[card.publication_status], 'badge' + (stale || card.publication_status === 'NOT_ON_SITES' ? ' pending' : '')));
        article.append(node('span', stages[card.display_status], 'badge' + (stale || card.id === 'P04' ? ' pending' : '')));
        article.append(node('p', card.scope, 'scope'), node('p', card.summary));
        const facts = node('dl');
        for (const fact of card.facts) facts.append(node('dt', fact.label), node('dd', fact.value));
        article.append(facts, node('p', '适用边界', 'number'));
        const limits = node('ul');
        for (const limit of card.limits) limits.append(node('li', limit));
        article.append(limits);
        const details = node('details'), evidence = node('ul', undefined, 'evidence');
        details.append(node('summary', `查看证据 · 记录日期 ${card.evidence_date}`));
        for (const id of card.evidence_ids) {
          const ref = data.evidence[id], item = node('li'), link = node('a', ref.path);
          link.href = ref.url; link.target = '_blank'; link.rel = 'noopener noreferrer';
          item.append(link, node('small', '证据日期 ' + ref.recorded_on), node('small', 'Git commit ' + ref.commit), node('small', 'SHA256 ' + ref.sha256 + ' · ' + ref.bytes + ' bytes'));
          evidence.append(item);
        }
        details.append(evidence); article.append(details); cards.append(article);
      }
      document.getElementById('manifestDigest').textContent = '进度清单 SHA256 ' + data.manifest_sha256 + ' · 来源提交 ' + data.source_commit;
      cards.hidden = false;
    } catch {
      cards.replaceChildren(); cards.hidden = true;
      document.getElementById('snapshotMeta').textContent = '';
      document.getElementById('manifestDigest').textContent = '';
      status.dataset.state = 'UNKNOWN';
      status.textContent = '研究进度暂不可验证（UNKNOWN）。证据缺失、绑定错误或服务不可用；已隐藏进度卡片，请人工复核。历史流量页面仍可独立查看。';
    }
  }
  load();
})();
