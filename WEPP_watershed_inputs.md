# WEPP Watershed Analysis Input Files

This documentation provides a comprehensive guide to the input files required for running the Water Erosion Prediction Project (WEPP) for watershed analysis, including hillslopes, channels, and impoundments.

## Required Input Files for WEPP Components

| Component | Required Files | Optional Files |
|-----------|---------------|----------------|
| Hillslope | Climate (.cli)<br>Slope (.slp)<br>Soil (.sol)<br>Management (.man) | Run (.run)<br>Irrigation (.sim/.fim) |
| Channel   | Slope (.csl)<br>Soil (.cso)<br>Management (.chm)<br>Climate (.chc)<br>Channel (.chn) | Irrigation (.sim/.fim) |
| Impoundment | Impoundment (.imp) | - |
| Watershed | Structure (.str)<br>Hillslope Pass (.hil)<br>All hillslope, channel, and impoundment files | Watershed Run (.run) |

## Hillsope, and Channel slopes and structure files
Available from peridot/src/watershed_abstraction.rs in the weep in the woods repo https://github.com/wepp-in-the-woods/peridot/blob/main/src/watershed_abstraction.rs .

## Climate file
Step 1: Get the station meta objects from stationManager = CligenStationsManager(version=2015) 
stationMeta = stationManager.get_closest_station((-117, 46)) from there https://github.com/wepp-in-the-woods/wepppy2/blob/f5786755bbdd3c9c1599db42ee1da119ca04eea3/climates/cligen/__init__.py#L1881C5-L1883C65
Step 2: Go to this fucntion and call it: this is the main function-- https://github.com/rogerlew/wepppy/blob/abb28662476b220d539a3ad4157120ca897266f9/wepppy/nodb/climate.py#L356
This is an observed daymet fucntions that extracts the daymet climate data and also processes the input for cligen runs and runs the cligen as well.This cli_dir is the path to save the lcimate input file (i.e., the .cli file that goes into WEPP)
This will also save the daymet raw data into the same cli_dir path. 

cligen executable (linux binary) is saved in https://github.com/wepp-in-the-woods/wepppy2/blob/main/climates/cligen/bin/cligen532
this executable is path is saved in the _bin_dir variable in the class 

## Watershed Analysis Process in WEPP

The WEPP watershed model simulates:
1. Runoff and erosion on hillslopes
2. Water and sediment routing through channels
3. Impoundment effects on water and sediment
4. Sediment deposition and delivery at watershed outlet

The watershed application calculates sediment delivery, deposition, and enrichment for each element, allowing detailed source-to-outlet tracking of runoff and sediment.

## Detailed File Structures for Watershed Analysis

### 1. Hillslope Files (Required for each hillslope)

#### Climate File (.cli)
```
4.10                                  # CLIGEN version number
1 0 0                                 # Simulation mode, breakpoint flag, wind flag
Station: WEST_LAF IN CLIGEN V4.1      # Station identification
Latitude Longitude Elevation (m) Obs. Years Beginning year Years simulated
40.50 -87.00 200 30 2022 10           # Location parameters
Observed monthly ave max temperature (C)
-3.2 0.1 6.5 14.8 21.3 26.4 28.5 27.3 23.8 17.0 8.2 0.0   # Monthly temperature data
# [Additional lines for other climate parameters]
da mo year prcp dur tp ip tmax tmin rad w-vl w-dir tdew
1 1 2022 0.0 0.00 0.00 0.00 -2.3 -11.1 100 3.0 180 -8.5   # Daily climate data
# [Additional lines of daily climate data]
```

#### Slope File (.slp)
```
95.7                                  # Version control number
1                                     # Number of OFEs
100 100                               # Aspect (degrees), profile width (m)
3 100                                 # Number of slope points, length of OFE (m)
0.0,0.0 0.5,0.09 1.0,0.0              # Point pairs: distance(fraction), slope(m/m)
```

#### Soil File (.sol)
```
95.7                                  # Version control number
# Example Soil Input File for WEPP      # User comment line
1 1                                     # Number of OFEs, hydraulic conductivity flag (1=adjust)
'MIAMI' 'silt loam' 3 0.14 0.75 4500000 0.0074 3.5 6.8    # Soil identifiers and parameters
200 31.3 25.9 2.4 14.9 8.1             # Layer 1: depth(mm) sand% clay% OM% CEC rock%
400 35.1 27.6 1.4 13.7 8.9             # Layer 2 parameters
1000 34.2 26.7 0.4 11.5 9.6            # Layer 3 parameters
```

