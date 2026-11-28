This README file was generated on 2022-05-19 by Eirik Starheim Svendsen.
Last updated: 2022-05-20.


-------------------
GENERAL INFORMATION
-------------------
// Title of Dataset: Replication data for: Energy flow analysis of an industrial ammonia refrigeration system
// DOI: 10.5281/zenodo.6563580
// Contact Information

     // Name: Eirik Starheim Svendsen 
     // Institution: SINTEF Ocean
     // Email: eirik.starheim.svendsen@sintef.no
     // ORCID: 0000-0002-4148-1539

// Kind of data: Data files (.txt), table (.png) and figures (.png)
// Date of data collection/generation: 2021-08-01 - 2021-12-31
// Funding sources: Project KSP PCM-STORE (308847) supported by the Research Council of Norway and industry partners. 

// Description of dataset: 
This dataset includes energy data acquired from a pelagic fish processing plant, including data from an industrial ammonia refrigeration system that provides cooling and freezing. In addition, production data is included. Data from the system was analysed within the KSP project PCM-STORE (308847) supported by the Research Council of Norway and industry partners. PCM-STORE aims at building knowledge on novel PCM technologies for low-temperature thermal energy storage. Collecting and analysing data is an important part of evaluating the potential for reduction of CO2 emissions and increasing energy efficiency. Many processing plants measure and log data, but it is not often published. This dataset includes specific energy demand, peak power demand, power demand for different sections of the plant, ambient temperatures, and production volumes. The data was collected in 2021. The included graphics show the refrigeration system and some resulting tables and graphs. Production follows a seasonal cycle throughout the year, with no (or very low) production in the spring (Mar-May), and peak production in the autumn (Sep-Nov). The cycle is linked to the seasonal availability of fish. Annual SEC numbers (200-247 kWh/tonnes) were found to be in line with other Norwegian pelagic plants. A strong dependency between SEC and volume throughput were also found, where months of low production resulted in high SEC values and vice versa. Knowledge about the processes indicates that a fillet production is more energy intensive compared to round production, due to more energy demand from the fillet sections, higher mass (fish and brine) in each box and higher requirement of hot water for cleaning. This dataset is related to the conference paper "Energy flow analysis of an industrial ammonia refrigeration system and potential for a cold thermal energy storage" presented at the 15th IIR Gustav Lorentzen Conference on Natural Refrigerants, Trondheim, Norway 13-15 June 2022. 

--------------------------
METHODOLOGICAL INFORMATION
--------------------------
The processing plant in question has several separate logging systems for measuring, monitoring and storing data related to temperatures, pressures, energy consumption and other variables. In this work, data from the energy measurement system is gathered and processed. In addition, production data was acquired from the plant, reported as monthly values for each product category.

Raw data from the energy system was stored in tabular files, each row representing a date and sensor (M001 through M057) with hourly sensor readings stored in 24 columns. Sensors in this context refers to power meters, reporting power measurements in kW with one significant digit. Raw data was pre-processed and checked for missing values by utilizing an ad hoc ETL script written in python, where the analyse-ready data was converted to a more conventional timeseries format with each sensor assigned to a column. In the next place, sensors were added togehter in groups representing aggregated energy consumption of different sections of the plant which were of interest to this study, and groups were named accordingly. Finally, calculations were carried out to report on KPIs of interest, such as specific energy consumption (SEC), showing energy consumption in shares and/or normalised against max values etc.

--------------------
DATA & FILE OVERVIEW
--------------------
01_misc_data.txt
02_SEC_monthly_data.txt
03_daily_energy_data.txt
04_hourly_energy_data.txt
05_Figure_1.png
06_Table_1.png
07_Figure_2.png
08_Figure_3.png
09_Figure_4.png
10_Figure_5.png
11_Figure_6.png
12_Figure_7.png
13_Figure_8.png
14_Figure_9.png


-----------------------------------------
DATA-SPECIFIC INFORMATION FOR: Common
-----------------------------------------
Please note that comma (,) is used as decimal separator for these datasets.

