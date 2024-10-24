
#!/usr/bin/env python
# DataFrame utility functions via reading HTML including scraping web pages using bs4.
# Dave Babbitt <dave.babbitt@gmail.com>
# Author: Dave Babbitt, Data Scientist
# coding: utf-8

# Soli Deo gloria

"""
A set of utility functions specific to populating DataFrames from the web or hard drive
"""
from bs4 import BeautifulSoup as bs
from pathlib import Path
from scipy import stats
from urllib.request import urlretrieve
import io
import math
import matplotlib.pyplot as plt
import os
import pandas as pd
import random
import re
import seaborn as sns
import statsmodels.api as sm
import urllib

URL_REGEX = re.compile(r'\b(https?|file)://[-A-Z0-9+&@#/%?=~_|$!:,.;]*[A-Z0-9+&@#/%=~_|$]', re.IGNORECASE)
FILEPATH_REGEX = re.compile(r'\b[c-d]:\\(?:[^\\/:*?"<>|\x00-\x1F]{0,254}[^.\\/:*?"<>|\x00-\x1F]\\)*(?:[^\\/:*?"<>|\x00-\x1F]{0,254}[^.\\/:*?"<>|\x00-\x1F])', re.IGNORECASE)


def get_page_soup(page_url_or_filepath, verbose=True):
    match_obj = URL_REGEX.search(page_url_or_filepath)
    if match_obj:
        with urllib.request.urlopen(page_url_or_filepath) as response:
            page_html = response.read()
    else:
        with open(page_url_or_filepath, 'r', encoding='utf-8') as f:
            page_html = f.read()
    page_soup = bs(page_html, 'html.parser')
    
    return page_soup

def get_wiki_tables(tables_url_or_filepath, verbose=True):
    table_dfs_list = []
    try:
        table_dfs_list = get_page_tables(tables_url_or_filepath, verbose=verbose)
    except ValueError as e:
        if verbose:
            print(str(e).strip())
        page_soup = get_page_soup(tables_url_or_filepath, verbose=verbose)
        table_soups_list = page_soup.find_all('table', attrs={'class': 'wikitable'})
        table_dfs_list = []
        for table_soup in table_soups_list:
            table_dfs_list += get_page_tables(str(table_soup))
    
    return table_dfs_list

def get_page_tables(tables_url_or_filepath, verbose=True):
    '''
    %run ../../load_magic/dataframes.py
    tables_url = 'https://en.wikipedia.org/wiki/Provinces_of_Afghanistan'
    page_tables_list = get_page_tables(tables_url)
    '''
    if URL_REGEX.fullmatch(tables_url_or_filepath) or FILEPATH_REGEX.fullmatch(tables_url_or_filepath):
        tables_df_list = pd.read_html(tables_url_or_filepath)
    else:
        f = io.StringIO(tables_url_or_filepath)
        tables_df_list = pd.read_html(f)
    if verbose:
        print(sorted([(i, df.shape) for (i, df) in enumerate(tables_df_list)],
                     key=lambda x: x[1][0]*x[1][1], reverse=True))
    
    return tables_df_list


