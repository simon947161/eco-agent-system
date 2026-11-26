#!/usr/bin/env python3
"""Minimal synthetic 1-D transient thermo-hydraulic components for HEAT-001.

Standard-library only. This module does not read any real-site inputs.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

RHO = 1000.0
CP = 4180.0
MU = 0.001
G = 9.80665
D = 0.2
EPS = 4.5e-5
WALL_T = 0.008
WALL_RHO = 7850.0
WALL_CP = 500.0
G_FLUID_WALL = 200.0
U_GROUND = 0.26
T_GROUND = 12.0
K_MINOR = 4.0
P_REFERENCE = 300000.0
P_MIN = 120000.0
P_SAT_BOUND = 80000.0
P_SAT_MARGIN = 50000.0
CP_KW = CP / 1000.0


class InvalidModel(ValueError):
    pass


def require_finite_positive(name: str, value: float, allow_zero: bool = False) -> float:
    if not math.isfinite(value) or value < 0 or (value == 0 and not allow_zero):
        raise InvalidModel(f"{name} must be finite and {'nonnegative' if allow_zero else 'positive'}")
    return value


def hydrostatic_dp(dz_m: float, rho: float = RHO, gravity: float = G) -> float:
    if not math.isfinite(dz_m):
        raise InvalidModel("dz_m must be finite")
    return rho * gravity * dz_m


def friction_factor(reynolds: float, relative_roughness: float = EPS / D) -> float:
    require_finite_positive("Reynolds", reynolds, allow_zero=True)
    if not math.isfinite(relative_roughness) or relative_roughness < 0:
        raise InvalidModel("relative_roughness must be finite and nonnegative")
    if reynolds == 0:
        return 0.0
    if reynolds <= 2300:
        return 64.0 / reynolds
    turbulent = 0.25 / math.log10(relative_roughness / 3.7 + 5.74 / reynolds**0.9) ** 2
    if reynolds >= 4000:
        return turbulent
    laminar = 64.0 / reynolds
    w = (reynolds - 2300.0) / 1700.0
    return laminar * (1.0 - w) + turbulent * w


def darcy_pressure_drop(mass_flow_kg_s: float, length_m: float, diameter_m: float = D,
                        rho: float = RHO, mu: float = MU, roughness_m: float = EPS,
                        minor_k: float = 0.0) -> float:
    require_finite_positive("diameter_m", diameter_m)
    require_finite_positive("rho", rho)
    require_finite_positive("mu", mu)
    require_finite_positive("length_m", length_m, allow_zero=True)
    require_finite_positive("mass_flow_kg_s", abs(mass_flow_kg_s), allow_zero=True)
    if not math.isfinite(minor_k) or minor_k < 0:
        raise InvalidModel("minor_k must be finite and nonnegative")
    if mass_flow_kg_s == 0:
        return 0.0
    area = math.pi * diameter_m**2 / 4.0
    velocity = abs(mass_flow_kg_s) / (rho * area)
    reynolds = rho * velocity * diameter_m / mu
    f = friction_factor(reynolds, roughness_m / diameter_m)
    return (f * length_m / diameter_m + minor_k) * rho * velocity**2 / 2.0


def loop_pressure_profile(mass_flow_kg_s: float, lengths: list[float], elevations: list[float],
                          pump_head_pa: float, equipment_drop_pa: float = 25000.0) -> list[float]:
    """Absolute node pressures for one closed paired-pipe route, both directions."""
    if len(lengths) != len(elevations) - 1 or len(lengths) == 0:
        raise InvalidModel("length/elevation path dimensions do not match")
    if any((not math.isfinite(x) or x < 0) for x in lengths) or any(not math.isfinite(z) for z in elevations):
        raise InvalidModel("invalid route geometry")
    friction = sum(darcy_pressure_drop(mass_flow_kg_s, L) for L in lengths) * 2
    minor = darcy_pressure_drop(mass_flow_kg_s, 0, minor_k=K_MINOR) * 2
    # Split the lumped equipment drop and pump rise evenly at the circulation station.
    p = [P_REFERENCE]
    for i, (L, z0, z1) in enumerate(zip(lengths, elevations, elevations[1:])):
        seg = darcy_pressure_drop(mass_flow_kg_s, L) + equipment_drop_pa / (2 * len(lengths))
        p.append(p[-1] - hydrostatic_dp(z1-z0) - seg)
    if len(p) > 1:
        p[-1] += pump_head_pa - (friction + minor + equipment_drop_pa)
    return p


def pump_head(mass_flow_kg_s: float, design_flow_kg_s: float) -> float:
    require_finite_positive("design_flow_kg_s", design_flow_kg_s)
    if not math.isfinite(mass_flow_kg_s):
        raise InvalidModel("mass flow must be finite")
    q_shut = 3.0 * design_flow_kg_s / RHO
    q = abs(mass_flow_kg_s) / RHO
    return max(0.0, 120000.0 * (1.0 - (q / q_shut) ** 2))


def solve_mass_flow(required_kg_s: float, design_flow_kg_s: float, length_m: float,
                    elevation_gain_m: float, equipment_drop_pa: float = 25000.0) -> float:
    """Requested flow subject to the frozen pump curve; return zero if unavailable."""
    require_finite_positive("required_kg_s", required_kg_s, allow_zero=True)
    if required_kg_s == 0:
        return 0.0
    # A closed supply/return circuit has zero net static head. Elevation is retained
    # in the local absolute-pressure profile and cavitation/high-point gate below.
    if not math.isfinite(elevation_gain_m):
        raise InvalidModel("elevation_gain_m must be finite")
    static = 0.0
    def available(q: float) -> float:
        return pump_head(q, design_flow_kg_s) - equipment_drop_pa - 2 * darcy_pressure_drop(q, length_m, minor_k=K_MINOR) - static
    if available(required_kg_s) >= 0:
        return required_kg_s
    if available(0.0) <= 0:
        return 0.0
    lo, hi = 0.0, required_kg_s
    for _ in range(70):
        mid = (lo + hi) / 2
        if available(mid) >= 0:
            lo = mid
        else:
            hi = mid
    return lo


def pressure_is_safe(pressure_abs_pa: float, temperature_c: float) -> bool:
    return (math.isfinite(pressure_abs_pa) and 0 <= temperature_c <= 90
            and pressure_abs_pa >= P_MIN
            and pressure_abs_pa - P_SAT_BOUND >= P_SAT_MARGIN)


def backup_service_kw(demand_kw: float, primary_kw: float, capacity_kw: float = 650.0) -> float:
    for name,value in (("demand_kw",demand_kw),("primary_kw",primary_kw),("capacity_kw",capacity_kw)):
        require_finite_positive(name,value,allow_zero=True)
    shortfall=max(0.0,demand_kw-primary_kw)
    if shortfall>capacity_kw+1e-12:
        raise InvalidModel("backup capacity exceeded; service invalid")
    return shortfall


@dataclass
class Pipe:
    length_m: float
    dx_m: float
    dt_s: float
    ground_c: float = T_GROUND
    diameter_m: float = D
    roughness_m: float = EPS
    u_ground_w_mk: float = U_GROUND
    conductance_w_mk: float = G_FLUID_WALL
    wall_thickness_m: float = WALL_T
    fluid_c: list[float] | None = None
    wall_c: list[float] | None = None

    def __post_init__(self) -> None:
        for name, x in (("length_m", self.length_m), ("dx_m", self.dx_m), ("dt_s", self.dt_s)):
            require_finite_positive(name, x)
        if not 0 <= self.ground_c <= 90:
            raise InvalidModel("ground temperature outside frozen domain")
        self.n = max(1, math.ceil(self.length_m / self.dx_m))
        self.dx = self.length_m / self.n
        self.area = math.pi * self.diameter_m**2 / 4
        self.mass = RHO * self.area * self.dx
        self.fluid_cap = self.mass * CP
        self.wall_mass = WALL_RHO * math.pi * self.diameter_m * self.wall_thickness_m * self.dx
        self.wall_cap = self.wall_mass * WALL_CP
        self.g_fw = self.conductance_w_mk * self.dx
        self.g_wg = self.u_ground_w_mk * self.dx
        self.uf = self.dt_s * self.g_fw / self.fluid_cap
        self.uw = self.dt_s * (self.g_fw + self.g_wg) / self.wall_cap
        if max(self.uf, self.uw) > 1:
            raise InvalidModel("explicit wall/fluid exchange unstable under frozen dt")
        if self.fluid_c is None:
            self.fluid_c = [40.0] * self.n
        if self.wall_c is None:
            self.wall_c = [40.0] * self.n
        if len(self.fluid_c) != self.n or len(self.wall_c) != self.n:
            raise InvalidModel("state vector length does not match pipe mesh")

    @property
    def max_cfl(self) -> float:
        return (self.dt_s * (self.mass_flow_abs / (RHO * self.area))) / self.dx if hasattr(self, "mass_flow_abs") else 0.0

    def step(self, inlet_c: float, mass_flow_kg_s: float) -> float:
        if not math.isfinite(inlet_c) or not 0 <= inlet_c <= 90:
            raise InvalidModel("inlet temperature outside 0-90 C")
        if not math.isfinite(mass_flow_kg_s):
            raise InvalidModel("mass flow must be finite")
        cfl = abs(mass_flow_kg_s) * self.dt_s / self.mass
        if cfl > 0.7 + 1e-12:
            raise InvalidModel(f"CFL {cfl:.6g} exceeds frozen 0.7")
        old_f = self.fluid_c
        old_w = self.wall_c
        new_f = [0.0] * self.n
        new_w = [0.0] * self.n
        if mass_flow_kg_s >= 0:
            boundary = inlet_c
            for i in range(self.n):
                adv_in = boundary if i == 0 else old_f[i-1]
                adv = cfl * (adv_in - old_f[i])
                exchange = self.uf * (old_w[i] - old_f[i])
                new_f[i] = old_f[i] + adv + exchange
                new_w[i] = old_w[i] - (self.dt_s * self.g_fw / self.wall_cap) * (old_w[i]-old_f[i]) - (self.dt_s*self.g_wg/self.wall_cap)*(old_w[i]-self.ground_c)
        else:
            boundary = inlet_c
            for i in range(self.n-1, -1, -1):
                adv_in = boundary if i == self.n-1 else old_f[i+1]
                adv = cfl * (adv_in - old_f[i])
                exchange = self.uf * (old_w[i] - old_f[i])
                new_f[i] = old_f[i] + adv + exchange
                new_w[i] = old_w[i] - (self.dt_s * self.g_fw / self.wall_cap) * (old_w[i]-old_f[i]) - (self.dt_s*self.g_wg/self.wall_cap)*(old_w[i]-self.ground_c)
        if any(not math.isfinite(t) or t < -1e-9 or t > 90+1e-9 for t in new_f+new_w):
            raise InvalidModel("non-finite or out-of-domain pipe temperature")
        self.fluid_c, self.wall_c = new_f, new_w
        return old_f[-1] if mass_flow_kg_s >= 0 else old_f[0]


def carnot_cop(source_c: float, sink_supply_c: float = 65.0, approach_k: float = 3.0,
               fraction: float = 0.49) -> float:
    if not all(map(math.isfinite, (source_c, sink_supply_c, approach_k, fraction))):
        raise InvalidModel("non-finite heat pump parameter")
    tc = source_c + 273.15
    th = sink_supply_c + approach_k + 273.15
    if tc <= 0 or th <= tc or not 0 < fraction <= 1:
        raise InvalidModel("invalid heat pump temperature lift/fraction")
    cop = fraction * th / (th - tc)
    if not 1 < cop <= th/(th-tc):
        raise InvalidModel("COP outside 1<COP<=Carnot")
    return cop


def tank_step(stock_kwh: float, charge_kw: float, discharge_kw: float, dt_s: float,
              capacity_kwh: float = 320.0, max_rate_kw: float = 90.0,
              loss_fraction_h: float = 0.0018) -> tuple[float, float]:
    if any(not math.isfinite(x) for x in (stock_kwh, charge_kw, discharge_kw, dt_s)):
        raise InvalidModel("non-finite tank state/input")
    if stock_kwh < 0 or stock_kwh > capacity_kwh or charge_kw < 0 or discharge_kw < 0 or charge_kw*discharge_kw > 0:
        raise InvalidModel("invalid tank stock or simultaneous charge/discharge")
    if max(charge_kw, discharge_kw) > max_rate_kw + 1e-12:
        raise InvalidModel("tank rate exceeded")
    dt_h = dt_s / 3600
    loss = min(stock_kwh, stock_kwh * loss_fraction_h * dt_h)
    delta = (charge_kw-discharge_kw)*dt_h - loss
    new = stock_kwh + delta
    if new < -1e-12 or new > capacity_kwh+1e-12:
        raise InvalidModel(f"tank stock outside frozen bounds: start={stock_kwh}, charge={charge_kw}, discharge={discharge_kw}, dt_s={dt_s}, loss={loss}, end={new}, capacity={capacity_kwh}")
    return min(capacity_kwh, max(0.0, new)), loss
