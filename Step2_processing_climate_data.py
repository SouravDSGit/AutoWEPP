# -*- coding: utf-8 -*-
"""
Created on Fri May 17 10:44:41 2024

@author: SouravMukherjee
"""

def find_max_value_cluster(data):
  """
  Finds the cluster of non-zero values with the maximum value and returns the cluster and its index.

  Args:
      data: A list of integers.

  Returns:
      A tuple containing:
          - The cluster with the maximum value (list of integers).
          - The index of the cluster (starting position in the original data).
  """
  clusters = []
  current_cluster = []
  start_index = None
  for i, num in enumerate(data):
    if num != 0:
      if start_index is None:
        start_index = i
      current_cluster.append(num)
    elif current_cluster:
      clusters.append((start_index, current_cluster))
      start_index = None
      current_cluster = []
  if current_cluster:
    clusters.append((start_index, current_cluster))

  # Find cluster with maximum value
  max_value = float('-inf')  # Initialize with negative infinity
  max_cluster = None
  max_cluster_index = None
  for cluster_index, cluster in clusters:
    cluster_max = max(cluster)  # Find the maximum value within the cluster
    if cluster_max > max_value:
      max_value = cluster_max
      max_cluster = cluster
      max_cluster_index = cluster_index

  return max_cluster, max_cluster_index, cluster


import pandas as pd
import statistics
# dfp = pd.read_csv("C:/Users/souravmukherjee.USDA/Box/external EFR Study_Extreme Precip_DesignFlood/3rd Phase_Geomorphological Assessment/Data/WEPP/climate/gridmet_pinkham.csv")
# pr1hr = pd.read_table('C:/Users/souravmukherjee.USDA/Box/external EFR Study_Extreme Precip_DesignFlood/3rd Phase_Geomorphological Assessment/Data/WEPP/climate/15min_HBR_prcip',delimiter='\t',header=None)
# fac=4; unit=1
pr1hr = pd.read_table('C:/Users/souravmukherjee.USDA/Box/external EFR Study_Extreme Precip_DesignFlood/3rd Phase_Geomorphological Assessment/Data/WEPP/climate/1hr_HBR_prcip',delimiter='\t',header=None)
fac=1; unit=10 
# Sample data (replace with your actual DataFrame)
data = {
    'year': pr1hr[0],
    'month': pr1hr[1],
    'day': pr1hr[2],
    'hour': pr1hr[3],
    'precip': pr1hr[4]
}

df = pd.DataFrame(data)
    
# Calculate total daily precipitation depth
daily_precip = df.groupby(['year', 'month', 'day'])['precip'].sum().reset_index()
tp=[];ip=[];imax=[];imean=[];
for day,day_data in df.groupby(['year', 'month', 'day']):
    val= day_data['precip'].reset_index()
    # Check if total precipitation for the group is greater than 0
    if day_data['precip'].sum() > 0:
        max_index = val.precip.idxmax()
        #first_day_index = day_data.loc[(day_data['precip']>0)].index[0]
        max_cluster, max_cluster_start_index, cluster=find_max_value_cluster(val.precip)
        #ip.append(day_data['precip'].max()/day_data['precip'].mean())
        tp.append((max_index-max_cluster_start_index)/len(max_cluster))
        imax.append(max(cluster))
        imean.append(statistics.mean(cluster))
        ip.append(max(cluster)/statistics.mean(cluster))
    else:
        tp.append(0)
        ip.append(0)
        imean.append(0)
        imax.append(0)
    

daily_precip['tp']=tp
daily_precip['ip']=ip
daily_precip['imean']=imean
daily_precip['imax']=imax

# Calculate number of non-zero precip hours
non_zero_hours = df[df['precip'] > 0].groupby(['year', 'month', 'day'])['hour'].count()
nz =pd.DataFrame(non_zero_hours/fac)
daily_precip['dur']=0
# Merge them based on the date columns
merged_df = pd.merge(daily_precip, nz, on=['year', 'month', 'day'], how='outer')
merged_df['Dur'] = merged_df['dur'].fillna(0) + merged_df['hour'].fillna(0)
merged_df=merged_df.drop(['dur','hour','imax','imean'], axis=1)
merged_df['precip']=merged_df['precip']*unit
# merged_df = merged_df.reset_index()
filtered_df1 = merged_df.loc[(merged_df['year'] >= 1980) & (merged_df['year'] <= 2020)]
# filtered_df1.to_csv("C:/Users/souravmukherjee.USDA/Box/external EFR Study_Extreme Precip_DesignFlood/3rd Phase_Geomorphological Assessment/Data/WEPP/climate/daily_precip_dur_HBEF_1980_2020_using_15min_Data.csv")
filtered_df1.to_csv("C:/Users/souravmukherjee.USDA/Box/external EFR Study_Extreme Precip_DesignFlood/3rd Phase_Geomorphological Assessment/Data/WEPP/climate/daily_precip_dur_HBEF_1980_2020_using_1hr_Data.csv")