#### Management File (.man)
```
95.7                                  # Version control number
# Created on 1Jan22                   # Comment lines
1                                     # Number of OFEs
5                                     # Years in simulation

# Plant Growth Section                # (Contains plant parameters)
1                                     # Number of plant scenarios
CORN2                                 # Plant name
'Corn - Medium Fertilization Level'   # Description
1                                     # Landuse (1=cropland)
WeppWillSet                           # Units
3.6 3 28 10 3.2 60 0 0.304 0.65 0.051 # Plant parameters (line 1)
# [Additional plant parameter lines]

# Operation Section                   # (Contains tillage implement parameters)
1                                     # Number of operation scenarios  
PLNTSC                                # Operation name
# [Additional operation information]

# Initial Conditions Section          # (Contains initial soil/plant conditions)
1                                     # Number of initial condition scenarios
NOTLCORN                              # Scenario name
# [Additional initial condition information]

# Surface Effects Section             # (Contains tillage sequences)
1                                     # Number of surface effects scenarios
NOTLCORN                              # Scenario name
# [Additional surface effects information]

# Contouring Section                  # (Contains contouring information)
0                                     # Number of contouring scenarios

# Drainage Section                    # (Contains drainage information)
0                                     # Number of drainage scenarios

# Yearly Section                      # (Contains yearly management)
1                                     # Number of yearly scenarios
CORNNOTL                              # Scenario name
# [Additional yearly information]

# Management Section                  # (Ties scenarios together by OFE/year)
CORNNOTL                              # Management name
1                                     # Number of OFEs
1                                     # Initial conditions index for OFE
5                                     # Number of rotation repeats
1                                     # Years in rotation
# [Additional management information]
```

### 2. Channel Files (Required for all channels)

#### Channel Slope File (.csl)
```
95.7                                  # Version control number
2                                     # Number of channels
200 5                                 # Aspect (degrees), width (m) for channel 1
7 100                                 # Number of slope points, length (m)
0,0 0.2,0.05 0.37,0.09 0.55,0.02 0.71,0.06 0.88,0.03 1,0.01   # Point pairs
200 5                                 # Aspect, width for channel 2
# [Additional channel information]
```

#### Channel Soil File (.cso)
```
95.7                                  # Version control number
# Channel Soil Example                # User comment line
2 1                                   # Number of channels, hydraulic conductivity flag
'CHANNEL' 'silt loam' 3 0.14 0.75 4500000 0.0074 3.5 6.8   # Channel 1 soil parameters
# [Layer information for channel 1]
'CHANNEL2' 'sandy loam' 2 0.16 0.75 5500000 0.0092 3.2 12.5   # Channel 2 soil parameters
# [Layer information for channel 2]
```

#### Channel Management File (.chm)
```
95.7                                  # Version control number
# Channel Management Example          # Comment lines
2                                     # Number of channels
5                                     # Years in simulation

# Plant Growth Section                # (Similar structure to hillslope management)
1                                     # Number of plant scenarios
GRASS                                 # Plant name
# [Additional plant information]

# [Additional sections similar to hillslope management file]

# Management Section                  # (Ties scenarios together by channel/year)
GRASS_CHANNEL                         # Management name
2                                     # Number of channels
1                                     # Initial conditions index for channel 1
2                                     # Initial conditions index for channel 2
# [Additional management information]
```

#### Channel File (.chn)
```
95.7                                  # Version control number
2                                     # Number of channels
1                                     # Peak calculation method (1=EPIC, 2=CREAMS)
1.50                                  # Length to width ratio

# First channel                       # Comment line
1                                     # Shape (1=triangular, 2=naturally eroded)
2                                     # Control structure (2=normal flow)
1                                     # Friction slope calculation method
4                                     # Output type
5.0 0.030                             # Bank slope (m/m), Manning's n (bare soil)
0.040 0.0082 3.5 0.3 0.3              # Total Manning's n, erodibility, critical shear, depths
0.026 5.0 0.060                       # Control structure parameters

# Second channel                      # Comment line
# [Similar information for channel 2]
```

### 3. Impoundment File (.imp)

```
95.7                                  # Version control number
2                                     # Number of impoundments
Test Impoundment With Rock Fill       # Description
# [Additional comment lines]

0                                     # Drop spillway (0=not present)
0 0                                   # Culvert (0=not present) and number of culverts
1                                     # Rock-fill Check dam (1=present)
Impoundment With Rock Fill Outlet     # Description
2.5 1.0 2.0 2.0 0.50                  # Rock-fill parameters: length, stage, overtop, width, diameter
0                                     # Emergency spillway (0=not present)
0                                     # Filter fence (0=not present)
0                                     # Perforated riser (0=not present)
2.00 1.0 0.00 0.1 0.009               # Miscellaneous data: overtop, full stage, initial stage, time step, infiltration
2 2                                   # Structure size, particle subclasses
14                                    # Number of stage-area-length points
0.0 250.0 12.0                        # Min stage, area, length
# Stage data
1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0 10.0 12.0 14.0 16.0 18.0
# Area data
450.0 650.0 825.0 1000.0 1125.0 1250.0 1375.0 1500.0 1650.0 1800.0 2075.0 2315.0 2545.0 2775.0
# Length data
16.0 19.0 21.0 23.0 24.5 26.0 27.5 29.0 30.0 31.0 33.0 35.0 37.0 38.0

# Second impoundment description
# [Similar information for impoundment 2]
```

### 4. Watershed Structure Files

