#!/usr/bin/env python
# coding: utf-8







# Soli Deo gloria







from urllib import request
import os
import random
import pandas as pd
import storage
s = storage.Storage()

# https://twitter.com/oudeicrat/status/1331560741862858753?s=20
def create_race_homicide_rate_by_state_year_dataframe():
    
    # Download from pastebin
    pastebin_url = 'https://pastebin.com/raw/Y33BcKv1'
    race_homicide_rate_by_state_year_df = s.load_object('race_homicide_rate_by_state_year_df', download_url=pastebin_url)
    
    # Move the column name header back to the first row
    race_homicide_rate_by_state_year_df = race_homicide_rate_by_state_year_df.T.reset_index().T.reset_index(drop=True)
    race_homicide_rate_by_state_year_df.columns = ['Year', 'State_Name', 'Perpetrator_Race', 'Homicide_Rate_Per_100_000']
    
    # Make the index a mult-index Year and State_Name
    race_homicide_rate_by_state_year_df = race_homicide_rate_by_state_year_df.set_index(['Year', 'State_Name'])
    
    # Fix the string added to the year index by the resetting
    arrays = [[int(idx) for idx in race_homicide_rate_by_state_year_df.index.get_level_values(0).tolist()],
              race_homicide_rate_by_state_year_df.index.get_level_values(1).tolist()]
    race_homicide_rate_by_state_year_df.index = pd.MultiIndex.from_arrays(arrays, names=('Year', 'State_Name'))
    
    return race_homicide_rate_by_state_year_df