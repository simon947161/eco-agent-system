#!/usr/bin/env python3
"""Offline SYNTHETIC L2 runner. Reads only the byte-pinned P1 hourly fixture."""
from __future__ import annotations
import csv, gzip, hashlib, json, math, pathlib, sys, time
from l2_model import Pipe, InvalidModel, CP, RHO, P_REFERENCE, U_GROUND, backup_service_kw, carnot_cop, solve_mass_flow, darcy_pressure_drop, pressure_is_safe, tank_step, hydrostatic_dp

ROOT = pathlib.Path(__file__).resolve().parent
FIXTURE = ROOT / "fixtures" / "paired_hours.csv.gz"
CONTRACT = ROOT / "L2_FROZEN_SYNTHETIC_CONTRACT.json"
OUT = ROOT / "outputs"
P1 = json.loads(CONTRACT.read_text(encoding="utf-8"))["p1_parameters"]
P1 = {k:v["value"] for k,v in P1.items()}


def read_fixture():
    raw = FIXTURE.read_bytes()
    expected = "b47919eef8b20db388c83aacfa18266819c4d3581076adb4665bed28cc29f94d"
    if hashlib.sha256(raw).hexdigest() != expected:
        raise InvalidModel("P1 fixture SHA mismatch")
    with gzip.open(FIXTURE, "rt", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 8760 or any(r.get("origin") != "SYNTHETIC" for r in rows):
        raise InvalidModel("P1 fixture row count or SYNTHETIC tag invalid")
    return rows


def new_pipe(length, dx, dt):
    return Pipe(float(length),float(dx),float(dt))


def max_state_delta(a,b):
    return max(abs(x-y) for p,q in zip(a,b) for arr1,arr2 in ((p.fluid_c,q.fluid_c),(p.wall_c,q.wall_c)) for x,y in zip(arr1,arr2))


def annual_cycle(layout, dt_s=60, dx_m=25, rows=None, max_cycles=8):
    """Repeat identical synthetic year until pipe thermal state is periodic."""
    if rows is None: rows=read_fixture()
    geom = {"L": (80,40,(0,2,3)),"T": (120,180,(0,6,3))}[layout]
    lac,lcb,elev=geom
    pipes=[new_pipe(lac,dx_m,dt_s),new_pipe(lac,dx_m,dt_s),new_pipe(lcb,dx_m,dt_s),new_pipe(lcb,dx_m,dt_s)]
    tank=0.0
    steps_per_hour=int(3600/dt_s)
    if steps_per_hour*dt_s != 3600: raise InvalidModel("internal dt must divide one hour")
    last_outputs=None; cycle_count=0; periodic_error=float("inf")
    elapsed_start=time.perf_counter()
    for cycle in range(1,max_cycles+1):
        start=[Pipe(p.length_m,p.dx_m,p.dt_s,fluid_c=list(p.fluid_c),wall_c=list(p.wall_c)) for p in pipes]
        start_pipe_energy=sum(sum(p.mass*CP*t + p.wall_cap*w for t,w in zip(p.fluid_c,p.wall_c)) for p in pipes[2:])/3.6e6
        annual={k:0.0 for k in ("demand_kwh","qualified_network_kwh","network_delivery_kwh","backup_kwh","hp_heat_kwh","hp_electricity_kwh","pump_electricity_kwh","source_extraction_kwh","pipe_ground_loss_kwh","tank_charge_kwh","tank_discharge_kwh","tank_loss_kwh","terminal_dump_kwh","service_shortfall_kwh")}
        hourly=[]; hour_acc={k:0.0 for k in ("demand_kwh","qualified_network_kwh","network_delivery_kwh","backup_kwh","hp_heat_kwh","hp_electricity_kwh","pump_electricity_kwh","source_extraction_kwh","pipe_ground_loss_kwh","tank_charge_kwh","tank_discharge_kwh","tank_loss_kwh","terminal_dump_kwh","min_pressure_pa","max_supply_c")}
        for hi,row in enumerate(rows):
            demand_kw=float(row["space_kw"])+float(row["dhw_kw"])
            if not math.isfinite(demand_kw) or demand_kw<0: raise InvalidModel("invalid demand input")
            for sub in range(steps_per_hour):
                # At C, low-loop return outlet supplies the heat pump source. Use the dynamic
                # source outlet from the supply pipe and frozen Carnot-fraction COP.
                ac_out=pipes[0].fluid_c[-1]
                try: cop=carnot_cop(ac_out,65.0,3.0,P1["carnot_fraction"])
                except InvalidModel: cop=0.0
                hp_cap=min(200.0,150.0*cop/(cop-1.0)) if cop>1 else 0.0
                # High loop follows the P1 65/40 C demand design; dynamically transported return
                # enthalpy sets the HP sink requirement. This closes HP-to-loop heat explicitly.
                last_day=hi>=8736
                available_tank=max(0.0,tank*(1.0-0.0018*dt_s/3600.0))
                m_high_req=(demand_kw+(90.0 if tank<320.0 and not last_day else 0.0))*1000/(CP*25.0) if demand_kw>0 else 0.0
                m_high=solve_mass_flow(m_high_req,2.77511961722488,lcb,elev[2]-elev[1])
                high_ratio=m_high/m_high_req if m_high_req>0 else 0.0
                high_dp=25000.0+2*darcy_pressure_drop(m_high,lcb,minor_k=4.0)
                high_head=min(120000.0,high_dp)
                high_pump=(m_high/RHO)*high_head/0.65/1000
                return_at_c=pipes[3].fluid_c[-1]
                heat_needed=m_high*CP/1000*max(0.0,65.0-return_at_c)
                # P1 optional tank is a single C-side inventory. HP first follows demand;
                # pre-existing stock can bridge a cap deficit. No free initial heat is allowed.
                hp_heat_target=min(hp_cap,heat_needed)
                q_source_target=hp_heat_target*(1.0-1.0/cop) if cop>1 else 0.0
                m_low_req=q_source_target*1000/(CP*5.0) if q_source_target>0 else 0.0
                m_low=solve_mass_flow(m_low_req,7.177033492822966,lac,0.0)
                low_ratio=m_low/m_low_req if m_low_req>0 else 0.0
                hp_heat=hp_heat_target*low_ratio
                q_source=hp_heat*(1.0-1.0/cop) if cop>1 else 0.0
                hp_elec=hp_heat/cop if cop>1 else 0.0
                low_dp=25000.0+2*darcy_pressure_drop(m_low,lac,minor_k=4.0)
                low_head=min(120000.0,low_dp)
                low_pump=(m_low/RHO)*low_head/0.65/1000
                supply_out=pipes[2].fluid_c[-1]
                available_network=m_high*CP/1000*max(0.0,supply_out-40.0) if supply_out>=63.0 else 0.0
                qualified=min(demand_kw,available_network*min(1.0,high_ratio))
                tank_discharge=min(90.0,max(0.0,demand_kw-qualified),available_tank*3600/dt_s)
                tank_charge=min(90.0,max(0.0,320.0-tank)*3600/dt_s,max(0.0,available_network-qualified)) if not last_day and tank_discharge<=1e-12 else 0.0
                tank, tank_loss=tank_step(tank,tank_charge,tank_discharge,dt_s)
                terminal_dump=0.0
                if hi==8759 and sub==steps_per_hour-1:
                    terminal_dump=tank
                    tank=0.0
                network_delivery=qualified+tank_charge
                qualified=min(demand_kw,qualified*min(1.0,high_ratio))
                primary_service=min(demand_kw,qualified+tank_discharge)
                backup=backup_service_kw(demand_kw,primary_service,650.0)
                # Dynamic source-side return and fixed high-side return close the two water loops.
                low_return=max(0.0,ac_out-(q_source*1000/max(m_low*CP,1e-30))) if m_low>0 else ac_out
                heat_to_network=hp_heat
                supply_at_c=(return_at_c+heat_to_network*1000/(m_high*CP)) if m_high>0 else 40.0
                return_at_b=(supply_out-network_delivery*1000/(m_high*CP)) if m_high>0 and supply_out>=63.0 else supply_out
                dtdt=dt_s/3600.0
                ground_kw=sum(p.u_ground_w_mk*p.dx*sum(t-12.0 for t in p.wall_c) for p in pipes[2:])
                pipes[0].step(40.0,m_low)
                pipes[1].step(low_return,m_low)
                pipes[2].step(supply_at_c,m_high)
                pipes[3].step(return_at_b,m_high)
                # Path absolute pressure uses the maximum node elevation, including the frozen
                # piecewise linear route; net closed-loop static head is zero.
                p_high=P_REFERENCE-hydrostatic_dp(max(elev)-elev[0])-high_dp/2
                p_low=P_REFERENCE-hydrostatic_dp(max(elev[:2])-elev[0])-low_dp/2
                if not pressure_is_safe(p_high,max(40.0,supply_out)) or not pressure_is_safe(p_low,ac_out):
                    raise InvalidModel("absolute-pressure / saturation-margin gate failed")
                values={"demand_kwh":demand_kw*dtdt,"qualified_network_kwh":qualified*dtdt,"backup_kwh":backup*dtdt,
                        "hp_heat_kwh":hp_heat*dtdt,"hp_electricity_kwh":hp_elec*dtdt,"pump_electricity_kwh":(low_pump+high_pump)*dtdt,
                        "source_extraction_kwh":q_source*dtdt,"network_delivery_kwh":network_delivery*dtdt,
                        "pipe_ground_loss_kwh":ground_kw*dtdt/1000,"tank_charge_kwh":tank_charge*dtdt,
                        "tank_discharge_kwh":tank_discharge*dtdt,"tank_loss_kwh":tank_loss,"terminal_dump_kwh":terminal_dump}
                for k,v in values.items():
                    annual[k]+=v
                    if k in hour_acc: hour_acc[k]+=v
                hour_acc["min_pressure_pa"]=min(hour_acc["min_pressure_pa"] or float("inf"),p_high,p_low)
                hour_acc["max_supply_c"]=max(hour_acc["max_supply_c"],supply_out)
            hourly.append({"tag":"SYNTHETIC","layout":layout,"hour":hi,**hour_acc,"tank_end_kwh":tank})
            hour_acc={k:0.0 for k in hour_acc}
        periodic_error=max_state_delta(pipes,start)
        end_pipe_energy=sum(sum(p.mass*CP*t + p.wall_cap*w for t,w in zip(p.fluid_c,p.wall_c)) for p in pipes[2:])/3.6e6
        annual["pipe_energy_storage_delta_kwh"]=end_pipe_energy-start_pipe_energy
        annual["network_energy_residual_kwh"]=(annual["hp_heat_kwh"]-annual["network_delivery_kwh"]-annual["pipe_ground_loss_kwh"]-annual["pipe_energy_storage_delta_kwh"])
        annual["tank_energy_residual_kwh"]=annual["tank_charge_kwh"]-annual["tank_discharge_kwh"]-annual["tank_loss_kwh"]-annual["terminal_dump_kwh"]
        cycle_count=cycle
        last_outputs=(annual,hourly,tank)
        if periodic_error<=0.01:
            break
    if periodic_error>0.01:
        raise InvalidModel(f"periodic pipe/wall state not reached in {max_cycles} cycles: {periodic_error:.6g} K")
    if abs(tank)>1e-7:
        raise InvalidModel(f"terminal tank stock mismatch: {tank:.9g} kWh")
    elapsed=time.perf_counter()-elapsed_start
    annual,hourly,tank=last_outputs
    annual["periodic_error_K"]=periodic_error
    annual["warmup_cycles"]=cycle_count
    annual["runtime_s"]=elapsed
    annual["fuel_kwh_LHV"]=annual["backup_kwh"]/P1["boiler_eff"]
    annual["service_kwh"]=annual["demand_kwh"]
    annual["electricity_kwh"]=annual["hp_electricity_kwh"]+annual["pump_electricity_kwh"]
    annual["primary_kwh"]=annual["electricity_kwh"]*P1["grid_pe"]+annual["fuel_kwh_LHV"]*P1["fuel_pe"]
    annual["operation_kgco2e"]=annual["electricity_kwh"]*P1["grid_ef"]+annual["fuel_kwh_LHV"]*P1["fuel_ef"]
    length=lac+lcb
    capex=P1["boiler_capex"]+P1["network_hp_capex"]+length*P1["trench_capex"]+P1["tank_kwh"]*P1["tank_capex"]
    annual_power=annual["electricity_kwh"]*P1["electricity_price"]
    annual_fuel=annual["fuel_kwh_LHV"]*P1["fuel_price"]
    pv_years=sum((1+P1["rate"])**-y for y in range(1,int(P1["life"])+1))
    pv=capex+pv_years*(capex*P1["fixed_om"]+annual_power+annual_fuel)
    annual["lcoh_aud_per_mwh"]=pv/(pv_years*annual["service_kwh"]/1000)
    if abs(annual["network_energy_residual_kwh"])>1e-5:
        raise InvalidModel("annual network energy residual " + json.dumps({k:annual.get(k) for k in ("network_energy_residual_kwh","hp_heat_kwh","network_delivery_kwh","pipe_ground_loss_kwh","pipe_energy_storage_delta_kwh","tank_loss_kwh","warmup_cycles","periodic_error_K")},sort_keys=True))
    if abs(annual["tank_energy_residual_kwh"])>1e-5:
        raise InvalidModel(f"tank annual energy residual {annual['tank_energy_residual_kwh']:.9g} kWh exceeds frozen 1e-5 kWh")
    return annual,hourly


def U_GROUND_TOTAL(lac,lcb): return 2*U_GROUND*(lac+lcb)


def write_case(layout,dt,dx,annual,hourly):
    OUT.mkdir(exist_ok=True)
    stem=f"L2_V3_{layout}_dt{dt}_dx{dx}"
    with (OUT/(stem+"_hourly.csv")).open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(hourly[0])); w.writeheader(); w.writerows(hourly)
    (OUT/(stem+"_annual.json")).write_text(json.dumps({"tag":"SYNTHETIC","layout":layout,"dt_s":dt,"dx_m":dx,**annual},indent=2)+"\n",encoding="utf-8")


if __name__=="__main__":
    layout=sys.argv[1] if len(sys.argv)>1 else "L"
    dt=int(sys.argv[2]) if len(sys.argv)>2 else 60
    dx=float(sys.argv[3]) if len(sys.argv)>3 else 25
    a,h=annual_cycle(layout,dt,dx)
    if "--no-write" not in sys.argv[4:]: write_case(layout,dt,dx,a,h)
    print(json.dumps({"tag":"SYNTHETIC","layout":layout,"dt_s":dt,"dx_m":dx,"annual":a},sort_keys=True))
