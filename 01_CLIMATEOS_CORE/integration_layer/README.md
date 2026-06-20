# ClimateOS x EcoEngine Integration Framework V1

## Purpose

The Integration Layer defines how ClimateOS interacts with EcoEngine.

ClimateOS and EcoEngine are separate systems.

ClimateOS provides governance runtime capabilities.
EcoEngine provides scientific computation capabilities.

The systems are complementary. ClimateOS does not replace EcoEngine, and
EcoEngine does not replace ClimateOS.

## Strategic Flow

```text
ClimateOS
-> Call
-> EcoEngine
-> Return Results
-> Evidence
-> Validation
-> Governance
```

## Documents

- [ClimateOS EcoEngine Framework](CLIMATEOS_ECOENGINE_FRAMEWORK.md)
- [System Responsibilities](SYSTEM_RESPONSIBILITIES.md)
- [Input Output Model](INPUT_OUTPUT_MODEL.md)
- [Computation Request Types](COMPUTATION_REQUEST_TYPES.md)
- [Computation Response Types](COMPUTATION_RESPONSE_TYPES.md)
- [Evidence Integration](EVIDENCE_INTEGRATION.md)
- [Validation Integration](VALIDATION_INTEGRATION.md)
- [CCZPS Alignment](CCZPS_ALIGNMENT.md)
- [ESG++ Alignment](ESGPP_ALIGNMENT.md)
- [Future Engine Support](FUTURE_ENGINE_SUPPORT.md)
- [Integration System Map](INTEGRATION_SYSTEM_MAP.md)
- [Engine Interface Concept](ENGINE_INTERFACE_CONCEPT.md)
- [ClimateOS Runtime Vision](CLIMATEOS_RUNTIME_VISION.md)

## Current Status

`Foundation Established`

This is documentation only. No runtime implementation, APIs, simulations,
formulas, engine calls, or EcoEngine modifications are implemented.