Sections 
Shorthand		Section
ref_sys_1		Refrigeration system 1
ref_sys_2		Refrigeration system 2
rsw			RSW system
el_boiler		Electrical boiler
fillet_sections		Fillet sections (2)
others			Everything else that is not covered by sections above


-----------------------------------------
DATA-SPECIFIC INFORMATION FOR: 01_misc_data.txt
-----------------------------------------
The file is structured with 5 columns named variable, subvariable, period, unit and value. Variable denotes a standalone dataset, with subvariable, period and unit as descriptors and value as data value.

variable: sec_annual
	subvariable: none
	period: 2017, 2018, 2019, 2020, 2021
	unit: kWh/tonnes
	Annual specific energy consumption (SEC) measured at the facility

variable: average_monthly_production_normalised
	subvariable: none
	period: januar through december
	unit: unitless (share)
	Monthly production values at the facility normalised against the highest measured value within the period 2017-2021

variable: product_category
	subvariable: whole_frozen, fillet_frozen, roe
	period:	2017-2021
	unit: unitless (share)
	Production volume by category, shares, on aggregated data for 2017-2021

variable: peak_power
	subvariable: none
	period: 01.2021 through 12.2021
	unit: MW
	Highest measured peak power (monthly) at the facility

variable: power_consumption_by_section
	subvariable: sections (see 'Common' and 06_Table_1.png)
	period: whole_year_2021, production_period_2021, non_production_period_2021
	unit: unitless (share)
	Measured energy consumption at the facility, listed as shares by each section, for three different periods within 2021: whole year, production month and month without production.

variable: monthly_production_relative
	subvariable: none
	period: 01.2021 through 12.2021
	unit: unitless
	Monthly production values for 2021 normalised against the month with highest production (08.2021)

-----------------------------------------
DATA-SPECIFIC INFORMATION FOR: 02_SEC_monthly_data.txt
-----------------------------------------
The file is structured with 4 columns, production_volume (tonnes), fillet_share (-), SEC (kWh/tonnes) and TEC (kWh), where each row represents one of the 47 months between 2017-2021 (i.e., months in which production was taking place).

fillet_share: of the total monthly production volume, how much of the processed fish were filleted (as opposed to whole freezing and roe production). 
SEC: specific energy consumption
TEC: total energy consumption

-----------------------------------------
DATA-SPECIFIC INFORMATION FOR: 03_daily_energy_data.txt
-----------------------------------------
This file is structured with 5 columns, date (dd.mm.yyyy), TEC_daily (MWh), temperature_type, avg_ambient_temperature (°C) and load_elboiler_relative (-). Each row represents a day between 01.01.2021 through 31.12.2021.

Temperature data was acquired from https://frost.met.no (weather station ID SN59210). Some daily values for the period were missing, and interpolated values are reported in place. The column 'temperature_type' denotes whether or not the reported value is an observation or an interpolated value.

load_elboiler_relative: energy consumption of the electrical boiler reported as a relative value, i.e., daily energy readings are normalised against the highest measured daily reading (03.12.2021).

-----------------------------------------
DATA-SPECIFIC INFORMATION FOR: 04_hourly_energy_data.txt
-----------------------------------------
This file is structured with 4 columns, date (dd.mm.yyyy), time (hh:mm), ref_sys_1 (kW) and el_boiler (kW).

Each row represents hourly readings of refrigeration system number 1 (ref_sys_1) and the electrical boiler (el_boiler) for a sample period (05.01.2021 00:00-14.01.2021 23:00). 

-----------------------------------------
DATA-SPECIFIC INFORMATION FOR: .png-files
-----------------------------------------
Files (05_..) and (07_.. through 14_..) shows figures from the associated publication, which shows all data within this dataset in different visual graphs.
File 06_Table_1.png shows a table describing the different sections of the plant, i.e., how sensor data from the raw data was grouped together to provide sensible information about the plant.


--------------------------
SHARING/ACCESS INFORMATION
--------------------------
Use citation as recommended by the repository for use of this dataset. See repository for license type.


