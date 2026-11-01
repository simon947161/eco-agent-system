// Reads only the fixed, committed repository files below. No database or network access.
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {readFile, writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {evidenceCommit, evidenceRepository, taskDirectory, evidenceFiles, evaluateProgress} from '../worker/research-progress.mjs';

const app = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const repo = path.resolve(app, '../..');
export const manifestPath = path.join(app, 'data/research-progress.json');
export const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
const requireFact = (condition, message) => { if (!condition) throw new Error('Evidence review required: ' + message); };

export function generateProgress() {
  const evidence = {}, sources = {};
  for (const [id, [file, date]] of Object.entries(evidenceFiles)) {
    const sourcePath = taskDirectory + file;
    const bytes = execFileSync('git', ['show', `${evidenceCommit}:${sourcePath}`], {cwd: repo, maxBuffer: 1024 * 1024});
    sources[id] = file.endsWith('.json') ? JSON.parse(bytes.toString('utf8')) : bytes.toString('utf8');
    evidence[id] = {commit: evidenceCommit, path: sourcePath, recorded_on: date,
      sha256: sha256(bytes), bytes: bytes.length,
      url: `https://github.com/${evidenceRepository}/blob/${evidenceCommit}/${sourcePath}`};
  }
  const state = sources.execution, hrs = state.workstreams.p02_streamflow;
  const monthly = sources.p03_reference, soil = sources.soil_result, rain = sources.rainfall_result;
  requireFact(state.schema === 'climateos.regional_public_os.execution_state.v1' && state.updated_on === '2026-10-31', 'execution state');
  requireFact(state.site.deployment_verified === true && state.site.version_number === 2 && state.site.access_mode === 'custom_owner_only', 'P02 private publication');
  requireFact(hrs.records === 22645 && hrs.coverage_start === '1964-03-01' && hrs.coverage_end === '2026-02-28' && hrs.human_scientific_review === 'pending', 'P02 scope');
  requireFact(state.site.p03_deployment_performed === false && monthly.year_month === '2026-07' && monthly.link.reference_status === 'VERIFIED_REFERENCE_ONLY', 'P03 status');
  requireFact(monthly.link.association_meaning === 'POSTHOC_READ_ONLY_REFERENCE_NOT_PART_OF_ORIGINAL_MONTHLY_REVIEW' && monthly.existing_project_tables_unchanged === true && monthly.link.original_monthly_receipt_amended === false, 'P03 retrospective scope');
  requireFact(soil.status === 'PARTIAL' && soil.month === '2000-07' && soil.cell.latitude === -36.25 && soil.cell.longitude === 149.1 && soil.metadata['day-sm_pct'].valid_samples === 31, 'P04 sample scope');
  requireFact(soil.comparisons.sm_pct.status === 'PASS_EMPIRICAL_COMPARISON' && soil.comparisons.sm_pct.daily_mean.agrees === true && soil.comparisons.sm_pct.final_day.agrees === false && soil.provider_general_semantics_proven === false && soil.scientific_admission === false && soil.cross_source_numeric_join === 'BLOCKED', 'P04 limited soil result');
  requireFact(rain.status === 'BLOCKED_EXACT_DAILY_MONTHLY_LINEAGE_UNVERIFIED' && rain.source_mapping.daily_physical_sample_acquired === false && rain.source_mapping.monthly_sum_compared === false && rain.blocked_inventory_request.arcgis_error_code === 499 && rain.blocked_inventory_request.retry_count === 0 && rain.scientific_admission === false, 'P04 stopped rainfall state');
  requireFact(state.automation.schedule_created === false && state.automation.unattended_write_readback_verified === false, 'automation');
  const fact = (label, value) => ({label, value: String(value)});
  const manifest = {
    schema: 'climateos.owner_research_progress.v1', repository: evidenceRepository,
    source_commit: evidenceCommit, generated_on: '2026-11-01', evidence_as_of: state.updated_on,
    deployment_status: 'NOT_DEPLOYED', automation_status: 'NOT_ESTABLISHED', scientific_admission: false,
    evidence,
    cards: [
      {id: 'P02', title: '历史流量网站', recorded_status: 'VERIFIED_HISTORICAL_RECORD', publication_status: 'PUBLISHED_PRIVATE_V2',
        evidence_date: '2026-10-26', scope: `HRS 410033 · ${hrs.coverage_start} 至 ${hrs.coverage_end} · ${hrs.records.toLocaleString('en-US')} 条日记录`,
        summary: '已在 Owner 私有网站展示历史流量、质量标记和证据链。网站验收记录日期为 2026-10-26，本页没有重新检查线上状态。',
        facts: [fact('网站版本', 'Sites v2 · Owner 私有'), fact('最后观测日', hrs.coverage_end), fact('数据版本标签', hrs.source_version),
          fact('网站源提交', state.site.sites_source_commit), fact('网站实现提交', state.site.github_implementation_commit)],
        limits: ['历史数据不能表示当前水况；数据版本标签不是最后观测日期。', '人工科学复核仍待完成；不能据此判断饮水能力、污染或因果关系。'],
        evidence_ids: ['p02', 'execution']},
      {id: 'P03', title: '月度研究证据引用', recorded_status: 'VERIFIED_REFERENCE_ONLY', publication_status: 'NOT_ON_SITES',
        evidence_date: '2026-10-26', scope: '2026 年 7 月已有研究周期 · 一条事后只读补充引用',
        summary: '仓库验收记录证明：已在原本的本地研究流程中挂接历史流量证据。本页仅展示已提交的验收信息。',
        facts: [fact('研究月份', monthly.year_month), fact('引用编号', monthly.link.reference_id), fact('原始研究记录', '验收记录：原有六张表未改变；原 Receipt 未修改')],
        limits: ['这条引用是在原 7 月研究审阅后补加，不属于原始月度审阅证据。', '引用功能尚未部署到 Sites；本页没有读取、复制或迁移原始月度数据库。', '近期 WaterNSW 数据仍因凭据绑定未恢复而受阻；未建立自动更新。'],
        evidence_ids: ['p03', 'p03_reference', 'execution']},
      {id: 'P04', title: '土壤与降雨验证', recorded_status: 'PARTIAL_EMPIRICAL_ONLY', publication_status: 'NOT_ON_SITES',
        evidence_date: '2026-10-31', scope: 'AWRA-L v7 · 2000 年 7 月 · 36.25°S / 149.10°E 单个网格（525 / 742）',
        summary: '已有的 31 天土壤样本支持：该格点该月的月值与日均值在预设容差内一致，与月末日值不一致。降雨日值与月值的精确产品来源关系仍未确认。',
        facts: [fact('土壤月值（原始比例）', soil.comparisons.sm_pct.daily_mean.observed), fact('31 天均值（原始比例）', soil.comparisons.sm_pct.daily_mean.reference),
          fact('降雨验证', 'BLOCKED · 来源关系未确认，未比较日值总和'), fact('受阻访问', 'ArcGIS 499 Token Required · 已停止，未重试')],
        limits: ['仅是一个格点、一个月的经验复现，不能推广为产品通用规则或流域结论。', 'HRS 日界线与夏令时、月度质量及完整性、流域网格准入仍未解决。', '没有科学准入、跨来源数值拼接或因果结论；降雨调查保持停止。'],
        evidence_ids: ['soil', 'soil_result', 'rainfall', 'rainfall_result', 'execution']},
    ],
  };
  evaluateProgress(manifest, Date.parse('2026-11-01T00:00:00Z'));
  return JSON.stringify(manifest, null, 2) + '\n';
}

export function verifyProgressBytes(actual) {
  requireFact(actual === generateProgress(), 'generated manifest differs from pinned Git evidence; run generator and review');
  return actual;
}

export async function checkedProgress() {
  return verifyProgressBytes(await readFile(manifestPath, 'utf8'));
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  if (process.argv.slice(2).some(arg => arg !== '--check')) throw new Error('Only --check is supported');
  if (process.argv.includes('--check')) await checkedProgress();
  else await writeFile(manifestPath, generateProgress());
  console.log(process.argv.includes('--check') ? 'Pinned evidence links, bytes and generated manifest match.' : 'Generated NOT_DEPLOYED research manifest from pinned Git evidence.');
}
