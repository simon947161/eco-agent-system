"""Small CF-inspired state/mediator subset, not a CF or BMI implementation."""
from __future__ import annotations
from dataclasses import dataclass, asdict, replace
from datetime import datetime
import hashlib, json, math

class Rejection(ValueError):
    def __init__(self, code, detail=''):
        self.code=code;self.detail=detail;super().__init__(code+(': '+detail if detail else ''))
def need(ok,code,detail=''):
    if not ok:raise Rejection(code,detail)
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def digest(v):return hashlib.sha256(canonical(v).encode()).hexdigest()

# unit, dimensions(M,L,T,Theta), CF name or explicit local semantic identifier,
# medium, temporal meaning. These are field definitions, not source admission.
CATALOG={
 'ta':('K',(0,0,0,1),'air_temperature','gas','instantaneous'),
 'ts':('K',(0,0,0,1),'surface_temperature','surface','instantaneous'),
 'pressure':('Pa',(1,-1,-2,0),'air_pressure','gas','instantaneous'),
 'u':('m s-1',(0,1,-1,0),'eastward_wind','gas','instantaneous'),
 'v':('m s-1',(0,1,-1,0),'northward_wind','gas','instantaneous'),
 'q':('kg kg-1',(0,0,0,0),'specific_humidity','gas','instantaneous'),
 'rain':('kg m-2 s-1',(1,-2,-1,0),'precipitation_flux','liquid','mean_flux'),
 'rain_amount':('kg m-2',(1,-2,0,0),'precipitation_amount','liquid','accumulated'),
 'rn':('W m-2',(1,0,-3,0),None,'surface','mean_flux'),
 'water':('kg m-2',(1,-2,0,0),None,'soil_liquid','instantaneous'),
 'evap':('kg m-2 s-1',(1,-2,-1,0),'water_evaporation_flux','liquid_to_gas','mean_flux'),
 'runoff':('kg m-2 s-1',(1,-2,-1,0),'runoff_flux','liquid','mean_flux'),
 'ch4':('ppb_dry_global_mean',(0,0,0,0),None,'gas_dry','annual_mean'),
 'n2o':('ppb_dry_global_mean',(0,0,0,0),None,'gas_dry','annual_mean'),
 'erf':('W m-2',(1,0,-3,0),None,'global_toa','annual_mean'),
 'roni':('K',(0,0,0,1),None,'ocean_anomaly','seasonal_mean'),
 'enso_phase':('1',(0,0,0,0),None,'statistical_context','seasonal_mean')}
KINDS={'OBSERVED_STATE','CONSTRAINED_ESTIMATE','SIMULATED_STATE','HYPOTHESIS_SCENARIO'}

@dataclass(frozen=True)
class Grid:
    id:str
    crs:str
    cells:tuple[tuple[float,float,float,float],...]
    support:str='area'
    vertical:str='surface/idealised_mixed_layer'
    def validate(self):
        need(self.support in ('area','point','global','index_region'),'SPATIAL_SUPPORT')
        need(1<=len(self.cells)<=16,'GRID_BUDGET')
        for c in self.cells:need(len(c)==4 and all(math.isfinite(x) for x in c) and c[1]>c[0] and c[3]>c[2],'CELL_BOUNDS')
        if self.support=='area':
            need(self.crs=='LOCAL_CARTESIAN_METRES','AREA_CRS_REQUIRES_VALIDATED_TRANSFORM')
            for i,a in enumerate(self.cells):
                for b in self.cells[i+1:]:need(overlap(a,b)==0,'OVERLAPPING_CELLS')
        return self
    @property
    def areas(self):return tuple((b-a)*(d-c) for a,b,c,d in self.cells)
    @classmethod
    def strip(cls,n=2,length=2000.):
        need(type(n) is int and 1<=n<=16,'GRID_BUDGET')
        return cls(f'local_{n}','LOCAL_CARTESIAN_METRES',tuple((i*length/n,(i+1)*length/n,0.,1000.) for i in range(n))).validate()

@dataclass(frozen=True)
class TimeSupport:
    start:str
    end:str
    calendar:str='proleptic_gregorian'
    local_clock:str='UTC; no inferred local observation day'
    def seconds(self):
        need(self.calendar=='proleptic_gregorian','CALENDAR')
        try:a,b=(datetime.fromisoformat(x.replace('Z','+00:00')) for x in (self.start,self.end))
        except ValueError:raise Rejection('TIME_FORMAT')
        need(a.tzinfo is not None and b.tzinfo is not None,'NAIVE_TIME')
        dt=(b-a).total_seconds();need(dt>0,'TIME_BOUNDS');return dt

