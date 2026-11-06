"""Read-only source audit. Never execute upstream MATLAB or infer emissions."""
from pathlib import Path
import csv, datetime as dt, hashlib, io, json, statistics, zipfile
import openpyxl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RAW = ROOT / 'runtime_data/local_case_method_intake'
OUT = HERE / 'evidence'

def digest(b):
    return hashlib.sha256(b).hexdigest()

def audit():
    receipts = json.loads((OUT/'acquisition.json').read_text())
    for r in receipts['records']:
        if r.get('local_original'):
            b = (ROOT/r['local_original']).read_bytes()
            assert digest(b) == r['sha256'], 'Original changed'
            assert hashlib.md5(b).hexdigest() == r['md5']
    with zipfile.ZipFile(RAW/'Data for Network SL1.zip') as z:
        member = 'Data for Network SL1/Measured_Methane_Data_SL1.xlsx'
        b = z.read(member)
        w = openpyxl.load_workbook(io.BytesIO(b), read_only=True, data_only=True)
        rows = list(w['Measured_Data'].values)
        assert rows[0] == ('Date and Time', 'CH4 Concentration (mg/L)')
        measured = [(t, float(v)) for t,v in rows[1:]]
        assert all(isinstance(t,dt.datetime) and t.tzinfo is None for t,v in measured)
        assert all(v >= 0 for t,v in measured)
        fw = openpyxl.load_workbook(io.BytesIO(z.read('Data for Network SL1/Sewer_Flow_Data_SL1.xlsx')),read_only=True,data_only=True)
        flows = list(fw['Sewer_1'].values)[1:]
        author_summary = list(fw['Summary'].values)[1]
        counts = {}
        for t,v in flows: counts[t] = counts.get(t,0)+1
        fmean = statistics.mean(v for t,v in flows)
        assert len(flows) == author_summary[1]
        assert abs(fmean-author_summary[4]) < 1e-10
        feed = openpyxl.load_workbook(io.BytesIO(z.read('Data for Network SL1/Feed_Data_SL1.xlsx')),read_only=True,data_only=True)
        feed_rows = list(feed.worksheets[0].values)
        feed_schema = [{'column_1_based':i+1,'label':feed_rows[2][i], 'unit_or_header':feed_rows[3][i+1] if i+1<len(feed_rows[3]) else None} for i in range(0,len(feed_rows[2]),3) if feed_rows[2][i]]
    with zipfile.ZipFile(RAW/'Fig2_S2.zip') as z:
        txt=z.read('Fig2_S2/Measured_Data_Plotting_Moonstone_Fig2C.txt').decode('utf-8-sig')
        lines=[s for s in txt.splitlines() if s.strip()]
        plotted=[(dt.datetime.strptime(r['DateTime'],'%d-%b-%Y %H:%M:%S'),float(r['CH4'])) for r in csv.DictReader(lines)]
        assert plotted == measured, 'Published plotting input differs from workbook'
        script=z.read('Fig2_S2/Fig2_S2_field_data.m').decode('utf-8-sig')
        assert 'Dissolved' in script and 'mg/L' in script
    values=[v for t,v in measured]
    result = {
      'status':'RAW_DATA_AUDIT_PASSED_WITH_LIMITS', 'measurement_operator':'author-labelled dissolved CH4 concentration; not atmospheric mole fraction or emission flux',
      'site_label':'SL1; same values labelled Moonstone in author plotting input; geography and sampling instrumentation not established from acquired originals',
      'count':len(measured),'missing_time':sum(t is None for t,v in measured),'missing_value':sum(v is None for t,v in measured),
      'duplicate_timestamps':len(measured)-len(set(t for t,v in measured)),
      'time_start_naive':min(t for t,v in measured).isoformat(),'time_end_naive':max(t for t,v in measured).isoformat(),
      'timezone':None, 'utc_conversion_performed':False,
      'unit':'mg/L dissolved CH4','mean_sample_weighted':statistics.mean(values),'median':statistics.median(values),'min':min(values),'max':max(values),
      'not_time_weighted':True,'elapsed_hours':(max(t for t,v in measured)-min(t for t,v in measured)).total_seconds()/3600,
      'member_sha256':digest(b),'plotting_input_exact_match':True,'independent_dataset_count':1,
      'flow':{'rows':len(flows),'unique_timestamps':len(counts),'excess_rows_on_repeated_time':len(flows)-len(counts),'timestamps_with_repeats':sum(v>1 for v in counts.values()),'start_naive':min(t for t,v in flows).isoformat(),'end_naive':max(t for t,v in flows).isoformat(),'row_arithmetic_mean_lps':fmean,'author_summary_mean_lps':author_summary[4],'author_summary_mean_reproduced':True,'physical_time_mean_established':False,'join_to_methane_performed':False},
      'feed_schema':feed_schema,
      'gaps':['timezone/UTC','instrument, calibration, analytical uncertainty','sampling and phase-transfer protocol','site coordinates and verified geographic mapping','independent validation split','co-located meteorology and station absolute pressure'],
      'D3':'DATA_NOT_READY','P1-A':'PENDING','science_review':'PENDING',
      'executed':['archive/member hash checks','read-only field/QC audit','author-labelled measured plotting input cross-check','author flow summary arithmetic reproduction','sample descriptive statistics'],
      'not_executed':['upstream MATLAB','SeweX','new fitting/inversion','gas ideal-law conversion on dissolved samples','C x Q emission estimate','P2/P4 real calibration','ACCU/AWT','production deployment']}
    OUT.mkdir(exist_ok=True)
    (OUT/'qc-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    with (OUT/'measured-transcription.csv').open('w',newline='',encoding='utf-8') as f:
        out=csv.writer(f);out.writerow(['source_row_1_based','time_as_stored_no_timezone','dissolved_ch4_mg_per_l','dissolved_ch4_g_per_m3','conversion_factor','source_member'])
        for i,(t,v) in enumerate(measured,2): out.writerow([i,t.isoformat(),v,v,1,member])
    return result,measured

if __name__=='__main__':
    result,measured=audit()
    print(json.dumps(result,ensure_ascii=False,indent=2))
