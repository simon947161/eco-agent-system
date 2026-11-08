NOAA_AirCore_data_v20210813
Created by Bianca Baier and Colm Sweeney (08/13/2021)
This is the current NOAA AirCore dataset that includes data targeting the following sites:
- Boulder, CO
- Lamont, OK
- Lauder, NZ
- Sodankyla, Finland
- Park Falls, WI
- Edwards AFB/Dryden, CA
- Tra”nou, France 

**Updates to previous dataset (previous version: v20201223): 
- IMPORTANT: CO2 profiles are reported on the WMO x2019 scale 
- Dataset consists of 159 flight days
- A DOI is now available for citing this dataset. Please use: 

Baier, B., Sweeney, C., Newberger, T., Higgs, J., Wolter, S., & NOAA Global Monitoring Laboratory. (2021). NOAA AirCore atmospheric sampling system profiles (Version 20210813) [Data set]. NOAA GML. https://doi.org/10.15138/6AV0-MY81

Available files:
Level 1
- Initial_file - description of AirCore launch which includes description of AirCore, Met and mole fraction measurements.
- Met File - AC[launchyyyymmddHHMM]_[AirCoreID]_py_final_met.csv is a comma separated value with the met data gathered during the duration of the flight (ascent and descent, see variables below)
- Mole Fraction File - AC[launchyyyymmddHHMM]_[AirCoreID]_py_pic.csv is a comma seperated value with mole fraction data from analysis of air in the AirCore (see variables below)
Level 2
- Initial_file - description of AirCore launch which includes description of AirCore, Met and mole fraction measurements.
- Final output file - AirCore[AirCoreID]_[launchyyyyddmmHHMM]_v[yyyymmdd].txt final dry mole fraction values of aircore (see description below)
Level 2/icartt
- Final output files - AC_[AirCoreID]_[launchyyyymmddHHMM]_R# - in NASA ICARTT format for all available AirCore flights

##############################
Final output  Variables:
DateTime (UTC) - yyyy-mm-dd HH:MM:SS
Pressure (mb) - atmospheric pressure (mbar)
lat(N)- latitude (degrees north)
lon(E)- longitude (degrees east)
sec_frm_midnight - seconds from midnight
CO2 (ppm) - calibrated CO2 mole fraction (ppm) on X2019 scale
co2_err (ppm) - CO2 mole fraction uncertainty (ppm)
CH4 (ppb) - calibrated CH4 mole fraction (ppb) on X2004 scale
ch4_err - CH4 mole fraction uncertainty (ppb)
CO (ppb) - calibrated CO mole fraction (ppb) on X2014A scale
co_err - CO mole fraction uncertainty (ppb)
T (C) - Atmospheric temperature (C) - Radiosonde (iMET usually)
TH(K) - Atmospheric potential temperature (K) - Radiosonde (iMET usually)
RH (%)- Atmospheric relative humidity (%)- Radiosonde (iMET usually)
Alt (m) - altitude (m)
AirCoreT(C) - Average AirCore Temperature during flight (C)
alt_err_co2+(m) - estimated diffusion altitude (m) for CO2 above Alt that is included in the measurement
alt_err_co2-(m) - estimated diffusion altitude (m) for CO2 below Alt that is included in the measurement
alt_err_ch4+(m) - estimated diffusion altitude (m) for CH4 above Alt that is included in the measurement
alt_err_ch4-(m) - estimated diffusion altitude (m) for CH4 below Alt that is included in the measurement
alt_err_co+(m) - estimated diffusion altitude (m) for CO above Alt that is included in the measurement
alt_err_co-(m) - estimated diffusion altitude (m) for CO below Alt that is included in the measurement

