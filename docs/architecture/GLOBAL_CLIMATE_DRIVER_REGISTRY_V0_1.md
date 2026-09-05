# Global Climate Driver Registry v0.1

Status: DRAFT_FOR_FOUNDER_REVIEW  
Parent: Issue #97  
Ontology dependency: `EARTH_SYSTEM_ONTOLOGY_V0_1.md`

## 1. Registry purpose

This registry defines canonical ClimateOS entries for large-scale climate drivers. It does not assert that any listed driver produces the same outcome everywhere. Each entry is interpreted through region, season, hemisphere, lag, compound-driver context, evidence and uncertainty.

## 2. Common entry fields

Each registered driver uses:

- `driver_id`
- `canonical_name`
- `aliases`
- `driver_class`
- `physical_domain`
- `state_vocabulary`
- `primary_spatial_scale`
- `primary_temporal_scale`
- `hemisphere_context`
- `season_context_required`
- `observation_or_index_reference`
- `known_mechanism_scope`
- `regional_response_examples`
- `compound_driver_notes`
- `confidence_policy`
- `validation_status`
- `provider_neutrality`
- `version`

## 3. Initial registry

### CDR-ENSO — El Niño–Southern Oscillation

- **Aliases:** ENSO, El Niño, La Niña, neutral ENSO
- **Class:** coupled ocean–atmosphere mode
- **Physical domain:** tropical Pacific ocean and atmosphere
- **State vocabulary:** `el_nino`, `la_nina`, `neutral`, `transitioning`, `uncertain`
- **Spatial scale:** basin to global teleconnection
- **Temporal scale:** interannual, with event evolution over months
- **Hemisphere context:** global; regional interpretation required
- **Season context:** mandatory
- **Index references:** provider-neutral references to recognised SST and pressure-based indices
- **Mechanism scope:** tropical Pacific SST anomalies, Walker-circulation changes and downstream atmospheric teleconnections
- **Response examples:** rainfall, temperature, storm-track, drought, flood or tropical-cyclone tendencies depending on region and season
- **Compound drivers:** IOD, SAM, MJO, monsoon state, subtropical ridge and background warming
- **Guardrail:** never encode `El Niño = drought` as a universal rule
- **Validation status:** `multi_source_supported`

### CDR-IOD — Indian Ocean Dipole

- **Aliases:** IOD, positive IOD, negative IOD
- **Class:** coupled ocean–atmosphere mode
- **Physical domain:** tropical Indian Ocean
- **State vocabulary:** `positive`, `negative`, `neutral`, `developing`, `decaying`, `uncertain`
- **Spatial scale:** basin to regional teleconnection
- **Temporal scale:** seasonal to interannual
- **Hemisphere context:** strongest relevance to Indian Ocean rim and connected circulation; regional interpretation required
- **Season context:** mandatory
- **Index references:** provider-neutral Indian Ocean SST-gradient references
- **Mechanism scope:** east–west SST gradient and atmospheric circulation anomalies
- **Response examples:** rainfall and dryness tendencies across Australia, Africa and surrounding regions
- **Compound drivers:** ENSO, monsoon circulation, SAM and background ocean state
- **Guardrail:** IOD state cannot directly create a local hazard conclusion
- **Validation status:** `multi_source_supported`

### CDR-SAM — Southern Annular Mode

- **Aliases:** SAM, Antarctic Oscillation
- **Class:** atmospheric circulation mode
- **Physical domain:** Southern Hemisphere mid-to-high latitudes
- **State vocabulary:** `positive`, `negative`, `neutral`, `variable`, `uncertain`
- **Spatial scale:** hemispheric to regional
- **Temporal scale:** days to seasonal persistence
- **Hemisphere context:** Southern Hemisphere
- **Season context:** mandatory because regional effects vary strongly by season
- **Index references:** provider-neutral pressure/wind anomaly references
- **Mechanism scope:** north–south displacement and strength of westerly wind belt
- **Response examples:** rainfall, storm-track and temperature tendencies in southern Australia and other Southern Hemisphere regions
- **Compound drivers:** ENSO, IOD, stratospheric variability and blocking
- **Guardrail:** identical SAM phase may support different regional effects by season
- **Validation status:** `multi_source_supported`

### CDR-MJO — Madden–Julian Oscillation

