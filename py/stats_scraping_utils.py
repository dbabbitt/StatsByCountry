
#!/usr/bin/env python
# Utility Functions to Scrape Websites.
# Dave Babbitt <dave.babbitt@gmail.com>
# Author: Dave Babbitt, Data Scientist
# coding: utf-8

# Soli Deo gloria

"""
StatsScrapingUtilities: A set of utility functions common to stats scraping
"""
import os
import pandas as pd
import urllib
import warnings
warnings.filterwarnings('ignore')

class StatsScrapingUtilities(object):
    """
    This class implements the core of the utility functions
    needed to scrape statistical content off web pages.
    
    Examples
    --------
    
    import sys
    
    # Insert at 1, 0 is the script path (or '' in REPL)
    sys.path.insert(1, '../py')
    
    from storage import Storage
    from stats_scraping_utils import StatsScrapingUtilities
    
    s = Storage()
    ssu = StatsScrapingUtilities(s=s)
    """
    
    def __init__(self, s=None, verbose=False):
        if s is None:
            from storage import Storage
            self.s = Storage()
        else:
            self.s = s
        
        # Obscuration error and url patterns
        import re
        self.obscure_regex = re.compile('<([^ ]+)[^>]*class="([^"]+)"[^>]*>')
        self.url_regex = re.compile(r'\b(https?|file)://[-A-Z0-9+&@#/%?=~_|$!:,.;]*[A-Z0-9+&@#/%=~_|$]', re.IGNORECASE)
        self.filepath_regex = re.compile(r'\b[c-d]:\\(?:[^\\/:*?"<>|\x00-\x1F]{0,254}[^.\\/:*?"<>|\x00-\x1F]\\)*(?:[^\\/:*?"<>|\x00-\x1F]{0,254}[^.\\/:*?"<>|\x00-\x1F])', re.IGNORECASE)
        
        # Renaming dictionaries, use it something like:
        # df.Country = df.Country.map(lambda x: ssu.country_name_dict.get(x, x))
        self.country_name_dict = {
            "Cote d'Ivoire": "Côte d'Ivoire",
            "Korea (Democratic People's Republic of)": 'North Korea',
            "Korea, Dem. People's Rep.": 'North Korea',
            "Lao People's Democratic Republic": 'Laos',
            'Antigua And Barbuda': 'Antigua & Barbuda',
            'Antigua and Barbuda': 'Antigua & Barbuda',
            'Bahamas, The': 'Bahamas',
            'Bolivia (Plurinational State of)': 'Bolivia',
            'Bonaire, Sint Eustatius And Saba': 'Bonaire, Sint Eustatius & Saba',
            'Bonaire, Sint Eustatius and Saba': 'Bonaire, Sint Eustatius & Saba',
            'Bosnia And Herzegovina': 'Bosnia & Herzegovina',
            'Bosnia and Herzegovina': 'Bosnia & Herzegovina',
            'Brunei Darussalam': 'Brunei',
            'Congo': 'ROC',
            'Congo, Dem. Rep.': 'DRC',
            'Congo, Democratic Republic of the': 'DRC',
            'Congo, Rep.': 'ROC',
            'Curacao': 'Curaçao',
            'Czech Republic': 'Czechia',
            'DR Congo': 'DRC',
            'Democratic Republic of Congo': 'DRC',
            'Democratic Republic of the Congo': 'DRC',
            'Egypt, Arab Republic': 'Egypt',
            'Gambia, The': 'Gambia',
            'Guinea Bissau': 'Guinea-Bissau',
            'Hong Kong SAR, China': 'Hong Kong',
            'Iran (Islamic Republic of)': 'Iran',
            'Korea, North': 'North Korea',
            'Korea, Rep.': 'South Korea',
            'Korea, Republic of': 'South Korea',
            'Korea, South': 'South Korea',
            'Macao SAR, China': 'Macau',
            'Macao': 'Macau',
            'Micronesia (Federated States of)': 'Federated States of Micronesia',
            'Moldova, Republic of': 'Moldova',
            'Palestine, State of': 'Palestine',
            'Republic of Congo': 'ROC',
            'Republic of the Congo': 'ROC',
            'Reunion': 'Réunion',
            'Russian Federation': 'Russia',
            'Saint Barthelemy': 'St. Barthélemy',
            'Saint Barthélemy': 'St. Barthélemy',
            'Saint Helena, Ascension And Tristan Da Cunha': 'St. Helena, Ascension & Tristan da Cunha',
            'Saint Helena, Ascension and Tristan da Cunha': 'St. Helena, Ascension & Tristan da Cunha',
            'Saint Kitts & Nevis': 'St. Kitts & Nevis',
            'Saint Kitts And Nevis': 'St. Kitts & Nevis',
            'Saint Kitts and Nevis': 'St. Kitts & Nevis',
            'Saint Lucia': 'St. Lucia',
            'Saint Martin (French part)': 'St. Martin',
            'Saint Martin': 'St. Martin',
            'Saint Pierre & Miquelon': 'St. Pierre & Miquelon',
            'Saint Pierre And Miquelon': 'St. Pierre & Miquelon',
            'Saint Pierre and Miquelon': 'St. Pierre & Miquelon',
            'Saint Vincent And the Grenadines': 'St. Vincent & Grenadines',
            'Saint Vincent and the Grenadines': 'St. Vincent & Grenadines',
            'Sao Tome & Principe': 'São Tomé & Príncipe',
            'Sao Tome And Principe': 'São Tomé & Príncipe',
            'Sao Tome and Principe': 'São Tomé & Príncipe',
            'Sint Maarten (Dutch part)': 'Sint Maarten',
            'Slovak Republic': 'Slovakia',
            'St. Kitts and Nevis': 'St. Kitts & Nevis',
            'St. Vincent and the Grenadines': 'St. Vincent & Grenadines',
            'Syrian Arab Republic': 'Syria',
            'São Tomé and Príncipe': 'São Tomé & Príncipe',
            'Taiwan, Province of China': 'Taiwan',
            'Tanzania, United Republic of': 'Tanzania',
            'Timor Leste': 'Timor-Leste',
            'Trinidad And Tobago': 'Trinidad & Tobago',
            'Trinidad and Tobago': 'Trinidad & Tobago',
            'Turkey': 'Turkiye',
            'Turks And Caicos Islands': 'Turks & Caicos Islands',
            'Turks and Caicos Islands': 'Turks & Caicos Islands',
            'U.S. Virgin Islands': 'US Virgin Islands',
            'United Arab Emirates': 'UAE',
            'United Kingdom of Great Britain and Northern Ireland': 'UK',
            'United Kingdom': 'UK',
            'United States Virgin Islands': 'US Virgin Islands',
            'United States of America': 'USA',
            'United States': 'USA',
            'Venezuela (Bolivarian Republic of)': 'Venezuela',
            'Viet Nam': 'Vietnam',
            'Virgin Islands (British)': 'British Virgin Islands',
            'Virgin Islands (U.S.)': 'US Virgin Islands',
            'Wallis And Futuna': 'Wallis & Futuna',
            'Wallis and Futuna': 'Wallis & Futuna',
            'Yemen, Rep.': 'Yemen',
        }
        
        # US States information
        self.us_states_list = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
                               'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia',
                               'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
                               'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
                               'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
                               'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota',
                               'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
                               'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia',
                               'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
        self.us_stats_df = self.s.load_object('us_stats_df')
        self.column_description_dict = self.s.load_object('column_description_dict')
        self.us_states_abbreviation_dict = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
                                            'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT',
                                            'Delaware': 'DE', 'District of Columbia': 'DC', 'Florida': 'FL',
                                            'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
                                            'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY',
                                            'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
                                            'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
                                            'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT',
                                            'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
                                            'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
                                            'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
                                            'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
                                            'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
                                            'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
                                            'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
                                            'Wisconsin': 'WI', 'Wyoming': 'WY', 'American Samoa': 'AS',
                                            'Guam': 'GU', 'Northern Mariana Islands': 'MP',
                                            'Puerto Rico': 'PR', 'Virgin Islands': 'VI'
                                           }
    
    
    
    
    def get_driver(self, browser_name='FireFox', verbose=True):
        if verbose:
            print('Getting the {} driver'.format(browser_name))
        log_dir = '../log'
        os.makedirs(name=log_dir, exist_ok=True)
        if browser_name == 'FireFox':
            executable_name = 'geckodriver'
        elif browser_name == 'Chrome':
            executable_name = 'chromedriver80'
        executable_path = '../../web-scrapers/exe/{}.exe'.format(executable_name)
        service_log_path = os.path.join(log_dir, '{}.log'.format(executable_name))
        from selenium import webdriver
        if browser_name == 'FireFox':
            fp = webdriver.FirefoxProfile()
            #fp.set_preference(key, value)
            driver = webdriver.Firefox(
                firefox_profile=fp,
                firefox_binary=None,
                capabilities=None,
                proxy=None,
                executable_path=executable_path,
                options=None,
                service_log_path=service_log_path,
                service_args=None,
                service=None,
                desired_capabilities=None,
                log_path=None,
                keep_alive=True
            )
        elif browser_name == 'Chrome':
            co = webdriver.ChromeOptions()
            co.add_argument('--no-sandbox')
            #co.set_capability(name, value)
            driver = webdriver.Chrome(
                chrome_options=None,
                executable_path=executable_path,
                keep_alive=True,
                options=co,
                port=0,
                service_log_path=service_log_path,
            )
        
        # Set timeout information and maximize
        driver.set_page_load_timeout(20)
        driver.maximize_window()
        
        return driver
    
    
    
    def wait_for(self, wait_count, verbose=True):
        if verbose:
            print('Waiting for {} seconds'.format(wait_count))
        import time
        time.sleep(wait_count)
    
    
    
    def driver_get_url(self, driver, url_str, verbose=True):
        if verbose:
            print('Getting URL: {}'.format(url_str))
        finished = 0
        fails = 0
        while (finished == 0) and (fails < 8):
            try:
                
                # Message: Timeout loading page after 100000ms
                driver.set_page_load_timeout(300)
                
                driver.get(url_str)
                finished = 1
            except Exception as e:
                message = str(e).strip()
                if verbose:
                    print(message)
                fails += 1
                
                # Wait for 10 seconds
                self.wait_for(10, verbose=verbose)
    
    
    
    def get_page_soup(self, url_or_filepath_or_html, driver=None, verbose=False):
        if self.url_regex.fullmatch(url_or_filepath_or_html):
            try:
                with urllib.request.urlopen(url_or_filepath_or_html) as response:
                    page_html = response.read()
            except:
                self.driver_get_url(driver, url_or_filepath_or_html, verbose=verbose)
                page_html = driver.page_source
        elif self.filepath_regex.fullmatch(os.path.abspath(url_or_filepath_or_html)):
            with open(url_or_filepath_or_html, 'r', encoding='utf-8') as f:
                page_html = f.read()
        else:
            page_html = url_or_filepath_or_html
        from bs4 import BeautifulSoup as bs
        page_soup = bs(page_html, 'html.parser')
        
        return page_soup
    
    
    
    def get_page_tables(self, url_or_filepath_or_html, driver=None, pdf_file_name=None, verbose=True):
        '''
        tables_url = 'https://en.wikipedia.org/wiki/Provinces_of_Afghanistan'
        page_tables_list = ssu.get_page_tables(tables_url)
        
        url = 'https://crashstats.nhtsa.dot.gov/Api/Public/Publication/812581'
        file_name = '2016_State_Traffic_Data_CrashStats_NHTSA.pdf'
        page_tables_list = ssu.get_page_tables(url, pdf_file_name=file_name)
        '''
        tables_df_list = []
        if pdf_file_name is not None:
            data_pdf_folder = os.path.join(self.s.data_folder, 'pdf')
            os.makedirs(name=data_pdf_folder, exist_ok=True)
            file_path = os.path.join(data_pdf_folder, pdf_file_name)
            import requests
            response = requests.get(url_or_filepath_or_html)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            import tabula
            tables_df_list = tabula.read_pdf(file_path, pages='all')
        elif self.url_regex.fullmatch(url_or_filepath_or_html) or self.filepath_regex.fullmatch(os.path.abspath(url_or_filepath_or_html)):
            from urllib.error import HTTPError
            try:
                tables_df_list = pd.read_html(url_or_filepath_or_html)
            except (ValueError, HTTPError) as e:
                if verbose: print(str(e).strip())
                page_soup = self.get_page_soup(url_or_filepath_or_html, driver=driver)
                table_soups_list = page_soup.find_all('table')
                for table_soup in table_soups_list:
                    tables_df_list += self.get_page_tables(str(table_soup), driver=None, verbose=False)
        else:
            import io
            f = io.StringIO(url_or_filepath_or_html)
            tables_df_list = pd.read_html(f)
        if verbose:
            print(sorted([(i, df.shape) for (i, df) in enumerate(tables_df_list)],
                         key=lambda x: x[1][0], reverse=True))
        
        return tables_df_list
    
    
    
    def get_column_descriptions(self, df, column_list=None):
        if column_list is None:
            column_list = df.columns
        groups_dict = df.columns.to_series().groupby(df.dtypes).groups
        rows_list = []
        for dtype, dtype_column_list in groups_dict.items():
            for column_name in dtype_column_list:
                if column_name in column_list:
                    null_mask_series = df[column_name].isnull()
                    blank_mask_series = df[column_name].map(lambda x: not len(str(x)))
                    mask_series = null_mask_series | blank_mask_series
                    
                    # Get input row in dictionary format; key = col_name
                    row_dict = {}
                    row_dict['column_name'] = column_name
                    row_dict['dtype'] = str(dtype)
                    row_dict['count_nulls'] = null_mask_series.sum()
                    row_dict['count_blanks'] = blank_mask_series.sum()
                    
                    # Count how many unique numbers there are
                    try:
                        row_dict['count_uniques'] = len(df[column_name].unique())
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
    
    
    
    def get_country_state_equivalents(self,
                                      countries_df, country_name_column, country_value_column,
                                      states_df, state_name_column, state_value_column,
                                      cn_col_explanation=None, st_col_explanation=None,
                                      countries_set=None, states_set=None, verbose=False):
        if countries_set is None:
            countries_set = set([cn for cn in countries_df[country_name_column] if str(cn) != 'nan'])
        
        # Check for duplicate country names
        mask_series = countries_df.duplicated(subset=[country_name_column], keep=False)
        assert countries_df[mask_series].shape[0] == 0, "You've duplicated some country names"
        
        mask_series = countries_df[country_name_column].isin(countries_set)
        country_tuples_list = [(r[country_name_column], r[country_value_column]) for i, r in countries_df[mask_series].iterrows()]
        
        if states_set is None:
            states_set = set([sn for sn in states_df[state_name_column] if str(sn) != 'nan'])
        
        # Check for duplicate state names
        mask_series = states_df.duplicated(subset=[state_name_column], keep=False)
        assert states_df[mask_series].shape[0] == 0, "You've duplicated some state names"
        
        mask_series = states_df[state_name_column].isin(states_set)
        state_tuples_list = [(r[state_name_column], r[state_value_column]) for i, r in states_df[mask_series].iterrows()]
        
        # Get country-to-state equivalence dictionary
        rows_list = []
        if verbose:
            if cn_col_explanation is None:
                cn_col_explanation = country_value_column.replace('_', ' ')
            print()
            explanations_list = []
        for country_tuple in country_tuples_list:
            candidate_tuple = sorted([s for s in state_tuples_list], key=lambda x: abs(x[1] - country_tuple[1]))[0]
            state_name = candidate_tuple[0]
            country_name = country_tuple[0]
            if verbose:
                explanations_list.append(f'{country_name} ({country_tuple[1]:.2f}) is close to the {cn_col_explanation} of {state_name} ({candidate_tuple[1]:.2f})')
            row_dict = {}
            row_dict['country_name'] = country_name
            row_dict['state_name'] = state_name
            rows_list.append(row_dict)
        c2s_equivalent_dict = pd.DataFrame(rows_list).set_index('country_name').state_name.to_dict()
        if verbose:
            for explanation in sorted(explanations_list):
                print(explanation.replace('.00)', ')'))

        
        # Get the state-to-country equivalence dictionary
        rows_list = []
        if verbose:
            if st_col_explanation is None:
                st_col_explanation = state_value_column.replace('_', ' ')
            print()
            explanations_list = []
        for state_tuple in state_tuples_list:
            candidate_tuple = sorted([s for s in country_tuples_list], key=lambda x: abs(x[1] - state_tuple[1]))[0]
            country_name = candidate_tuple[0]
            state_name = state_tuple[0]
            if verbose:
                explanations_list.append(f'{state_name} ({state_tuple[1]:,.2f}) is close to the {st_col_explanation} of {country_name} ({candidate_tuple[1]:,.2f})')
            row_dict = {}
            row_dict['state_name'] = state_name
            row_dict['country_name'] = country_name
            rows_list.append(row_dict)
        s2c_equivalent_dict = pd.DataFrame(rows_list).set_index('state_name').country_name.to_dict()
        if verbose:
            for explanation in sorted(explanations_list):
                print(explanation.replace('.00)', ')'))
        
        return s2c_equivalent_dict, c2s_equivalent_dict
    
    
    
    def get_similarity_measure(self, a, b):
        from difflib import SequenceMatcher
        
        return SequenceMatcher(None, str(a), str(b)).ratio()
    
    
    
    def check_4_doubles(self, item_list, verbose=False):
        '''
        countries_list = sorted(set(capitalism_gini_df.Country).symmetric_difference(set(corruption_df.Country)))
        doubles_df = ssu.check_4_doubles(countries_list)
        mask_series = (doubles_df.max_similarity > 0.6)
        columns_list = ['first_item', 'second_item', 'max_similarity']
        doubles_df[mask_series][columns_list].sort_values('max_similarity', ascending=False)
        '''
        if verbose:
            t0 = time.time()
        rows_list = []
        n = len(item_list)
        for i in range(n-1):
            first_item = item_list[i]
            max_similarity = 0.0
            max_item = first_item
            for j in range(i+1, n):
                second_item = item_list[j]

                # Assume the first item is never identical to the second item
                this_similarity = self.get_similarity_measure(str(first_item), str(second_item))
                
                if this_similarity > max_similarity:
                    max_similarity = this_similarity
                    max_item = second_item

            # Get input row in dictionary format; key = col_name
            row_dict = {}
            row_dict['first_item'] = first_item
            row_dict['second_item'] = max_item
            row_dict['first_bytes'] = '-'.join(str(x) for x in bytearray(str(first_item),
                                                                         encoding='utf-8', errors="replace"))
            row_dict['second_bytes'] = '-'.join(str(x) for x in bytearray(str(max_item),
                                                                          encoding='utf-8', errors="replace"))
            row_dict['max_similarity'] = max_similarity

            rows_list.append(row_dict)

        column_list = ['first_item', 'second_item', 'first_bytes', 'second_bytes', 'max_similarity']
        item_similarities_df = pd.DataFrame(rows_list, columns=column_list)
        if verbose:
            t1 = time.time()
            print(t1-t0, time.ctime(t1))

        return item_similarities_df
    
    
    
    def prepare_for_choroplething(self, countries_df, countries_target_column_name,
                                  us_states_df, st_col_name, st_col_explanation,
                                  equivalence_column_name, verbose=False):
        
        # Create the equivalence dictionaries
        s2c_dict, c2s_dict = self.get_country_state_equivalents(
            countries_df, 'country_name', countries_target_column_name,
            us_states_df, 'state_name', st_col_name,
            cn_col_explanation=None, st_col_explanation=st_col_explanation,
            countries_set=None, states_set=None, verbose=verbose)
        
        # Add the country equivalence column to the US stats dataframe
        self.us_stats_df[equivalence_column_name] = self.us_stats_df.index.map(lambda x: s2c_dict.get(x, x))
        
        # Add the numeric column to the US stats dataframe
        states_dict = us_states_df.set_index('state_name')[st_col_name].to_dict()
        states_min = us_states_df[st_col_name].min()
        self.us_stats_df[st_col_name] = self.us_stats_df.index.map(lambda x: states_dict.get(x, states_min))
        self.column_description_dict[st_col_name] = st_col_explanation
        self.s.store_objects(us_stats_df=self.us_stats_df, column_description_dict=self.column_description_dict)


      