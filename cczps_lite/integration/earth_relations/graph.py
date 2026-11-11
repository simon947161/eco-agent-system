"""Typed contracts, bounded ancestor closure, and an indivisible feedback factor.

Admission means executable in this synthetic sandbox, never scientific approval.
Only registered operations run. Descriptive evidence cannot authorize fluxes.
"""
from dataclasses import dataclass, asdict, replace
from collections import defaultdict, deque
from types import MappingProxyType
from ..earth_system_coupling.state import Rejection, need, digest

NODE_KINDS = {'EXTERNAL_FORCING','MODEL_STATE','PHYSICAL_PROCESS',
              'STATISTICAL_CONTEXT','DIAGNOSTIC','DECISION_QUESTION','OBSERVATION'}
EDGE_KINDS = {'PHYSICAL_FLUX','DECLARED_PROCESS_DEPENDENCY',
              'STATISTICAL_ASSOCIATION','HYPOTHESIS_CANDIDATE','DIAGNOSTIC_DERIVATION'}
OPS = {'forcing','coupled','water','heat','humidity','hotdry','saturation',
       'question','lag_water','detail','context_enso','context_ch4','extra','identity'}

@dataclass(frozen=True)
class Node:
    id: str
    kind: str
    operation: str
    scope: str = 'local_area'
    clock: str = 'land_interval'
    conditional: bool = False
    evidence: str = 'SYNTHETIC_TESTED_SCIENCE_PENDING'

@dataclass(frozen=True)
class Edge:
    id: str
    source: str
    target: str
    relation: str
    source_field: str
    target_field: str
    source_unit: str
    target_unit: str
    source_scope: str = 'local_area'
    target_scope: str = 'local_area'
    clock: str = 'land_interval'
    lag_steps: int = 0
    conversion: str = 'identity'
    evidence: str = 'SYNTHETIC_TESTED_SCIENCE_PENDING'
    source_ref: str = 'PR152_FIXED_BASELINE'
    applicability: str = 'idealised slab only; no real-region prediction'
    numeric: bool = True
    enabled: bool = True
    revoked: bool = False
    required: bool = True
    ledger: str | None = None

# Every executable endpoint is checked against an operation contract. Unknown
# field names cannot be smuggled through a graph just because their units match.
OUT = {'forcing':{'drivers':'bundle','rain':'kg m-2 s-1'},
       'coupled':{'water':'kg m-2','heat':'K','humidity':'kg kg-1','state':'bundle',
                  'surface.evap':'kg m-2 s-1','surface.heat':'W m-2','air.q':'kg kg-1'},
       'water':{'water':'kg m-2'},'heat':{'heat':'K'},'humidity':{'humidity':'kg kg-1'},
       'hotdry':{'flag':'1'},'saturation':{'flag':'1'},'question':{'answer':'1'},
       'lag_water':{'water':'kg m-2'},'detail':{'detail':'1'},
       'context_enso':{'enso':'1'},'context_ch4':{'erf':'W m-2'},
       'extra':{'summary':'1'},'identity':{'value':'1'}}
IN = {'forcing':{},'coupled':{'drivers':'bundle','air.evap':'kg m-2 s-1',
                            'air.heat':'W m-2','surface.q_lag':'kg kg-1'},
      'water':{'water':'kg m-2'},'heat':{'heat':'K'},'humidity':{'humidity':'kg kg-1'},
      'hotdry':{'water':'kg m-2','heat':'K'},'saturation':{'water':'kg m-2'},
      'question':{'hotdry':'1','saturation':'1'},'lag_water':{'water':'kg m-2'},
      'detail':{'flag':'1','humidity':'kg kg-1'},'context_enso':{},'context_ch4':{},
      'extra':{'state':'bundle','rain':'kg m-2 s-1'},'identity':{'left':'1','right':'1'}}
MANDATORY = {k:set(v) for k,v in IN.items()}
MANDATORY['coupled'] = {'drivers'}
MANDATORY['identity'] = {'left'}
PHYSICAL = {'evap_exchange':('surface.evap','air.evap','kg m-2 s-1','water_and_latent'),
            'heat_exchange':('surface.heat','air.heat','W m-2','sensible')}

