#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on Sun Mar  1 19:52:37 2026
# @author: amalmichael
# Week 7 Assignment
# Plot high speed internet adoption by county in USA
# data from https://www.fcc.gov/sites/default/files/county_tiers_201406_202406.zip
# shape file from https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2024&layergroup=Counties+%28and+equivalent%29


# %%
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
# %%

# 1. Load the FCC data
# Use latin1 encoding to handle special characters in county names
df = pd.read_csv('county_tiers_201406_202406.csv', encoding='latin1')
# %%


# 2. Filter for 2024 (June) and Clean FIPS
df_2024 = df[(df['Year'] == 2024) & (df['Month'] == 6)].copy()
df_2024['FIPS'] = df_2024['FIPS'].astype(str).str.zfill(5)
df_2024['Tier_4'] = df_2024['Tier_4'].replace(-999, 0) # Handle redacted data
# %%


# 3. Load County Shapefile (e.g., download from US Census TIGER)
# Path to your downloaded .shp file
counties = gpd.read_file('tl_2024_us_county.shp') 
# %%


# 4. Merge the data with the shapes
merged = counties.merge(df_2024, left_on='GEOID', right_on='FIPS')

# Filter for the Lower 48 States to remove the white space
# 02 = Alaska, 15 = Hawaii, 72 = Puerto Rico, 66 = Guam, etc.
excluded_states = ['02', '15', '72', '66', '60', '69', '78']
merged = merged[~merged['STATEFP'].isin(excluded_states)]
# -------------------------------

# %%

# 5. Plot the Mapfrom matplotlib.colors import ListedColormap

# 1. Define the custom blue gradient (White -> Light -> Dark)
# Tier 0=White, 1=Lightest Blue, 2, 3, 4, 5=Deepest Blue
custom_colors = [
    '#FFFFFF', # 0: 0% (Pure White)
    '#DEEBF7', # 1: 0-20% (Visible Light Blue)
    '#9ECAE1', # 2: 20-40%
    '#4292C6', # 3: 40-60%
    '#2171B5', # 4: 60-80%
    '#08306B'  # 5: 80%+ (Deep Navy)
]
custom_blue_cmap = ListedColormap(custom_colors)

# 2. Plot the Map
fig, ax = plt.subplots(1, 1, figsize=(15, 10))

# We use categorical=True because Tier_4 is discrete codes 0-5
merged.plot(column='Tier_4', 
            ax=ax, 
            legend=False,
            cmap=custom_blue_cmap,
            edgecolor='0.8',   # Light grey borders so white counties are visible
            linewidth=0.3,
            )

# 2. Create Custom Legend Patches (Equal Width Squares)
labels = ['0%', '0-20%', '20-40%', '40-60%', '60-80%', '80%+']
patches = []
for i, color in enumerate(custom_colors):
    patches.append(mpatches.Patch(color=color, label=labels[i], ec='0.8', lw=0.5))

# 3. Add the Expanded Legend to the axis
ax.legend(handles=patches, 
          title="Household Adoption Rate",
          title_fontproperties={'weight': 'bold', 'size': 14}, # Larger Title
          loc='lower center', 
          bbox_to_anchor=(0.5, -0.15), # Moves it slightly lower to avoid crowding
          ncol=6, 
          frameon=False,
          fontsize=12,             # Larger font for labels
          handlelength=2.5,        # Makes the color boxes wider
          handleheight=1.5,        # Makes the color boxes taller
          columnspacing=2.0)       # Spreads the legend items out across the page

# 4. Final Touches
ax.set_title('2024 U.S. County-Level High-Speed (100 Mbps) Adoption', 
             fontsize=18, fontweight='bold', pad=20)
ax.axis('off')
# Optional: Standard Albers Equal Area projection for a more professional look
fig.tight_layout()



# %%
# Save the image 
fig.savefig('broadband_geopandas_map.png')