##############################
INI Variables:
Cylinders_Header - Column headers for trace gas measured
Fill_Std_Values - Mole fraction value for "fill" gas - gas that AirCore has in it before launch
Cal_Std_Values - Mole fraction value for "cal" gas - gas used to calibrate instrument
Chase_Std_Values - Mole fraction value for "chase" gas - gas that follows sample at bottom of AirCore
Fill_Std_ID - ID of tank used for as the "fill" gas
Cal_Std_ID - ID of tank used for as the "cal" gas
Chase_Std_ID - ID of tank used for as the "chase" gas
Analyzer_ID - ID of analyzers used for analysis of trace gases
Mole_fraction_file_name - Name of data file from mole fraction analysis (see description below)
Analysis flow rate - cc/min. Approximate flow rate used during analysis
AirCore_ID - AirCore ID (specific ID of AirCore tubing plus fittings)
Met_Sensor_ID - ID of met (RH, T) sensors used
Met_file_name - Name of met data file (see description below). 
CO_flag - (0 or 1) indicates CO was used as a tracer for mixing.
flip - (0 or 1) indicates whether AirCore is being analyzed top (1) first or bottom (0) first
Tot_AirCore_launched - Total AirCore balloons launched during a single day (UTC)
Tot_AirCore_Strings - Total AirCore samplers launched during a single day (UTC)
Valve_Close_Delay - delay (minutes) between AirCore landing and valve closing 
Min_indx_Cutoff - PI QA/QC cutoff of AirCore profile top
Max_indx_Cutoff - PI QA/QC cutoff of AirCore profile bottom
Home_Institution - PI home institution
AirCore Dimensions:
 - Section number - incremental section in AirCore from top to bottom and includes sample measurement apparatus. 
 - Description - Text description of section.
 - Used_fill - used_fill(1) when being used during sampling 
 - Used_analysis - Used_analysis(1) when being used during analysis phase
 - length - length(m) of section.
 - Diameter - Inner diameter (m) of section
 - Porosity - Fraction of total volume available for airflow
 - CV - Critical flow value of section. 1 suggests no critical flow value

##############################
Met Data Variables:
secs_since_midn_UTC - seconds after midnight 
lat(N)- degrees
lon(E)- degrees
Alt (m)- meters
Pressure (mb) - mbars
T (C)- Temperature, celcius (Radiosonde)
RH (%)- Relative Humidity, percent (Radiosonde)
Tcore1 - AirCore temp1
Tcore2 - AirCore temp1
Tcore3 - AirCore temp1
Tcore4 - AirCore temp1
Tcore5 - AirCore temp1
Flight - Ground(0)/Ascent(1)/Descent(2) 
close - Valve close after landing (1). Not closed (0)
smooth_alt - Smoothed altitude profile
smooth_Pamb - Smoothed pressure profile
smooth_Tamb - Smoothed temperature profile
smooth_Tcoil - Smoothed average aircore temperature profile - Average of most 1-5 temperature sensors in AirCore 
fract_moles_imet - output on flow model indicating the fraction (relative to the landing) of total dry air capture at each altiude during flight
dP_mb - differential pressure (mbar) measured between ambient and closed end of the AirCore

*NOTE* on met data variables: 
The temperature and relative humidity profiles reported in the final AirCore files are radiosonde (i.e. iMet) temperature and pressure measured
upon descent. RH data for each Level2 file as of 11/5/2019 now uses RH data collected during ascent rather than descent due to observed hysteresis in the sensor. However the following caveats apply: 
- Large spikes - we will use descent data if the ascent RH profile relative to the descent profile above 10-12km has large spikes indicative of balloon H2O(g) shedding, and 
- Low data yield - we will use descent data if less than 80% of the ascent RH profile is recovered.

Both ascent and descent T/RH profiles are provided for the data user in the Level1 met file for data users.    

##############################
Mole Fraction Data Variables:
tco2_since_midn_UTC - seconds after midnight (use data of filename as midnight)
CO2(ppm) - CO2 dry mole fraction (umol CO2/mol dry air) 
CH4(ppb) - CH4 dry mole fraction (nmol CH4/mol dry air)
CO (ppb) - CO dry mole fraction (nmol CH4/mol dry air)
AirCore_index - AirCore_index(1) estimated beginning to end of AirCore sample.  AirCore_index(0) when running standards or other AirCores
top_mix_index - top_mix_index(1) marking mixing between "fill" gas and "clean" sample at top of aircore.
bot_mix_index - bot_mix_index(1) marking mixing between "chase" gas and "clean" sample at bottom of aircore sample. 
