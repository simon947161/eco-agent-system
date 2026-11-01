"""P04 preparation: source-quality availability, not a climate/causal analysis."""
import argparse
import json
import sys
from calendar import monthrange
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from cczps_lite.environmental_question_runtime.evidence_links import accepted_reference, INDEX


def preflight():
    reference=accepted_reference()
    index=json.loads(INDEX.read_bytes())
    months=defaultdict(list)
    for shard in index['shards']:
        for row in json.loads((INDEX.parent/shard['file']).read_bytes()):
            if '2000-01-01' <= row['date'] <= '2025-12-31':
                months[row['date'][:7]].append(row)
    availability=[]
    for year in range(2000,2026):
        for month in range(1,13):
            key=f'{year:04}-{month:02}'
            rows=months[key]; counts=Counter(r['quality'] for r in rows)
            availability.append({'year_month':key,'expected_calendar_labels':monthrange(year,month)[1],
                'records':len(rows),'missing_calendar_labels':monthrange(year,month)[1]-len(rows),
                'null_values':sum(r['value'] is None for r in rows),
                'quality_counts':{q:counts[q] for q in ('A','B','C','E','G')},
                'a_b_nonnull_days':sum(r['quality'] in ('A','B') and r['value'] is not None for r in rows)})
    return {'case_id':'P04-WATER-SOIL-CLIMATE-001','status':'PREPARED_NOT_SCIENTIFICALLY_EXECUTED',
        'question':'Do precipitation anomalies and antecedent soil moisture align with low-flow months within the same verified upstream catchment, after considering seasonality and competing explanations?',
        'study_period':['2000-01-01','2025-12-31'],'spatial_scope':reference['station'],
        'historical_water_reference':reference,'source_coverage_end':'2026-02-28',
        'availability_method':'Calendar-label counts by original quality code; no value interpolation or physical/statistical inference',
        'monthly_water_availability':availability,
        'missing_dependencies':['Licensed catchment polygon and confirmed gauge spatial alignment',
            'Licensed precipitation series with compatible time/space definition',
            'Licensed soil moisture series with depth/units and observed/modelled distinction',
            'Resolution of daily interval/UTC alignment and source header ambiguity',
            'Independent scientific review of analysis protocol and water record quality'],
        'operational_series':'NOT_ADMITTED; API account/rights and public-layer staleness/units/QC unresolved',
        'environmental_conclusion':None,'causal_conclusion':None,'automatic_updates':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path('.local/p04-water-soil-climate-preflight.json'))
    args=parser.parse_args();result=preflight()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'case_id':result['case_id'],'status':result['status'],'months':len(result['monthly_water_availability']),'missing_dependencies':len(result['missing_dependencies'])}))