class Graph:
    def __init__(self, nodes, edges, max_nodes=256, max_edges=1024):
        nodes, edges = list(nodes), list(edges)
        need(len(nodes)<=max_nodes and len(edges)<=max_edges,'GRAPH_BUDGET')
        need(len({n.id for n in nodes})==len(nodes),'DUPLICATE_NODE')
        need(len({e.id for e in edges})==len(edges),'DUPLICATE_EDGE')
        self.nodes = MappingProxyType({n.id:n for n in nodes}); self.edges = MappingProxyType({e.id:e for e in edges})
        for n in nodes:
            need(n.kind in NODE_KINDS and n.operation in OPS,'NODE_CONTRACT',n.id)
            expected = ('PHYSICAL_PROCESS' if n.operation=='coupled' else 'EXTERNAL_FORCING' if n.operation=='forcing' else 'STATISTICAL_CONTEXT' if n.operation.startswith('context_') else 'MODEL_STATE' if n.operation in ('water','heat','humidity') else 'DECISION_QUESTION' if n.operation=='question' else 'DIAGNOSTIC')
            need(n.kind==expected,'NODE_KIND_OPERATION',n.id)
            expected_support = ('index_region','seasonal') if n.operation=='context_enso' else ('global','annual') if n.operation=='context_ch4' else ('local_area','land_interval')
            need((n.scope,n.clock)==expected_support,'NODE_SUPPORT_CONTRACT',n.id)
        self.incoming=defaultdict(list)
        for e in edges:
            need(e.source in self.nodes and e.target in self.nodes,'EDGE_ENDPOINT',e.id)
            self.incoming[e.target].append(e)
        self.incoming = MappingProxyType({k:tuple(self.incoming[k]) for k in self.nodes})

    def with_edge(self, edge):
        need(edge.id in self.edges,'UNKNOWN_EDGE')
        return Graph(self.nodes.values(),[edge if e.id==edge.id else e for e in self.edges.values()])

    def hash(self):return digest(self.inspect_raw())
    def inspect_raw(self):
        return {'nodes':[asdict(n) for n in self.nodes.values()],
                'edges':[asdict(e) for e in self.edges.values()]}

    def admission(self, e, lag_steps=0):
        if e.revoked:return 'REVOKED'
        if not e.enabled:return 'INACTIVE'
        if e.relation not in EDGE_KINDS:return 'UNKNOWN_RELATION'
        if not e.source_ref or not e.applicability:return 'EVIDENCE_MISSING'
        if e.relation in ('STATISTICAL_ASSOCIATION','HYPOTHESIS_CANDIDATE'):
            return 'UNSUPPORTED_NUMERIC_LINK' if e.numeric else 'CONTEXT_ONLY'
        if not e.numeric:return 'NONNUMERIC_DEPENDENCY'
        if self.nodes[e.source].kind=='STATISTICAL_CONTEXT':return 'CONTEXT_CANNOT_FORCE'
        if e.evidence!='SYNTHETIC_TESTED_SCIENCE_PENDING':return 'EVIDENCE_NOT_EXECUTABLE'
        a,b=self.nodes[e.source],self.nodes[e.target]
        if e.source_scope!=a.scope or e.target_scope!=b.scope or a.scope!=b.scope:return 'SPATIAL_MISMATCH'
        if e.clock!=a.clock or e.clock!=b.clock:return 'TIME_SUPPORT_MISMATCH'
        if e.conversion!='identity' or e.source_unit!=e.target_unit:return 'UNIT_CONVERSION_UNSUPPORTED'
        if OUT[a.operation].get(e.source_field)!=e.source_unit or IN[b.operation].get(e.target_field)!=e.target_unit:return 'FIELD_SEMANTICS'
        if type(e.lag_steps) is not int or not 0<=e.lag_steps<=4:return 'LAG_RANGE'
        if e.relation=='PHYSICAL_FLUX':
            if (e.source!=e.target or a.operation!='coupled' or e.id not in PHYSICAL):return 'UNREGISTERED_PHYSICAL_EXCHANGE'
            f,t,u,ledger=PHYSICAL[e.id]
            if (e.source_field,e.target_field,e.source_unit,e.ledger)!=(f,t,u,ledger):return 'LEDGER_CONTRACT'
            return 'ACCEPTED' if e.lag_steps==0 else 'FLUX_DELAY_UNSUPPORTED'
        if e.source==e.target:
            return 'ACCEPTED' if (a.operation=='coupled' and e.id=='humidity_feedback' and e.source_field=='air.q' and e.target_field=='surface.q_lag' and e.lag_steps==lag_steps) else 'UNREGISTERED_FEEDBACK'
        if e.lag_steps and not (b.operation=='lag_water' and e.lag_steps==1):return 'TIME_LAG_UNSUPPORTED'
        if b.operation=='lag_water' and e.lag_steps!=1:return 'TIME_LAG_UNSUPPORTED'
        return 'ACCEPTED'

    def plan(self, targets=('question',), full=False, lag_steps=0):
        need(bool(targets) and all(x in self.nodes for x in targets),'UNKNOWN_TARGET')
        admission={e.id:self.admission(e,lag_steps) for e in self.edges.values()}
        selected=set(self.nodes) if full else set(targets); stack=list(selected)
        while stack:
            for e in self.incoming[stack.pop()]:
                if admission[e.id]=='ACCEPTED' and e.source not in selected:
                    selected.add(e.source);stack.append(e.source)
        # Missing required connections fail the relevant task, not unrelated tasks.
        for node in selected:
            op=self.nodes[node].operation
            accepted=[e for e in self.incoming[node] if admission[e.id]=='ACCEPTED' and e.source!=e.target]
            slots=[e.target_field for e in accepted]
            need(len(slots)==len(set(slots)),'AMBIGUOUS_INPUT',node)
            need(MANDATORY[op]<=set(slots),'MISSING_REQUIRED_EDGE',node)
            if op=='coupled':
                for key in (*PHYSICAL,'humidity_feedback'):
                    need(key in admission and admission[key]=='ACCEPTED' and self.edges[key].source==node and self.edges[key].target==node,'PHYSICAL_CLOSURE_REQUIRED',key)
        indeg={x:0 for x in selected}; downstream=defaultdict(list)
        for e in self.edges.values():
            if admission[e.id]=='ACCEPTED' and e.source in selected and e.target in selected and e.source!=e.target:
                indeg[e.target]+=1;downstream[e.source].append(e.target)
        queue=deque(sorted(x for x,v in indeg.items() if not v));order=[]
        while queue:
            n=queue.popleft();order.append(n)
            for other in downstream[n]:
                indeg[other]-=1
                if indeg[other]==0:queue.append(other)
        need(len(order)==len(selected),'UNREGISTERED_CYCLE')
        return {'targets':list(targets),'order':order,'graph_hash':self.hash(),
                'selected_nodes':sorted(selected),'omitted_nodes':sorted(set(self.nodes)-selected),
                'edges':[{'id':e.id,'status':admission[e.id] if admission[e.id]!='ACCEPTED' else ('EXECUTE' if e.source in selected and e.target in selected else 'NOT_NEEDED')} for e in self.edges.values()],
                'science':'PENDING','mode':'full_safe' if full else 'selective'}

    def trace(self, target, lag_steps=0, cap=1000000):
        p=self.plan((target,),lag_steps=lag_steps);counts={};depth={};links=[]
        for n in p['order']:
            parents={e.source for e in self.incoming[n] if e.source!=n and self.admission(e,lag_steps)=='ACCEPTED'}
            counts[n]=min(cap,sum(counts[x] for x in parents)) if parents else 1
            depth[n]=1+max((depth[x] for x in parents),default=-1)
            links.extend(e.id for e in self.incoming[n] if self.admission(e,lag_steps)=='ACCEPTED')
        return {'target':target,'unique_nodes':p['selected_nodes'],'unique_edges':sorted(set(links)),
                'node_count':len(p['order']),'depth':depth[target],'path_count_capped':counts[target],
                'cap':cap,'paths_enumerated':False,'meaning':'dependency provenance, NOT causal attribution',
                'alternatives':[x for x in p['edges'] if x['status'] not in ('EXECUTE','NOT_NEEDED')]}


