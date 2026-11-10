"""Second implementation: raw integer precipitation and exact rational sums.

No production parser, aggregation, phase, quantile or statistics helper imports.
This is an independently implemented check, not independent human review.
"""
import csv, json
from fractions import Fraction as F
from pathlib import Path
from statistics import median
TASK=Path(__file__).resolve().parents[1];ROOT=TASK.parents[2]
def audit():
    stations=[]
    for sid in ('ASN00072150','ASN00074104','ASN00072008'):
        values={}
        with (TASK/'evidence/raw'/f'{sid}.csv').open(newline='',encoding='ascii') as f:
            for raw in csv.reader(f,skipinitialspace=True):
                r=[s.strip() for s in raw];date=r[5]
                assert r[0]==sid and date not in values
                values[date]=int(r[6]) if not r[7] and not r[8] and r[9]=='D' and int(r[6])>=0 else None
        stations.append(values)
    roni={}
    for line in (ROOT/'docs/tasks/climateos_physical_process_trajectory_001/evidence/RONI.ascii.txt').read_text().splitlines()[1:]:
        s,y,v=line.split();roni[int(y),s]=F(v)
    out={}
    for predictor,response,months in [('JJA','JJA',(6,7,8)),('SON','SON',(9,10,11)),('JJA','SON',(9,10,11))]:
        rain={}
        for y in range(1961,2021):
            vals=[st.get(f'{y}{m:02}') for st in stations for m in months]
            rain[y]=None if None in vals else F(sum(vals),30)
        base=[v for y,v in rain.items() if y<=1990 and v is not None]
        valid=sum(v is not None for v in rain.values())
        result={'valid_baseline':len(base),'valid_total':valid,'gate':len(base)>=24 and valid>=40}
        if result['gate']:
            ordered=sorted(base)
            def quantile(q):
                h=(len(ordered)-1)*q;i=int(h)
                return ordered[i]+(h-i)*(ordered[min(i+1,len(ordered)-1)]-ordered[i])
            lo,hi=quantile(F(1,5)),quantile(F(4,5))
            threshold=median(base);counts={p:{'n':0,'dry':0,'wet':0,'neither':0,'extreme_dry':0,'extreme_wet':0} for p in ('warm','cold','neutral')}
            phases={};values={}
            for y,v in rain.items():
                if v is None:continue
                index=roni[y,predictor];phase='warm' if index>=F(1,2) else 'cold' if index<=-F(1,2) else 'neutral'
                phases[y]=phase;values[y]=float(v);counts[phase]['n']+=1
                counts[phase]['dry' if v<threshold else 'wet' if v>threshold else 'neither']+=1
                counts[phase]['extreme_dry']+=int(v<lo);counts[phase]['extreme_wet']+=int(v>hi)
            result.update(threshold_fraction=str(threshold),threshold_mm=float(threshold),counts=counts,
                          exact_rain_mm=values,phases=phases)
        out[predictor+'_'+response]=result
    return out
if __name__=='__main__':print(json.dumps(audit(),indent=2,sort_keys=True))