# ________________________________________________________________________________________________________________________________________________________________________________________________
# For the period 2021 - 2023
#dfp = pd.read_csv("C:/Users/souravmukherjee.USDA/Box/external EFR Study_Extreme Precip_DesignFlood/3rd Phase_Geomorphological Assessment/Data/WEPP/climate/gridmet_pinkham.csv")
pr15min = pd.read_table('C:/Users/souravmukherjee.USDA/Box/external EFR Study_Extreme Precip_DesignFlood/3rd Phase_Geomorphological Assessment/Data/WEPP/climate/HBEF_RG1precipitation_15min.csv',delimiter=',')
pr15min['DateTime'] = pd.to_datetime(pr15min['DateTime'])
fac=4;unit=1;
# Extract components
pr15min['year'] = pr15min['DateTime'].dt.year
pr15min['month'] = pr15min['DateTime'].dt.month
pr15min['day'] = pr15min['DateTime'].dt.day
pr15min['hour'] = pr15min['DateTime'].dt.hour
pr15min['minute'] = pr15min['DateTime'].dt.minute


df = pd.DataFrame(pr15min)
    
# Calculate total daily precipitation depth
daily_precip = df.groupby(['year', 'month', 'day'])['precip'].sum().reset_index()
tp=[];ip=[];imax=[];imean=[];
for day,day_data in df.groupby(['year', 'month', 'day']):
    val= day_data['precip'].reset_index()
    # Check if total precipitation for the group is greater than 0
    if day_data['precip'].sum() > 0:
        max_index = val.precip.idxmax()
        #first_day_index = day_data.loc[(day_data['precip']>0)].index[0]
        max_cluster, max_cluster_start_index, cluster=find_max_value_cluster(val.precip)
        #ip.append(day_data['precip'].max()/day_data['precip'].mean())
        tp.append((max_index-max_cluster_start_index)/len(max_cluster))
        imax.append(max(cluster))
        imean.append(statistics.mean(cluster))
        ip.append(max(cluster)/statistics.mean(cluster))
    else:
        tp.append(0)
        ip.append(0)
        imean.append(0)
        imax.append(0)
    

daily_precip['tp']=tp
daily_precip['ip']=ip
daily_precip['imean']=imean
daily_precip['imax']=imax

# Calculate number of non-zero precip hours
non_zero_hours = df[df['precip'] > 0].groupby(['year', 'month', 'day'])['hour'].count()
nz =pd.DataFrame(non_zero_hours/fac)
daily_precip['dur']=0
# Merge them based on the date columns
merged_df = pd.merge(daily_precip, nz, on=['year', 'month', 'day'], how='outer')
merged_df['Dur'] = merged_df['dur'].fillna(0) + merged_df['hour'].fillna(0)
merged_df=merged_df.drop(['dur','hour','imax','imean'], axis=1)
merged_df['precip']=merged_df['precip']*unit
# merged_df = merged_df.reset_index()
filtered_df2 = merged_df.loc[(merged_df['year'] >= 2021) & (merged_df['year'] <= 2023)]
filtered_df2.to_csv("C:/Users/souravmukherjee.USDA/Box/external EFR Study_Extreme Precip_DesignFlood/3rd Phase_Geomorphological Assessment/Data/WEPP/climate/daily_precip_dur_HBEF_2021_2023_using_15min_Data.csv")



########################################################################################################################################################################################################
df = pd.read_csv("C:/Users/souravmukherjee.USDA/Box/external EFR Study_Extreme Precip_DesignFlood/3rd Phase_Geomorphological Assessment/Data/WEPP/climate/use_this_hbref_gridmet.csv")

df.rename(columns={'da': 'day', 'mo': 'month'}, inplace=True)

# Create a datetime column from day, month, and year
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

# Group by month and calculate the mean for columns of interest
monthly_averages = df.groupby(df['date'].dt.month)[['prcp', 'tmax', 'tmin','rad']].mean()

# Rename the index to month names (optional)
monthly_averages.index = pd.to_datetime(monthly_averages.index, format='%m').strftime('%B')

print(monthly_averages)
