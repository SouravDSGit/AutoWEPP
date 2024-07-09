# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 12:54:58 2024

@author: SouravMukherjee
"""

import pandas as pd
import numpy as np

 

# Specify the directory where you want to save the CSV files
output_dir = "C:/Users/souravmukherjee.USDA/Box/external EFR Study_Extreme Precip_DesignFlood/3rd Phase_Geomorphological Assessment/Data/WEPP/Run/summary_csv"

# Define the column names
column_names = ['year','total_precip_mm','total_irrig_mm','runoff_rain_mm','runoff_snowmelt_mm','runoff_irrig_mm','tot_detach_kgperm2','tot_interill_detach_kgperm2','tot_deposit_kgperm2','sediment_yield_kgperm','enrich_ratio_m2perm2','extra']

# Area values from csv
dfarea = pd.read_csv('C:/Users/souravmukherjee.USDA/Box/external EFR Study_Extreme Precip_DesignFlood/3rd Phase_Geomorphological Assessment/HBR_Culvert_Upareas/hillslope_areas.csv')
for i in range(1, 203):
    input_filename = f"C:/Users/souravmukherjee.USDA/Box/external EFR Study_Extreme Precip_DesignFlood/3rd Phase_Geomorphological Assessment/Data/WEPP/Run/summary_{i}"
    output_filename = f"{output_dir}/summary_{i}.csv"
    
    # Read the contents of the text file
    with open(input_filename, 'r') as f_in:
        lines = f_in.readlines()
        
    # Skip the first 11 lines and split the remaining lines into columns
    data = [line.strip().split() for line in lines[11:]]
    
    
    # Create a DataFrame from the data
    df = pd.DataFrame(data, columns=column_names)
    
    # Delete rows 
    df.drop([44,46], inplace=True)  # Delete row 44 and 46
    df=df.drop(index=range(47,67))
    
    
    
    # Open the file
    with open(f'C:/Users/souravmukherjee.USDA/Box/external EFR Study_Extreme Precip_DesignFlood/3rd Phase_Geomorphological Assessment/Data/WEPP/Run/culvert_hillslope_{i}.slp', 'r') as file:
        # Read the lines into a list
        lines = file.readlines()
    
    # Get the second line (index 1), split it into values, and get the second value (index 1)
    rep_width_m = float(lines[2].split()[1]) # extracting the representative width of the hillslope
    
    area_Ha = dfarea.loc[dfarea['Culvert Index'] == i, 'Area (Ha)'].values.sum()
    
    # adding overland flow length and hillslope area to the summary dataframe
    df['area_Ha'] = np.repeat(area_Ha, len(df))  
    df['Rep_width_m']=np.repeat(rep_width_m, len(df))  
    
    # Write the DataFrame to a CSV file
    df.to_csv(output_filename, index=False)