@dataclass(frozen=True)
class Field:
    id:str
    values:tuple[float|None,...]
    grid:Grid
    time:TimeSupport
    unit:str
    kind:str
    source_id:str
    source_version:str
    input_sha256:str
    license:str
    qc:str
    uncertainty:tuple[float|None,...]
    covariance:tuple[tuple[float,...],...]|None=None
    lineage:tuple[str,...]=()
    extensive:bool=False
    evidence_level:str='SYNTHETIC_TESTED'
    method_version:str='earth-coupling/1'
    reference_conditions:str='declared idealised boundary; no real site attribution'
    def validate(self):
        need(self.id in CATALOG,'UNKNOWN_FIELD');need(self.unit==CATALOG[self.id][0],'UNIT_MISMATCH',self.id)
        self.grid.validate();self.time.seconds();need(self.kind in KINDS,'STATE_CLASS')
        n=len(self.grid.cells);need(len(self.values)==len(self.uncertainty)==n,'FIELD_SHAPE')
        need(bool(self.source_id and self.source_version and self.license and self.qc and self.reference_conditions),'PROVENANCE')
        need(len(self.input_sha256)==64 and all(c in '0123456789abcdef' for c in self.input_sha256),'SOURCE_HASH')
        need(not self.extensive,'CATALOG_AREAL_DENSITIES_NOT_EXTENSIVE')
        for v,u in zip(self.values,self.uncertainty):
            need(v is None or (type(v) in (float,int) and math.isfinite(v)),'NONFINITE')
            need(u is None or (math.isfinite(u) and u>=0),'UNCERTAINTY')
        if self.kind=='OBSERVED_STATE':
            need(self.source_id.startswith('FROZEN_PUBLIC_') and self.evidence_level in ('OBSERVATION_DERIVED_HISTORICAL_ASSOCIATION','OPEN_DATA_RECALCULATED'),'SYNTHETIC_AS_OBSERVATION')
        if self.source_id.startswith('SYNTHETIC'):need(self.kind in ('SIMULATED_STATE','HYPOTHESIS_SCENARIO'),'SYNTHETIC_AS_OBSERVATION')
        if self.covariance is not None:
            covariance_check(self.covariance,n)
            for i,u in enumerate(self.uncertainty):
                need(u is None or abs(u*u-self.covariance[i][i])<=1e-9,'COVARIANCE_DIAGONAL')
        return self
    def metadata(self):
        c=CATALOG[self.id];return dict(asdict(self),identity=f'{self.id}@{self.grid.id}@{self.time.start}/{self.time.end}',dimensions=c[1],standard_name=c[2],medium=c[3],temporal_kind=c[4],semantic_name='climateos:'+self.id if c[2] is None else c[2])

def covariance_check(c,n):
    need(len(c)==n and all(len(row)==n for row in c),'COVARIANCE_SHAPE')
    l=[[0.]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):need(math.isfinite(c[i][j]) and abs(c[i][j]-c[j][i])<1e-9,'COVARIANCE_SYMMETRY')
        for j in range(i+1):
            v=c[i][j]-sum(l[i][k]*l[j][k] for k in range(j))
            if i==j:need(v>=-1e-10,'COVARIANCE_NOT_PSD');l[i][j]=math.sqrt(max(0,v))
            elif l[j][j]>1e-12:l[i][j]=v/l[j][j]
            else:need(abs(v)<1e-10,'COVARIANCE_NOT_PSD')

class State:
    def __init__(self,fields=()):
        self.fields={};self.revision=0
        for f in fields:self.put(f)
    def put(self,f):
        f.validate();old=self.fields.get(f.id)
        if old and old.kind=='OBSERVED_STATE':need(f==old,'OBSERVATION_IMMUTABLE')
        self.fields[f.id]=f;self.revision+=1
    def checkpoint(self):return (self.revision,self.fields.copy())
    def reset(self,cp):self.revision,self.fields=cp[0],cp[1].copy()
    def inspect(self):return {'revision':self.revision,'fields':{k:f.metadata() for k,f in sorted(self.fields.items())}}
    def hash(self):return digest(self.inspect())
    def require(self,ids,grid=None,time=None):
        for name in ids:
            need(name in self.fields,'MISSING_DEPENDENCY',name);f=self.fields[name]
            need(all(v is not None for v in f.values),'MISSING_DEPENDENCY',name)
            if grid:need(f.grid==grid,'SPATIAL_MISMATCH',name)
            if time:need(f.time==time,'TIME_MISMATCH',name)
        return {k:self.fields[k].values for k in ids}

def overlap(a,b):return max(0,min(a[1],b[1])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[2],b[2]))
def conservative_weights(source,target,extensive=False):
    source.validate();target.validate()
    need(source.support==target.support=='area','POINT_AREA_UNSUPPORTED')
    need(source.crs==target.crs,'CRS_MISMATCH')
    weights=[]
    for t,area in zip(target.cells,target.areas):
        ov=[overlap(t,s) for s in source.cells];need(abs(sum(ov)-area)<1e-8*area,'UNMAPPED_AREA')
        weights.append([v/(source.areas[i] if extensive else area) for i,v in enumerate(ov)])
    # Also require destination covers source, so total conservation is meaningful.
    for s,area in zip(source.cells,source.areas):need(abs(sum(overlap(s,t) for t in target.cells)-area)<1e-8*area,'TRUNCATED_DOMAIN')
    return weights
