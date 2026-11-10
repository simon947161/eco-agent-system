"""Uniform public step(dt) adapter around the four bounded model kernels.

Local kernels return proposals. Only the coupler commits them after closure
checks; a kernel cannot independently advance shared stocks during iteration.
"""
from .state import need,State
from .models import Atmosphere,Surface,ENSOContext,MethaneERF,default_config,initial_state,context_state

class ModelPort:
    def __init__(self,kernel):self.kernel=kernel;self.exchange=None
    def initialize(self,state,config=None):
        self.state=state;self.config=config or default_config();self.kernel.initialize(state);return self
    @property
    def required_fields(self):return self.kernel.required_fields
    @property
    def provided_fields(self):return self.kernel.provided_fields
    @property
    def units(self):return self.kernel.units
    @property
    def grid(self):return self.kernel.grid
    @property
    def current_time(self):return self.kernel.current_time
    def evidence(self):return self.kernel.evidence()
    def inspect(self):return dict(self.kernel.inspect(),interface='ModelPort.initialize/state; step(dt); proposals committed by coupler')
    def checkpoint(self):return self.state.checkpoint(),self.kernel.checkpoint()
    def reset(self,checkpoint):self.state.reset(checkpoint[0]);self.kernel.reset(checkpoint[1])
    def step(self,dt):
        cp=self.checkpoint()
        try:
            if isinstance(self.kernel,(Atmosphere,Surface)):
                need(dt==self.config['dt_s'],'LOCAL_CLOCK_MISMATCH')
                self.state.require(self.required_fields,grid=self.grid,time=self.state.fields['ts'].time)
                need(self.exchange is not None,'EXCHANGE_REQUIRED')
                values={k:list(f.values) for k,f in self.state.fields.items()}
                result=self.kernel.step(values,self.exchange,self.config,dt)
                self.kernel.current_time+=dt
                return {'proposal':result,'committed':False,'clock':self.current_time}
            return self.kernel.step(self.state,dt)
        except Exception:
            self.reset(cp);raise

def demonstrate():
    config=default_config();state=initial_state(config);values={k:list(f.values) for k,f in state.fields.items()}
    flux=Atmosphere().fluxes(values,config,values,config['dt_s']);out={}
    for cls in (Atmosphere,Surface,ENSOContext,MethaneERF):
        port=ModelPort(cls()).initialize(State(state.fields.values()),config);port.exchange=flux
        dt=config['dt_s'] if cls in (Atmosphere,Surface) else state.fields[port.required_fields[0]].time.seconds()
        out[port.kernel.name]={'output':port.step(dt),'interface':port.inspect(),'grid':port.grid.id,'checkpoint_reset_available':True}
    return out
