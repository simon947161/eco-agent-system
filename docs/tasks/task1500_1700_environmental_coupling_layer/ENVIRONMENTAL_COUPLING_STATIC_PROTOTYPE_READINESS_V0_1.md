# Environmental Coupling Static Prototype Readiness v0.1

Date: 2026-07-16

Status: INTERFACE_READY / SYNTHETIC_ONLY / NOT_DECISION_READY

Task: ClimateOS Task1661–1670

## 1. Graph contract

The graph uses five kinds of governed objects:

1. a graph header that fixes purpose and synthetic classification;
2. repository-authored synthetic source receipts;
3. environmental state nodes;
4. directed coupling relations;
5. non-negotiable execution boundaries.

Every object is closed to unknown fields. The dependency-free validator adds
cross-reference, governance-state and cycle checks that are not delegated to a
new runtime dependency.

## 2. Relationship taxonomy

The schema names four relationship types required by the long-range roadmap:

- `observed_association`;
- `lagged_signal`;
- `model_inference`;
- `causal_hypothesis`.

In this batch, `observed_association` is blocked because no observation was
admitted. `model_inference` is blocked because no model ran. A `lagged_signal`
may be represented only with an unestimated illustrative window. A
`causal_hypothesis` must retain `PROHIBITED_CONCLUSION` and route to a named
Task1701+ mechanism-test candidate.

## 3. Static Australian chain

The repository fixture represents this invented interface chain:

```text
hypothetical ENSO / IOD / SAM background
→ hypothetical south-eastern rainfall and heat regime
→ hypothetical Snowy Valleys / Riverina soil-moisture and water stress
→ hypothetical vegetation, fire, agriculture or biodiversity response
→ human-reviewed governance question
```

The place names provide an architectural translation context. They do not mean
that any present condition, forecast, impact or recommendation was assessed.

## 4. Uncertainty and stationarity

Every relation must state how uncertainty remains unresolved and must contain a
stationarity warning. Historical climate–environment relationships may change
under climate change, land management, ecological change and adaptation.

The prototype forbids numeric confidence and does not treat a graph path as
evidence that uncertainty decreases.

## 5. Mechanism routing

Three causal hypotheses produce only future routing identifiers:

- `TASK1701-CANDIDATE-001` — regional weather to water/land state;
- `TASK1701-CANDIDATE-002` — water/land to life-system response;
- `TASK1701-CANDIDATE-003` — life-system state to governance relevance.

These identifiers reserve review questions. They authorize no experiment,
model, data, compute or scientific claim.

## 6. Readiness decision

`STATIC_COUPLING_INTERFACE_READY / OBSERVED_AND_MODEL_RELATIONS_BLOCKED / CAUSAL_HYPOTHESES_ROUTED_NOT_PROVEN / NOT_READY_FOR_DECISION`
