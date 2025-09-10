# import pandas as pd

# def preprocess():
#     main = pd.read_csv("athlete_events.csv")
#     region = pd.read_csv("noc_regions.csv")

#     # filter only summer games
#     main = main[main['Season'] == 'Summer']

#     # clean region df
#     region = region.drop_duplicates(subset=['NOC'])

#     # drop old region if exists (safety)
#     if 'region' in main.columns:
#         main = main.drop(columns=['region'])

#     # merge fresh
#     main = main.merge(region[['NOC', 'region']], on='NOC', how='left')

#     # remove duplicates
#     main.drop_duplicates(inplace=True)

#     # remove old medal columns if they exist
#     if all(col in main.columns for col in ['Gold', 'Silver', 'Bronze']):
#         main = main.drop(columns=['Gold', 'Silver', 'Bronze'])

#     # one-hot-encoding for medals
#     main['Gold']   = (main['Medal'] == 'Gold').astype(int)
#     main['Silver'] = (main['Medal'] == 'Silver').astype(int)
#     main['Bronze'] = (main['Medal'] == 'Bronze').astype(int)

#     return main

import streamlit as st
import pandas as pd
@st.cache_data
def preprocess():
    main = pd.read_csv("athlete_events.csv")
    region = pd.read_csv("noc_regions.csv")

    main = main[main['Season'] == 'Summer']
    region = region.drop_duplicates(subset=['NOC'])
    
    if 'region' in main.columns:
        main = main.drop(columns=['region'])
        
    main = main.merge(region[['NOC','region']], on='NOC', how='left')
    main.drop_duplicates(inplace=True)

    # Medal columns as 0/1 integers
    main['Gold']   = (main['Medal'] == 'Gold').astype(int)
    main['Silver'] = (main['Medal'] == 'Silver').astype(int)
    main['Bronze'] = (main['Medal'] == 'Bronze').astype(int)

    return main