#### Structure File (.str)
```
95.7                                  # Version control number
2 0 1 0 0 0 0 0 0 0                   # Element #6: impoundment with hillslope 1 on right
2 0 0 0 0 0 0 0 6 0                   # Element #7: channel fed by impoundment 6
2 0 0 0 0 0 7 0 0 0                   # Element #8: channel fed by channel 7
2 0 2 0 0 0 0 0 0 0                   # Element #9: channel with hillslope 2 on right
# [Additional elements]
```

#### Hillslope Pass File (.hil)
This file is automatically created when running hillslope simulations and contains runoff and erosion results for each hillslope.

### 5. Watershed Run File (.run)

```
1                                     # WEPP continuous simulation
3                                     # Watershed version
E:\WEPP\INPUT\SHED\PASS\watershed.pas # Watershed pass file
0                                     # Average annual watershed output
watershed.sum                         # Summary output file name
Yes                                   # Water balance output?
water.out                             # Water balance output file name
Yes                                   # Plant/crop output?
crop.out                              # Plant/crop output file name
No                                    # Soil output?
Yes                                   # Channel erosion plotting?
plot.out                              # Plot file name
No                                    # Watershed graphics output?
Yes                                   # Event by event output?
event.out                             # Event output file name
Yes                                   # Final summary?
summary.out                           # Final summary file name
No                                    # Winter output?
No                                    # Yield output?
watershed.str                         # Watershed structure file name
Yes                                   # Impoundment output?
impound.out                           # Impoundment output file name
channel.chn                           # Channel file name
channel.chm                           # Channel management file name
channel.csl                           # Channel slope file name
west_laf.chc                          # Channel climate file name
channel.cso                           # Channel soil file name
impound.imp                           # Impoundment input file name
0                                     # No irrigation
10                                    # Number of years of simulation
No                                    # Event bypass?
```

## WEPP Watershed Outputs

Watershed analysis in WEPP produces a comprehensive set of outputs:

### 1. Summary Output Files
- **Watershed Summary File**: Overall watershed results including:
  - Average annual runoff and erosion at the watershed outlet
  - Sediment delivery ratio for the watershed
  - Specific surface index and enrichment ratio
  - Particle size distribution of sediment leaving the watershed
  - Annual, monthly or event-by-event summaries depending on options selected

### 2. Element-Specific Outputs
- **Hillslope Results**: Runoff, soil loss, deposition for each hillslope
- **Channel Results**: Channel detachment, deposition, sediment transport
- **Impoundment Results**: Sediment trapping efficiency, inflow/outflow volumes

### 3. Detailed Process Outputs
- **Water Balance Files**: Daily soil moisture, evapotranspiration, percolation
- **Plant Growth Files**: Biomass development, crop yield, canopy cover
- **Event Files**: Storm-by-storm analysis of runoff and erosion
- **Impoundment Files**: Storage dynamics, sediment retention by particle class

### 4. Spatial Outputs
- **Profile Plot Files**: Spatial distribution of erosion/deposition on hillslopes
- **Channel Erosion Files**: Spatial patterns of channel detachment/deposition

## Key Watershed Processes Modeled by WEPP

1. **Hillslope Hydrology and Erosion**:
   - Infiltration using modified Green-Ampt equation
   - Runoff generation and routing
   - Interrill and rill erosion
   - Deposition as function of transport capacity

2. **Channel Processes**:
   - Channel hydrology (transmission losses)
   - Peak flow calculation (modified rational formula or CREAMS method)
   - Channel detachment when flow shear > critical shear
   - Deposition when sediment load > transport capacity
   - Selective transport by particle size

3. **Impoundment Processes**:
   - Water routing through various outlet structures
   - Sediment deposition based on particle settling velocities
   - Outflow concentration calculations
   - Stage-discharge relationships for different structures

4. **Sediment Routing and Delivery**:
   - Continuity-based sediment routing
   - Particle size selective erosion and deposition
   - Enrichment of finer sediment particles
   - Mass balance across the entire watershed

## Watershed Output Analysis

The WEPP watershed output allows analysis of:

1. **Source Area Contributions**: Identify which hillslopes contribute most sediment
2. **Channel Network Effects**: Understand sediment routing through channels
3. **Impoundment Efficiency**: Evaluate sediment trapping in structures
4. **Management Scenarios**: Compare different conservation practices
5. **Temporal Patterns**: Analyze seasonal and annual variations
6. **Event-Scale Processes**: Examine individual storm responses
7. **Sediment Budgets**: Track sediment from source to outlet
8. **Sediment Enrichment**: Evaluate changes in particle size distribution

## Important Considerations

1. The watershed model must be carefully parameterized for each component.
2. Spatial relationships between elements must be accurately represented in the structure file.
3. Channel and impoundment parameters have significant effects on sediment delivery.
4. Watershed applications are limited to field-scale areas with ephemeral gullies or constructed waterways.
5. The model is not designed for watersheds with permanent channels or perennial streams.
6. Maximum recommended watershed size is approximately 260 hectares (640 acres).