def get_column_descriptions(df, column_list=None):
    if column_list is None:
        column_list = df.columns
    
    # Use the strings of the dtypes to avoid unimplemented type errors
    g = df.columns.to_series().groupby(df.dtypes.map(lambda x: str(x))).groups
    
    rows_list = []
    for dtype, dtype_column_list in g.items():
        for column_name in dtype_column_list:
            if column_name in column_list:
                null_mask_series = df[column_name].isnull()
                blank_mask_series = df[column_name].map(lambda x: not len(str(x)))
                mask_series = null_mask_series | blank_mask_series
                
                # Get input row in dictionary format; key = col_name
                row_dict = {}
                row_dict['column_name'] = column_name
                row_dict['dtype'] = dtype
                row_dict['count_nulls'] = null_mask_series.sum()
                row_dict['count_blanks'] = blank_mask_series.sum()
                
                # Count how many unique numbers there are
                try:
                    row_dict['count_uniques'] = df[column_name].nunique()
                except Exception:
                    row_dict['count_uniques'] = math.nan
                
                # Count how many zeroes the column has
                try:
                    row_dict['count_zeroes'] = int((df[column_name] == 0).sum())
                except Exception:
                    row_dict['count_zeroes'] = math.nan
                
                # Check to see if the column has any dates
                date_series = pd.to_datetime(df[column_name], errors='coerce')
                null_series = date_series[~date_series.notnull()]
                row_dict['has_dates'] = (null_series.shape[0] < date_series.shape[0])
                
                # Show the minimum value in the column
                try:
                    row_dict['min_value'] = df[~mask_series][column_name].min()
                except Exception:
                    row_dict['min_value'] = math.nan
                
                # Show the maximum value in the column
                try:
                    row_dict['max_value'] = df[~mask_series][column_name].max()
                except Exception:
                    row_dict['max_value'] = math.nan
                
                # Show whether the column contains only integers
                try:
                    row_dict['only_integers'] = (df[column_name].apply(lambda x: float(x).is_integer())).all()
                except Exception:
                    row_dict['only_integers'] = float('nan')

                rows_list.append(row_dict)

    columns_list = ['column_name', 'dtype', 'count_nulls', 'count_blanks', 'count_uniques', 'count_zeroes', 'has_dates',
                    'min_value', 'max_value', 'only_integers']
    blank_ranking_df = pd.DataFrame(rows_list, columns=columns_list)
    
    return(blank_ranking_df)

def example_iterrows():
    '''
    rows_list = []
    columns_list = ['distance_from_white', 'distance_from_black', 'distance_from_red', 'distance_from_green', 'distance_from_blue',
                    'distance_from_magenta', 'distance_from_yellow', 'distance_from_cyan']
    index_list = []
    for row_index, row_series in student_df.iterrows():
        #print(row_index)
        
        # Get input row in dictionary format; key = col_name
        row_dict = {}
        index_list.append(row_index)
        
        for column_index, column_value in row_series.iteritems():
            #print(column_index, value)
            row_dict[column_index] = column_value
    
        rows_list.append(row_dict)

    event_grouping_df = pd.DataFrame(rows_list, columns=columns_list, index=index_list)
    event_grouping_df.sample(n=15).T.sample(n=5).T
    '''

    return "Don't run this, just look at the code using example_iterrows?"

def get_max_rsquared_adj(df, columns_list, verbose=False):
    if verbose:
        t0 = time.time()
    rows_list = []
    n = len(columns_list)
    for i in range(n-1):
        first_column = columns_list[i]
        first_series = df[first_column]
        max_similarity = 0.0
        max_column = first_column
        for j in range(i+1, n):
            second_column = columns_list[j]
            second_series = df[second_column]
            
            # Assume the first column is never identical to the second column
            X, y = first_series.values.reshape(-1, 1), second_series.values.reshape(-1, 1)
            #this_similarity = abs(first_series.cov(second_series))
            
            # Compute with statsmodels, by adding intercept manually
            X1 = sm.add_constant(X)
            result = sm.OLS(y, X1).fit()
            this_similarity = abs(result.rsquared_adj)
            
            if this_similarity > max_similarity:
                max_similarity = this_similarity
                max_column = second_column

        # Get input row in dictionary format; key = col_name
        row_dict = {}
        row_dict['first_column'] = first_column
        row_dict['second_column'] = max_column
        row_dict['max_similarity'] = max_similarity

        rows_list.append(row_dict)

    column_list = ['first_column', 'second_column', 'max_similarity']
    column_similarities_df = pd.DataFrame(rows_list, columns=column_list)
    if verbose:
        t1 = time.time()
        print(t1-t0, time.ctime(t1))

    return column_similarities_df

def clean_numerics(df, columns_list=None, verbose=False):
    if columns_list is None:
        columns_list = df.columns
    for cn in columns_list:
        df[cn] = df[cn].map(lambda x: re.sub(r'[^0-9\.]+', '', str(x)))
        df[cn] = pd.to_numeric(df[cn], errors='coerce', downcast='integer')
    
    return df