def remap(f,target):
    f.validate()
    w=conservative_weights(f.grid,target,f.extensive);values=[]
    for row in w:values.append(None if any(v is None and weight>0 for v,weight in zip(f.values,row)) else sum((v or 0)*weight for v,weight in zip(f.values,row)))
    cov=f.covariance
    if cov is None and all(u is not None for u in f.uncertainty):cov=tuple(tuple(f.uncertainty[i]**2 if i==j else 0. for j in range(len(f.values))) for i in range(len(f.values)))
    outcov=None if cov is None else tuple(tuple(sum(a[i]*cov[i][j]*b[j] for i in range(len(a)) for j in range(len(b))) for b in w) for a in w)
    u=tuple(None for _ in w) if outcov is None else tuple(math.sqrt(max(0,outcov[i][i])) for i in range(len(w)))
    return replace(f,values=tuple(values),grid=target,uncertainty=u,covariance=outcov,kind='CONSTRAINED_ESTIMATE' if f.kind=='OBSERVED_STATE' else f.kind,lineage=f.lineage+('area_overlap: covariance supplied or diagonal independence assumption',)).validate()
def accumulate(fields,target_time):
    """Sum complete adjacent accumulated intervals. Never disaggregate months."""
    need(bool(fields),'MISSING_DEPENDENCY');first=fields[0];n=len(first.values)
    need(CATALOG[first.id][4]=='accumulated','NOT_ACCUMULATED')
    need(fields[0].time.start==target_time.start and fields[-1].time.end==target_time.end,'TIME_COVERAGE')
    for a,b in zip(fields,fields[1:]):need(a.time.end==b.time.start,'TIME_GAP_OR_OVERLAP')
    for f in fields:need(f.id==first.id and f.grid==first.grid and f.unit==first.unit and f.kind==first.kind,'AGGREGATION_SUPPORT')
    values=tuple(None if any(f.values[i] is None for f in fields) else sum(f.values[i] for f in fields) for i in range(n))
    return replace(first,values=values,time=target_time,uncertainty=(None,)*n,covariance=None,lineage=first.lineage+('time_sum: temporal covariance UNKNOWN; no zero fill',)).validate()
def difference(before,after):
    need(before.fields.keys()==after.fields.keys(),'DIFFERENCE_FIELD_SET')
    out={}
    for key in before.fields.keys()&after.fields.keys():
        a,b=before.fields[key],after.fields[key];need(a.grid==b.grid and a.time==b.time and a.unit==b.unit,'DIFFERENCE_SUPPORT')
        out[key]={'delta':tuple(None if x is None or y is None else y-x for x,y in zip(a.values,b.values)),'unit':a.unit,'before':a.metadata(),'after':b.metadata()}
    return {'reference_hash':before.hash(),'scenario_hash':after.hash(),'reference_revision':before.revision,'scenario_revision':after.revision,'fields':out}

def field_from_metadata(raw):
    from dataclasses import fields
    d={f.name:raw[f.name] for f in fields(Field)}
    d['grid']=Grid(**dict(d['grid'],cells=tuple(tuple(c) for c in d['grid']['cells'])))
    d['time']=TimeSupport(**d['time'])
    for k in ('values','uncertainty','lineage'):d[k]=tuple(d[k])
    if d['covariance'] is not None:d['covariance']=tuple(tuple(r) for r in d['covariance'])
    return Field(**d).validate()

def apply_difference(state,patch,reverse=False):
    """Immutable, hash-guarded reconstruction; observations cannot be overwritten."""
    origin='scenario' if reverse else 'reference';target='reference' if reverse else 'scenario'
    need(state.hash()==patch[origin+'_hash'],'DIFFERENCE_BASE_HASH')
    out=State(state.fields.values())
    for name,item in patch['fields'].items():out.put(field_from_metadata(item['before' if reverse else 'after']))
    out.revision=patch[target+'_revision'];need(out.hash()==patch[target+'_hash'],'DIFFERENCE_TARGET_HASH')
    return out
def transform_point(x,y,source,target):
    """Only EPSG4326 <-> EPSG3857 points. Never use Mercator for area conservation."""
    need(all(math.isfinite(v) for v in (x,y)),'COORDINATE');R=6378137.
    if (source,target)==('EPSG:4326','EPSG:3857'):
        need(abs(x)<=180 and abs(y)<=85.05112878,'CRS_DOMAIN');return R*math.radians(x),R*math.log(math.tan(math.pi/4+math.radians(y)/2))
    if (source,target)==('EPSG:3857','EPSG:4326'):return math.degrees(x/R),math.degrees(2*math.atan(math.exp(y/R))-math.pi/2)
    raise Rejection('CRS_TRANSFORM_UNSUPPORTED')
