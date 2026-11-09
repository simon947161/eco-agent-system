"""Offline extraction from one-shot snapshots and frozen public Git artifacts."""
from pathlib import Path
import hashlib, html, json, re, subprocess

T = Path(__file__).resolve().parent
ROOT = T.parents[2]
CACHE = ROOT/'runtime_data/physical-process-trajectory'

def write(name, value):
    (T/'evidence'/name).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8', newline='\n')

def text(name):
    return re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', ' ', (CACHE/(name+'.raw')).read_text(encoding='utf-8'))))

def main():
    aggi = text('aggi')
    for token in ['1936.03 ± 0.48', '338.86 ± 0.02', '-8.96E-05', '-0.000125', '0.045194', '0.86', '729.2', '2025 2.372 0.569']:
        assert token in aggi, ('MANUAL_SOURCE_FACT_CHANGED', token)
    acq=json.loads((T/'evidence/acquisition.json').read_text())
    write('aggi-facts.json', {
        'source_id':'GML_AGGI', 'source_version':'AGGI 2025 update; retrieved 2026-11-09 UTC',
        'source_sha256':acq['aggi']['sha256'], 'locator':'Observations CH4/N2O paragraphs; Table 1 CH4 and footnotes; Table 2 2025 CH4',
        'M_ppb':1936.03,'M_reported_uncertainty_ppb':0.48,'N_ppb':338.86,'N_reported_uncertainty_ppb':0.02,
        'M0_ppb':729.2,'a':-8.96e-5,'b':-0.000125,'d':0.045194,'e':0.86,
        'published_2025_ERF_W_m2':0.569,'published_decimals':3,
        'unit':'ppb_dry_global_mean','phase':'gas_dry_air_mole_fraction','year':2025,'baseline_year':1750,
        'uncertainty_definition':'Page reports plus/minus abundance uncertainty, but the AGGI page does not define its confidence level. Propagation is a conditional standard-error interpretation, NOT a claimed calibrated 95% interval.',
        'rights':'NOAA GML government numerical data public domain unless otherwise noted; attribution NOAA GML; no endorsement',
        'raw_html_redistributed':False, 'transformation':'Manually transcribed numerical facts, each literal checked against downloaded HTML; no figures or third-party content included'
    })
    method=text('roni-method')
    assert 'ERSSTv6' in method and '1991' in method and 'variance' in method
    write('roni-metadata.json', {'source_id':'CPC_RONI','version':'ERSSTv6; 1991-2020 base; 2026-11-03 file modification',
        'sha256':acq['roni']['sha256'],'raw_file':'RONI.ascii.txt','unit':'degC_relative_SST_anomaly',
        'support':'Niño3.4 5N-5S 120-170W minus tropical 20N-20S SST anomaly, variance-adjusted; three-month mean',
        'seasons':'DJF year names January; NDJ year names December; JJA and SON are non-overlapping within year',
        'quality':'No per-row quality flag or observation uncertainty supplied; reconstructed index, not a raw thermometer series. Most recent two months revisable, full historical revisions possible.',
        'rights':'NOAA/NWS public-domain numerical product; cite CPC, no endorsement; independent analysis is ClimateOS authored',
        'weather_candidate_status':'DATA_NOT_READY',
        'weather_reason':'BoM product terms explicitly allow study/research; they do not establish unrestricted raw redistribution. Parameterized rainfall discovery page was inaccessible to the web reader (not an asserted HTTP403). No raw payload URL/content was obtained; no retry or alternate endpoint pursued. No weather probability computed.'})
    sha='987cc1dc7170204e5eab3d1750590ba463ea9d08'
    def gitfile(f):
        return subprocess.check_output(['git','show',sha+':apps/regional-public-os/data/'+f],cwd=ROOT)
    indexraw=gitfile('index.json'); index=json.loads(indexraw); raw=gitfile('2020.json')
    expected=next(s['sha256'] for s in index['shards'] if s['file']=='2020.json')
    assert hashlib.sha256(raw).hexdigest()==expected
    assert hashlib.sha256(indexraw).hexdigest()=='bd4728ea129330d5e1abd35dce9b223df87c6801c18ad52e7d9db0eb7e0d45ca'
    data=json.loads(raw)
    rows=data if isinstance(data,list) else data['records']
    selected=[r for r in rows if '2020-01-01'<=r['date']<='2020-01-31']
    write('hrs-january-2020.json', {'source_id':'HRS_INHERITED','git_commit':sha,'git_path':'apps/regional-public-os/data/2020.json',
        'parent_shard_sha256':expected,'parent_index_sha256':hashlib.sha256(indexraw).hexdigest(),
        'raw_source_reacquired':False,'metadata':index['metadata'],'rows':selected,
        'transformation':'Selected Jan 2020 from pinned public derived shard. No values changed; no imputation, flow conversion or UTC assignment.',
        'scope':'Cooma QC example only; NOT Nile measurement'})
    act=text('au-act')
    assert '43% below 2005 levels by 2030' in act and 'Compilation No. 2' in act
    old=json.loads((T.parent/'global_natural_systems_evidence_atlas_001/evidence/scorecard-facts.json').read_text())
    au=next(r for r in old['records'] if r['name']=='Australia')
    write('scorecard-audit-facts.json', {
        'source_id':'SCORECARD_AU','direct_current_retrieval':acq['scorecard'],
        'web_reader_observation':'Before the direct 403, web reader exposed the disputed wording at the original URL. Reader cache/version freshness cannot be independently established. No retry after 403.',
        'historical_snapshot_sha256':old['source_sha256'], 'page_datePublished':old['datePublished'],'page_dateModified':old['dateModified'],
        'date_scope':'Page-wide metadata; not verified as Australian-card publication/revision dates',
        'short_quote':'by 2030 compared with the base year of 2030',
        'locator':'Australia accordion, question 2 response',
        'responses':['No','No','No','Yes','Yes'], 'response_provenance':'Web reader visible Australian card, not a new direct byte snapshot',
        'published_label':au['published_percent_label'],'label_basis':'PR146 frozen CSS extraction, not independently re-downloaded now',
        'rubric':'Five questions worth 20 points each; partial-credit detail not independently established',
        'law':{'source_id':'AU_ACT','compilation':'C2025C00153; Compilation 2','effective_date':'2025-02-20','registration_date':'2025-02-27',
            'section':'10(1)(a)','reduction_percent':43,'baseline_year':2005,'target_year':2030,
            'implementation':'point target and 2021-2030 emissions budget','net_zero_year':2050,'sha256':acq['au-act']['sha256']},
        'contact_status':'NOT_SENT','score_wrong_proven':False})
    print('Extracted AGGI, RONI metadata, HRS fixed-window subset, Scorecard/law facts')

if __name__=='__main__': main()
