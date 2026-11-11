"""Atomic PR152 feedback through actual ModelPorts, reusing its iteration/ledger."""
from ..earth_system_coupling import models as m
from ..earth_system_coupling.ports import ModelPort
from ..earth_system_coupling.state import need

class CoupledPorts:
    def __init__(self, state, config):
        self.state, self.config = state, config
        self.air = ModelPort(m.Atmosphere()).initialize(state, config)
        self.land = ModelPort(m.Surface()).initialize(state, config)
        self.calls = 0
        self.last_exchange = None

    def step(self, lag=None):
        cp = self.state.checkpoint()
        clocks = (self.air.kernel.checkpoint(), self.land.kernel.checkpoint())
        self.last_exchange = None
        def proposals(old, guess, config, strategy, lag_values):
            need(strategy == 'two_way', 'ATOMIC_TWO_WAY_ONLY')
            flux = self.air.kernel.fluxes(guess, config, old, config['dt_s'], lag_values)
            self.last_exchange = flux
            # Iterations recompute proposals from the same old inventory/clock.
            outputs = []
            for port, clock in zip((self.land, self.air), reversed(clocks)):
                port.kernel.reset(clock)
                port.exchange = flux
                self.calls += 1
                out = port.step(config['dt_s'])
                need(out['committed'] is False, 'PREMATURE_COMMIT')
                outputs.append(out['proposal'])
            surface, air = outputs
            return {**{k:surface[k] for k in ('ts','water')},
                    **{k:air[k] for k in ('ta','q')}}, flux, surface, air
        try:
            info = m.advance(self.state, self.config, 'two_way', lag, mapper=proposals)
            E = self.last_exchange['evap']; H = self.last_exchange['sensible']
            info['exchange_ledger'] = {
                'surface_water_out_kg_m2': [v*self.config['dt_s'] for v in E],
                'air_water_in_kg_m2': [v*self.config['dt_s'] for v in E],
                'surface_sensible_out_j_m2': [v*self.config['dt_s'] for v in H],
                'air_sensible_in_j_m2': [v*self.config['dt_s'] for v in H],
                'surface_latent_out_j_m2': [v*m.LV*self.config['dt_s'] for v in E],
                'air_latent_in_j_m2': [v*m.LV*self.config['dt_s'] for v in E]}
            info['port_clocks_s'] = [self.air.current_time, self.land.current_time]
            return info
        except Exception:
            self.state.reset(cp)
            self.air.kernel.reset(clocks[0]); self.land.kernel.reset(clocks[1])
            self.last_exchange = None
            raise
