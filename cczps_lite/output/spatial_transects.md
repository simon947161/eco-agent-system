# Spatial Context & Transect Runtime

Schema version: 1.0

Configured spatial relationship evidence only. No automatic point selection, GIS calls, DEM calls, mapping calls, weather calls, simulations, forecasts, hydrology inference, wind inference, design advice, or construction advice.

## Supported Roles

core, upstream, downstream, upwind, downwind, highland, lowland, lateral

## Future Compatibility

Google Earth, DEM, watershed analysis, wind corridor data, ENVI-met, Fluent, other spatial computation tools

## Transect Readings

### Batlow

- Transect ID: batlow_transect_scenario_pack
- Scenario ID: batlow
- Core location: Batlow core location
- Validation status: valid_configured
- Configured roles: highland, lateral, lowland
- Missing-data points: none
- Relationship inference: not_performed

### Kunlun

- Transect ID: kunlun_transect_scenario_pack
- Scenario ID: kunlun
- Core location: Kunlun core location
- Validation status: configured_with_missing_data
- Configured roles: highland, lowland, upwind
- Missing-data points: kunlun_upwind_reference
- Relationship inference: not_performed

### Iraq

- Transect ID: iraq_transect_scenario_pack
- Scenario ID: iraq
- Core location: Iraq environmental recovery core location
- Validation status: valid_configured
- Configured roles: downstream, lateral, upstream
- Missing-data points: none
- Relationship inference: not_performed

### Baiyangdian-Xiong'an

- Transect ID: baiyangdian_xiongan_transect_scenario_pack
- Scenario ID: baiyangdian_xiongan
- Core location: Baiyangdian-Xiong'an core location
- Validation status: valid_configured
- Configured roles: downstream, downwind, lateral, upstream
- Missing-data points: none
- Relationship inference: not_performed