def sandbox_graph(extra=6, lag_steps=0, diamond_levels=0):
    nodes=[Node('forcing','EXTERNAL_FORCING','forcing'),Node('coupled','PHYSICAL_PROCESS','coupled'),
           Node('water','MODEL_STATE','water'),Node('heat','MODEL_STATE','heat'),Node('humidity','MODEL_STATE','humidity'),
           Node('hotdry','DIAGNOSTIC','hotdry'),Node('saturation','DIAGNOSTIC','saturation'),
           Node('question','DECISION_QUESTION','question'),Node('lag_water','DIAGNOSTIC','lag_water'),
           Node('hot_detail','DIAGNOSTIC','detail',conditional=True),
           Node('ENSO','STATISTICAL_CONTEXT','context_enso','index_region','seasonal',evidence='HISTORICAL_ASSOCIATION'),
           Node('CH4','STATISTICAL_CONTEXT','context_ch4','global','annual',evidence='OPEN_DATA_RECALCULATED')]
    edges=[]
    def edge(id,s,t,sf,tf,u,**kw):
        edges.append(Edge(id,s,t,kw.pop('relation','DECLARED_PROCESS_DEPENDENCY'),sf,tf,u,u,**kw))
    edge('drivers','forcing','coupled','drivers','drivers','bundle')
    for id,(sf,tf,u,ledger) in PHYSICAL.items():edge(id,'coupled','coupled',sf,tf,u,relation='PHYSICAL_FLUX',ledger=ledger)
    edge('humidity_feedback','coupled','coupled','air.q','surface.q_lag','kg kg-1',lag_steps=lag_steps)
    for node,u in [('water','kg m-2'),('heat','K'),('humidity','kg kg-1')]:edge('state_'+node,'coupled',node,node,node,u)
    edge('water_hot','water','hotdry','water','water','kg m-2',relation='DIAGNOSTIC_DERIVATION')
    edge('heat_hot','heat','hotdry','heat','heat','K',relation='DIAGNOSTIC_DERIVATION')
    edge('water_sat','water','saturation','water','water','kg m-2',relation='DIAGNOSTIC_DERIVATION')
    edge('hot_question','hotdry','question','flag','hotdry','1',relation='DIAGNOSTIC_DERIVATION')
    edge('sat_question','saturation','question','flag','saturation','1',relation='DIAGNOSTIC_DERIVATION')
    edge('water_delay','water','lag_water','water','water','kg m-2',lag_steps=1)
    edge('hot_detail','hotdry','hot_detail','flag','flag','1',relation='DIAGNOSTIC_DERIVATION')
    edge('humidity_detail','humidity','hot_detail','humidity','humidity','kg kg-1',relation='DIAGNOSTIC_DERIVATION')
    # These are visible rejected/context-only links, never numerical forcings.
    edge('enso_rain_claim','ENSO','forcing','enso','rain','1',relation='STATISTICAL_ASSOCIATION',source_scope='index_region',clock='seasonal',required=False)
    edge('ch4_local_claim','CH4','coupled','erf','drivers','W m-2',relation='HYPOTHESIS_CANDIDATE',source_scope='global',clock='annual',required=False)
    edge('enso_background','ENSO','question','enso','hotdry','1',relation='STATISTICAL_ASSOCIATION',source_scope='index_region',clock='seasonal',numeric=False,required=False)
    for i in range(extra):
        id=f'water_summary_{i}';nodes.append(Node(id,'DIAGNOSTIC','extra'))
        edge(id+'_state','coupled',id,'state','state','bundle',relation='DIAGNOSTIC_DERIVATION')
        edge(id+'_rain','forcing',id,'rain','rain','kg m-2 s-1',relation='DIAGNOSTIC_DERIVATION')
    prev=['question']
    for level in range(diamond_levels):
        this=[]
        for side in ('a','b'):
            id=f'diamond_{level}_{side}';nodes.append(Node(id,'DIAGNOSTIC','identity'));this.append(id)
            for index,parent in enumerate(prev):edge(f'{parent}_{id}',parent,id,'answer' if parent=='question' else 'value','left' if index==0 else 'right','1',relation='DIAGNOSTIC_DERIVATION')
        prev=this
    return Graph(nodes,edges)
