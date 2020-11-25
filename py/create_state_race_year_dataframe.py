#!/usr/bin/env python
# coding: utf-8



from urllib import request
import os
import random
import pandas as pd

# From https://www.census.gov/data/tables/time-series/demo/popest/2010s-state-detail.html
def create_state_race_year_dataframe():
    
    # Set up the download URL dictionary
    format_str = 'http://www2.census.gov/programs-surveys/popest/tables/2010-2019/state/asrh/sc-est2019-sr11h-{}.xlsx'
    states_url_dict = {}
    states_url_dict['Alabama'] = '01'
    states_url_dict['Alaska'] = '02'
    states_url_dict['Arizona'] = '04'
    states_url_dict['Arkansas'] = '05'
    states_url_dict['California'] = '06'
    states_url_dict['Colorado'] = '08'
    states_url_dict['Connecticut'] = '09'
    states_url_dict['Delaware'] = '10'
    states_url_dict['District of Columbia'] = '11'
    states_url_dict['Florida'] = '12'
    states_url_dict['Georgia'] = '13'
    states_url_dict['Hawaii'] = '15'
    states_url_dict['Idaho'] = '16'
    states_url_dict['Illinois'] = '17'
    states_url_dict['Indiana'] = '18'
    states_url_dict['Iowa'] = '19'
    states_url_dict['Kansas'] = '20'
    states_url_dict['Kentucky'] = '21'
    states_url_dict['Louisiana'] = '22'
    states_url_dict['Maine'] = '23'
    states_url_dict['Maryland'] = '24'
    states_url_dict['Massachusetts'] = '25'
    states_url_dict['Michigan'] = '26'
    states_url_dict['Minnesota'] = '27'
    states_url_dict['Mississippi'] = '28'
    states_url_dict['Missouri'] = '29'
    states_url_dict['Montana'] = '30'
    states_url_dict['Nebraska'] = '31'
    states_url_dict['Nevada'] = '32'
    states_url_dict['New Hampshire'] = '33'
    states_url_dict['New Jersey'] = '34'
    states_url_dict['New Mexico'] = '35'
    states_url_dict['New York'] = '36'
    states_url_dict['North Carolina'] = '37'
    states_url_dict['North Dakota'] = '38'
    states_url_dict['Ohio'] = '39'
    states_url_dict['Oklahoma'] = '40'
    states_url_dict['Oregon'] = '41'
    states_url_dict['Pennsylvania'] = '42'
    states_url_dict['Rhode Island'] = '44'
    states_url_dict['South Carolina'] = '45'
    states_url_dict['South Dakota'] = '46'
    states_url_dict['Tennessee'] = '47'
    states_url_dict['Texas'] = '48'
    states_url_dict['Utah'] = '49'
    states_url_dict['Vermont'] = '50'
    states_url_dict['Virginia'] = '51'
    states_url_dict['Washington'] = '53'
    states_url_dict['West Virginia'] = '54'
    states_url_dict['Wisconsin'] = '55'
    states_url_dict['Wyoming'] = '56'
    
    # Download the Excel files
    xlxs_folder = os.path.join('../', 'data', 'xlsx')
    os.makedirs(name=xlxs_folder, exist_ok=True)
    for state_name, xlsx_num in states_url_dict.items():
        xlsx_url = format_str.format(xlsx_num)
        file_name = xlsx_url.split('/')[-1]
        file_path = os.path.join(xlxs_folder, file_name)
        if not os.path.isfile(file_path):
            try:
                request.urlretrieve(xlsx_url, file_path)
            except Exception as e:
                print(f'{file_name} is getting an error: {str(e).strip()}')
    
    # Initialize the returned dataframe
    columns_list = ['TOTAL_POPULATION', 'White', 'Black_or_African_American', 'American_Indian_and_Alaska_Native', 'Asian',
                    'Native_Hawaiian_and_Other_Pacific_Islander', 'Two_or_More_Races']
    added_columns_list = ['State_Name'] + columns_list
    state_race_year_df = pd.DataFrame([], columns=added_columns_list)
    
    # Loop through each state, concatonating its data to the returned dataframe
    states_list = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia',
                   'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
                   'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
                   'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
                   'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
                   'West Virginia', 'Wisconsin', 'Wyoming']
    for state_str in states_list:
        xlsx_num = states_url_dict[state_str]
        file_name = f'sc-est2019-sr11h-{xlsx_num}.xlsx'
        file_path = os.path.join(xlxs_folder, file_name)
        df = pd.read_excel(file_path).drop([0, 1]+list(range(11, 135)), axis='index')
        
        # Trim the floating points off some of the to-be-transposed Year names
        df.columns = [str(cn).split('.')[0] for cn in df.iloc[0].tolist()]
        
        # Get rid of the 2 index, and the nan column by making it the index, becoming the to-be-transposed column names
        df = df.drop([2], axis='index').set_index('nan').T
        
        # Clean up the now-transposed columns of their extraneous punctuation and convert spaces to underscores
        df.columns = [cn.replace('.', ' ').replace(':', ' ').strip().replace(' ', '_') for cn in df.columns.tolist()]
        
        # Introduce the state name column
        df['State_Name'] = state_str
        
        # Reorder and eliminate extraneous columns
        df = df[added_columns_list]
        
        # Concatonate the temporary dataframe with the returned dataframe
        state_race_year_df = pd.concat([state_race_year_df, df])
    
    # Rename the index column as Year and make the index a mult-index Year and State_Name
    state_race_year_df = state_race_year_df.reset_index().rename(columns={'index': 'Year'}).set_index(['Year', 'State_Name'])
    
    return state_race_year_df