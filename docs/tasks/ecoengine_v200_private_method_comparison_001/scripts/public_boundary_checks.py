"""Two public input-contract checks. No trajectory or private code execution."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from cczps_lite.integration.earth_system_coupling import models,state

def run():
    frozen=json.loads((ROOT/'docs/tasks/climateos_earth_system_coupling_lab_001/EXPERIMENT_RESULTS.json').read_text(encoding='utf-8'))
    hashes={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
            for p in [ROOT/'cczps_lite/integration/earth_system_coupling/state.py',ROOT/'cczps_lite/integration/earth_system_coupling/models.py']}
    assert all(frozen['source_hashes'][name]==h for name,h in hashes.items()),'FROZEN_SOURCE_CHANGED'
    rows=[]
    for label,call,code in [
        ('nonfinite_coordinate',lambda:state.transform_point(float('nan'),0.,'EPSG:4326','EPSG:3857'),'COORDINATE'),
        ('nonfinite_configuration',lambda:models.validate_config(dict(models.default_config(),wind_m_s=float('nan'))),'CONFIG_NONFINITE')]:
        try:call()
        except state.Rejection as exc: actual=exc.code
        else:actual='NOT_REJECTED'
        assert actual==code,(label,actual)
        rows.append({'category':label,'status':'REJECTED','code':actual})
    return {'scope':'public input validation only; not a paired accuracy comparison','baseline_sha':'cf91e4a061341bc33d16400bcf4c6a2c2817aa65','trajectory_runs':0,'source_sha256':hashes,'rows':rows}

if __name__=='__main__':print(json.dumps(run(),indent=2))
