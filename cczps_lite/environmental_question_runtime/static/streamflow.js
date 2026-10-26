/* Read-only historical slice in the existing research Console. */
(() => {
  const el = id => document.getElementById(id);
  const ns = 'http://www.w3.org/2000/svg';
  function shape(tag, attrs) {
    const node = document.createElementNS(ns, tag);
    for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
    el('flowChart').appendChild(node); return node;
  }
  async function load() {
    try {
      const query = new URLSearchParams();
      if (el('flowStart').value) query.set('start', el('flowStart').value);
      if (el('flowEnd').value) query.set('end', el('flowEnd').value);
      const response = await fetch('/api/streamflow?' + query);
      const packet = await response.json();
      if (!response.ok) throw new Error(packet.error);
      el('flowChart').replaceChildren(); el('flowRows').replaceChildren();
      el('flowStatus').textContent = packet.status + (packet.coverage_end ? ` · source ends ${packet.coverage_end} · age ${packet.age_days} days · selected missing dates ${packet.selected_absent_dates}` : ' · no official snapshot imported');
      const {rows, ...evidence} = packet;
      el('flowEvidence').textContent = JSON.stringify(evidence, null, 2);
      if (!packet.coverage_end) return;
      el('flowStart').value = packet.selected_start; el('flowEnd').value = packet.selected_end;
      const start = Date.parse(packet.selected_start), end = Date.parse(packet.selected_end);
      const max = Math.max(1, ...rows.filter(r => r.value !== null).map(r => r.value));
      const x = day => 60 + 810 * (Date.parse(day) - start) / Math.max(86400000, end - start);
      const y = value => 225 - 195 * value / max;
      shape('path', {d:'M60 20V225H880', stroke:'#333', fill:'none'});
      shape('text', {x:5,y:25,fill:'#222'}).textContent = max.toFixed(1);
      shape('text', {x:10,y:225,fill:'#222'}).textContent = '0 ML';
      shape('text', {x:60,y:250,fill:'#222'}).textContent = packet.selected_start;
      shape('text', {x:880,y:250,fill:'#222','text-anchor':'end'}).textContent = packet.selected_end;
      let previous = null;
      for (const row of rows) {
        const tr = document.createElement('tr');
        for (const value of [row.date, row.value === null ? 'MISSING' : row.value, row.quality + ': ' + packet.quality_definitions[row.quality]]) {
          const td = document.createElement('td'); td.textContent = String(value); tr.appendChild(td);
        }
        el('flowRows').appendChild(tr);
        const good = row.value !== null && ['A','B'].includes(row.quality);
        if (good && previous && Date.parse(row.date) - Date.parse(previous.date) === 86400000) {
          shape('path', {d:`M${x(previous.date)} ${y(previous.value)}L${x(row.date)} ${y(row.value)}`, stroke:'#155e90', fill:'none'});
        }
        if (row.value !== null) {
          const dot = shape('circle', {cx:x(row.date),cy:y(row.value),r:good?2:3,fill:good?'#155e90':'#a44c00'});
          const title = document.createElementNS(ns,'title'); title.textContent = `${row.date}: ${row.value} ML; ${row.quality}`; dot.appendChild(title);
        }
        previous = good ? row : null;
      }
    } catch (error) {
      el('flowChart').replaceChildren(); el('flowRows').replaceChildren();
      el('flowEvidence').textContent = ''; el('flowStatus').textContent = 'Unavailable: ' + error.message;
    }
  }
  el('flowLoad').addEventListener('click', load); load();
})();