- **Aliases:** MJO
- **Class:** intraseasonal tropical atmospheric mode
- **Physical domain:** tropical convection and circulation
- **State vocabulary:** `phase_1` through `phase_8`, `weak`, `inactive`, `uncertain`
- **Spatial scale:** tropical planetary-scale propagation with regional teleconnections
- **Temporal scale:** intraseasonal, typically weeks
- **Hemisphere context:** global tropical influence; regional interpretation required
- **Season context:** mandatory
- **Index references:** provider-neutral phase/amplitude references
- **Mechanism scope:** eastward-propagating convective and circulation anomalies
- **Response examples:** monsoon bursts, tropical convection, rainfall, cyclone-environment modulation
- **Compound drivers:** ENSO, monsoon state, sea-surface temperatures and subtropical circulation
- **Guardrail:** MJO phase does not guarantee cyclone formation or rainfall at a specific site
- **Validation status:** `multi_source_supported`

### CDR-STR — Subtropical Ridge

- **Aliases:** subtropical high, subtropical ridge, western Pacific subtropical high where regionally scoped
- **Class:** atmospheric pressure and steering structure
- **Physical domain:** subtropical troposphere
- **State vocabulary:** `poleward`, `equatorward`, `strong`, `weak`, `expanded`, `contracted`, `split`, `merged`, `uncertain`
- **Spatial scale:** regional to hemispheric
- **Temporal scale:** synoptic to seasonal
- **Hemisphere context:** hemisphere-specific object instance required
- **Season context:** mandatory
- **Index references:** provider-neutral pressure, geopotential-height or ridge-position references
- **Mechanism scope:** subsidence, storm-track displacement, moisture transport and deep-layer steering contribution
- **Response examples:** rainfall suppression or enhancement tendencies, heat persistence and tropical-cyclone steering influence
- **Compound drivers:** monsoon flow, mid-latitude troughs, MJO, SST state and vertical wind shear
- **Guardrail:** the ridge is not a fixed wall and is not the sole determinant of cyclone track
- **Validation status:** `multi_source_supported`

### CDR-MON — Monsoon System

- **Aliases:** monsoon, regional monsoon circulation
- **Class:** seasonal coupled land–ocean–atmosphere circulation
- **Physical domain:** regional tropical/subtropical atmosphere and land–ocean thermal contrast
- **State vocabulary:** `onset`, `active`, `break`, `retreat`, `strong`, `weak`, `delayed`, `uncertain`
- **Spatial scale:** regional to continental
- **Temporal scale:** seasonal with intraseasonal variation
- **Hemisphere context:** regional instance required
- **Season context:** mandatory
- **Index references:** provider-neutral regional monsoon references
- **Mechanism scope:** seasonal wind reversal, moisture transport and convective organisation
- **Response examples:** rainfall, flood, drought, heat and tropical-cyclone environment tendencies
- **Compound drivers:** ENSO, IOD, MJO, subtropical ridge, SST and land-surface state
- **Guardrail:** there is no single global monsoon outcome; each regional monsoon requires its own boundary and evidence
- **Validation status:** `multi_source_supported`

### CDR-JET — Jet Stream

- **Aliases:** polar jet, subtropical jet, upper-level jet
- **Class:** atmospheric circulation feature
- **Physical domain:** upper troposphere
- **State vocabulary:** `poleward`, `equatorward`, `strengthened`, `weakened`, `zonal`, `amplified`, `blocked`, `uncertain`
- **Spatial scale:** hemispheric to regional
- **Temporal scale:** synoptic to seasonal
- **Hemisphere context:** hemisphere and jet type required
- **Season context:** mandatory
- **Index references:** provider-neutral wind and geopotential references
- **Mechanism scope:** storm-track guidance, wave propagation and upper-level divergence/convergence
- **Response examples:** storm-track shifts, blocking, rainfall and temperature tendencies
- **Compound drivers:** ENSO, SAM/NAO-like modes, stratospheric state, blocking and subtropical ridge
- **Guardrail:** jet-stream configuration must not be reduced to one-dimensional north/south movement
- **Validation status:** `multi_source_supported`

## 4. Registry interpretation rules

1. A registry entry defines a driver object, not an impact forecast.
2. Driver state must always be paired with a time window and provider/reference.
3. Region and season are mandatory before a response tendency is expressed.
4. Compound-driver relationships must remain explicit.
5. An unknown or conflicting state is represented as `uncertain`, not silently normalised.
6. Provider disagreement remains visible through separate evidence references.

## 5. Deferred candidates

Candidates for later controlled registration:

- PDO / IPO
- NAO
- AO
- QBO
- blocking indices
- stratospheric polar-vortex states
- regional ocean-current and marine heatwave drivers

Deferred candidates must not be introduced into production relationships before their object definitions and evidence rules are reviewed.

## 6. Acceptance checklist

- [ ] Seven initial drivers are registered.
- [ ] State vocabularies are machine-translatable.
- [ ] Region, season, hemisphere and lag remain explicit.
- [ ] No driver contains a deterministic hazard or impact rule.
- [ ] Provider-neutral references are preserved.
- [ ] Registry can be extended without changing ontology boundaries.
