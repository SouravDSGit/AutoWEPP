# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 12:41:29 2024

@author: SouravMukherjee
"""
import pandas as pd

# Create an empty DataFrame to store the data
df = pd.DataFrame(columns=[
    "Polygon_ID",
    "Total_Precip (mm)",
    "Runoff_Rain (mm)",
    "Runoff_Snowmelt (mm)",
    "Overlan_Flow_Length (m)",
    "Hillslope_Rep_Width (m)",
    "Hillslope_Drainage_Area (Ha)",
    "Sediment Yield per Area (tons/Ha/Yr)",
    "Sediment Yield per Area (Kg/Ha/Yr)",
    "Total Erosion (tonnes/yr)" 
])
# Loop through the range of i values (1 to 202)
for i in range(1, 203):
    filename = f"C:/Users/souravmukherjee.USDA/Box/external EFR Study_Extreme Precip_DesignFlood/3rd Phase_Geomorphological Assessment/Data/WEPP/Run/summary_csv/summary_{i}.csv"
    df0=pd.read_csv(filename);
    
    # Extracting the overland flow length from the slope input file
    with open(f'C:/Users/souravmukherjee.USDA/Box/external EFR Study_Extreme Precip_DesignFlood/3rd Phase_Geomorphological Assessment/Data/WEPP/Run/culvert_hillslope_{i}.slp', 'r') as file:
        # Read the lines into a list
        lines = file.readlines()
    
    # Get the fourth line (index 1), split it into values, and get the second value (index 1)
    overland_flow_length_m = float(lines[3].split()[1]) # extracting the hillslope profile length
    
    # Create a dictionary with extracted data
    data = {
        "Polygon_ID":i,
        "Total_Precip (mm)": df0.iloc[44,2],
        "Runoff_Rain (mm)": df0.iloc[44,4],
        "Runoff_Snowmelt (mm)": df0.iloc[44,5],
        "Overlan_Flow_Length (m)": overland_flow_length_m, 
        "Hillslope_Rep_Width (m)": df0.iloc[44,13],
        "Hillslope_Drainage_Area (Ha)": df0.iloc[44,12],
        "Sediment Yield per Area (tons/Ha/Yr)": ((df0.iloc[44,10]*df0.iloc[44,13])/df0.iloc[44,12])*0.00110,
        "Sediment Yield per Area (Kg/Ha/Yr)": (df0.iloc[44,10]*df0.iloc[44,13])/df0.iloc[44,12],
        "Total Erosion (tonnes/yr)" : df0.iloc[44,10]*df0.iloc[44,13]*0.00110
        }

    # Create a Series from the dictionary and append it to the DataFrame (efficient method)
    df = df.append(data, ignore_index=True)

    # ... (optional: print progress indicator)
    # print(i)

# Create the output filename
output_filename = "C:/Users/souravmukherjee.USDA/Box/external EFR Study_Extreme Precip_DesignFlood/3rd Phase_Geomorphological Assessment/Data/WEPP/output/output_file.csv"

# Save the final DataFrame as CSV
df.to_csv(output_filename, index=False)

print("Data extraction and combination complete!")