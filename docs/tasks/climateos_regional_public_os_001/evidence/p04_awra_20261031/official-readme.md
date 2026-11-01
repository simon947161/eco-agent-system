# The Australian Water Outlook Historical Sub-Collection

This README gives some detailed information on the AWO Historical simulation sub-collection - first for the historical water balance, and then evapotranspiration datasets.

It aims to complement the high level information available in the [NCI collections catalogue](https://geonetwork.nci.org.au/), and in the AWO webpage's [About page](https://awo.bom.gov.au/about/overview/historical), for those using the NetCDF files directly.

## Historical water balance

### Naming conventions for simulated variables in filenames

The first column below lists the short-hand version of simulated AWRA model
variables used in the prefix part of all filenames.

| Prefix | Variable | Unit |
| --- | --- | --- |
| rain_day | Precipitation | mm |
| e0 | Modelled potential evapotranspiration | mm |
| etot | Modelled actual evapotranspiration | mm |
| qtot | Runoff | mm |
| dd | Deep drainage | mm |
| sm | Rootzone soil moisture (0-1m depth) | mm |
| sm_pct | Rootzone soil moisture (0-1m depth) | % full |
| s0 | Upper soil moisture (0-0.1m depth) | mm |
| s0_pct | Upper soil moisture (0-0.1m depth) | % full |
| ss | Lower soil moisture (0.1-1m depth) | mm |
| ss_pct | Lower soil moisture (0.1-1m depth) | % full |
| sd | Deep soil moisture (1-6m depth) | mm |
| sd_pct | Deep soil moisture (1-6m depth) | % full |

The simulated variables are stored in NetCDF files depending on temporal and spatial aggregation:

* Australia-wide gridded files at daily scale are of the form XX_YYYY.nc, where YYYY is the year.

* All other spatial and temporal combinations are of the form XX.nc, where the full period is stored in one file for each variable.

### Directory structure

NetCDF files providing the raw national model simulations for each variable are provided in the uppermost directory, with various post-processed outputs provided in the `processed` directory within.

Top-level directory - `/g/data/iu04/australian-water-outlook/historical/v1/AWRALv7/`
 - Daily gridded raw simulated model output files for each variable.

`processed/`
 - `values/` (temporally aggregated grids and soil moisture converted to % full, incl. `sm`, `sm_pct`)
    - day (soil moisture converted to % full)
    - month (monthly aggregated/averaged values)
    - year (annually aggregated/averaged values)
    - month_td (month to date values)
    - year_td (year to date values)
 - `deciles/` (relative values ranked according to climatology)
    - day (all variables)
    - month (monthly aggregated/averaged values)
    - year (annually aggregated/averaged values)
    - month_td (month to date values)
    - year_td (year to date values)
 - `catchments_X/` (regionally aggregated data = see note [2] below for available regions)
    - values (temporally aggregated grids and soil moisture converted to % full)
    - deciles (relative values ranked according to climatology)

**Note 1**: Any files in `bins` sub-directories contain information on the climatology calculated percentiles for each variable at the relevant spatial and temporal scale. They are used to create the `deciles` processed versions of the AWRA outputs.

**Note 2**: Re region-specific spatially aggregated simulated variables.
These are available at several scales. Listed from smallest to largest they are:
 - `catchments_V32_RR`: These are aggregated to match the catchment river regions,
   per the Bureau of Meteorology Geofabric, version 3.2
 - `catchments_states`: These are aggregated to Australian state spatial boundaries
 - `catchments_national`: These are Australia-wide aggregated versions of the simulated variables.

### Notes on NetCDF format

These NetCDF files generally follow the [CF Metadata Conventions](https://cfconventions.org/) in terms of variable naming, specification of units etc - especially for spatial and time dimensions.

Of note regarding the time dimension variables: the metadata for these generally specifies the units as `"days since 1900-01-01"` - including for data aggregated into totals for monthly and yearly spatial periods, noted above. This is per CF conventions advice which "...recommends that year and month should not be used, because of the potential for mistakes and confusion" given those periods do not correspond to standard calendar months.

## Historical evapotranspiration

### Naming conventions for simulated variables in filenames

The first column below lists the short-hand version of simulated ET model
variables used in the prefix part of all filenames.

| Prefix | Variable | Unit |
| --- | --- | --- |
| ma_wet | Areal potential evapotranspiration | mm |
| pen_pet | Synthetic pan evaporation | mm |
| fao_pet | Reference crop evapotranspiration - Short | mm |
| asce_pet | Reference crop evapotranspiration - Tall | mm |
| msl_wet | Open water evaporation | mm |

The simulated variables are stored in NetCDF files depending on temporal and spatial aggregation:

* Australia-wide gridded files at daily scale are of the form XX_YYYY.nc, where YYYY is the year.

* All other spatial and temporal combinations are of the form XX.nc, where the full period is stored in one file for each variable.

### Directory structure

NetCDF files providing the raw national model simulations for each variable are provided in the uppermost directory, with various post-processed outputs provided in the `processed` directory within.

Top-level directory - `/g/data/iu04/australian-water-outlook/historical/v1/ET/`
 - Daily gridded raw simulated model output files for each variable.

`processed/`
 - `values/` (temporally aggregated grids)
    - month (monthly aggregated/average values)
    - year (annually aggregated/average values)
    - month_td (month to date values)
    - year_td (year to date values)
 - `catchments_X/` (regionally aggregated data = see note [1] below for available regions)
    - values (temporally aggregated grids and soil moisture converted to % full)

**Note 1**: Re region-specific spatially aggregated simulated variables.
These are available at several scales. Listed from smallest to largest they are:
 - `catchments_V32_RR`: These are aggregated to match the catchment river regions,
   per the Bureau of Meteorology Geofabric, version 3.2
 - `catchments_states`: These are aggregated to Australian state spatial boundaries
 - `catchments_national`: These are Australia-wide aggregated versions of the simulated variables.

### Notes on NetCDF format

Please see the above notes in the corresponding sub-section under the *Historical water balance* section, which also apply to the *Historical evapotranspiration* outputs.
