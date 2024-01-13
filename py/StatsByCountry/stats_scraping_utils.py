
#!/usr/bin/env python
# Utility Functions to Scrape Websites.
# Dave Babbitt <dave.babbitt@gmail.com>
# Author: Dave Babbitt, Data Scientist
# coding: utf-8

# Soli Deo gloria

"""
StatsScrapingUtilities: A set of utility functions common to stats scraping
"""
from . import nu, cu
import os
import pandas as pd
import urllib
import warnings

warnings.filterwarnings('ignore')
class StatsScrapingUtilities(object):
    """
    This class implements the core of the utility functions
    needed to scrape statistical content off web pages.
    
    Example:
        import sys
        sys.path.insert(1, '../py')
        from stats_scraping_utils import StatsScrapingUtilities
        ssu = StatsScrapingUtilities()
    """
    
    def __init__(self, verbose=False):
        
        # Obscuration error and url patterns
        import re
        self.obscure_regex = re.compile('<([^ ]+)[^>]*class="([^"]+)"[^>]*>')
        
        # Renaming dictionaries, use it something like:
        # df.Country = df.Country.map(lambda x: ssu.country_name_dict.get(x, x))
        self.country_name_dict = {
            "Cote d'Ivoire": "Côte d'Ivoire",
            "Dem. People's Rep. Korea": 'North Korea',
            "Korea (Democratic People's Republic of)": 'North Korea',
            "Korea, Dem. People's Rep.": 'North Korea',
            "Lao People's Democratic Republic": 'Laos',
            "Slovak Socialist Republic'": 'Slovakia',
            'Algeria (French Colonial Empire, French Algeria → Algeria)': 'Algeria',
            'American Samoa (US)': 'American Samoa',
            'Angola (Portuguese Empire, Portuguese Angola → Angola)': 'Angola',
            'Antigua And Barbuda': 'Antigua & Barbuda',
            'Antigua and Barbuda (British Empire → Antigua and Barbuda)': 'Antigua & Barbuda',
            'Antigua and Barbuda': 'Antigua & Barbuda',
            'Armenian SSR (\xa0Soviet Union → Armenia )': 'Armenia',
            'Aruba (Netherlands)': 'Aruba',
            'Azerbaijan SSR (\xa0Soviet Union → Azerbaijan)': 'Azerbaijan',
            'Bahamas (British Empire → Bahamas)': 'Bahamas',
            'Bahamas, The': 'Bahamas',
            'Bahrain (British Empire → Bahrain)': 'Bahrain',
            'Bangladesh (Pakistan, East Pakistan → Bangladesh)': 'Bangladesh',
            'Barbados (British Empire → Barbados)': 'Barbados',
            'Belgian Congo (Belgian Colonial Empire, Belgian Congo → Congo-Léopoldville → Zaire → DR Congo)': 'DRC',
            'Bermuda (UK)': 'Bermuda',
            'Bolivia (Plurinational State of)': 'Bolivia',
            'Bonaire, Sint Eustatius And Saba': 'Bonaire, Sint Eustatius & Saba',
            'Bonaire, Sint Eustatius and Saba': 'Bonaire, Sint Eustatius & Saba',
            'Bosnia And Herzegovina': 'Bosnia & Herzegovina',
            'Bosnia and Herzegovina (\xa0Yugoslavia → Bosnia and Herzegovina)': 'Bosnia & Herzegovina',
            'Bosnia and Herzegovina': 'Bosnia & Herzegovina',
            'Botswana (British Empire, Bechuanaland Protectorate → Botswana)': 'Botswana',
            'Brunei (British Empire, British Protectorate → Brunei)': 'Brunei',
            'Brunei Darussalam': 'Brunei',
            'Burkina Faso (French Colonial Empire, French West Africa → Republic of Upper Volta → Burkina Faso)': 'Burkina Faso',
            'Burma (→ Myanmar)': 'Myanmar',
            'Burundi (Belgian overseas colonies, Ruanda-Urundi → United Nations trust territories → Burundi)': 'Burundi',
            'Byelorussian SSR (\xa0Soviet Union → Belarus)': 'Belarus',
            'Cambodia (French Colonial Empire, French Indochina, French Cambodia → Cambodia)': 'Cambodia',
            'Cameroon (United Nations Trust Territories, French Colonial Empire, French Equatorial Africa, French Cameroons → Cameroon)': 'Cameroon',
            'Cape Verde (Portuguese Empire, Portuguese Cape Verde → Cape Verde)': 'Cape Verde',
            'Cayman Islands (UK)': 'Cayman Islands',
            'Central African Republic (French Colonial Empire, French Equatorial Africa, Ubangi-Shari → Central African Republic)': 'CAR',
            'Chad (French Colonial Empire, French Equatorial Africa, French Chad → Chad)': 'Chad',
            'Channel Islands - (111) Guernsey (UK) and (112) Jersey (UK)': 'Channel Islands',
            'Channel Islands - (8) Guernsey (UK) and (9) Jersey (UK)': 'Channel Islands',
            'Comoros (French Colonial Empire → Comoros)': 'Comoros',
            'Congo (French Colonial Empire, French Congo, French Equatorial Africa → Congo)': 'Congo',
            'Congo': 'ROC',
            'Congo, Dem. Rep.': 'DRC',
            'Congo, Democratic Republic of the': 'DRC',
            'Congo, Rep.': 'ROC',
            'Curacao': 'Curaçao',
            'Curaçao (Netherlands)': 'Curaçao',
            'Cyprus (British Empire, British Cyprus → Cyprus)': 'Cyprus',
            'Czech Republic': 'Czechia',
            'Czech Socialist Republic': 'Czechia',
            'DR Congo': 'DRC',
            'Dahomey (French Colonial Empire, French West Africa → Dahomey → Benin)': 'Benin',
            'Dem. Rep. Congo': 'DRC',
            'Democratic Republic of Congo': 'DRC',
            'Democratic Republic of the Congo': 'DRC',
            'Djibouti (French Colonial Empire, French Somaliland → Djibouti)': 'Djibouti',
            'East Timor (Portuguese Empire, Portuguese Timor → East Timor)': 'East Timor',
            'Egypt, Arab Republic': 'Egypt',
            'Equatorial Guinea (Spanish Empire, Spanish Guinea → Equatorial Guinea)': 'Equatorial Guinea',
            'Eritrea (\xa0Ethiopia → Eritrea)': 'Eritrea',
            'Estonian SSR (\xa0Soviet Union → Estonia)': 'Estonia',
            'Falkland Islands (UK)': 'Falkland Islands',
            'Fiji (British Empire → Fiji)': 'Fiji',
            'French Guiana (French Colonial Empire → France)': 'French Guiana',
            'French Polynesia (France)': 'French Polynesia',
            'French Polynesia (French Colonial Empire → France)': 'French Polynesia',
            'Gabon (French Colonial Empire, French Congo, French Equatorial Africa → Gabon': 'Gabon',
            'Gambia (British Empire, Gambia Colony and Protectorate → Gambia)': 'Gambia',
            'Gambia, The': 'Gambia',
            'Georgian SSR (\xa0Soviet Union → Georgia)': 'Georgia',
            'Germany (\xa0West Germany and East Germany → Germany)': 'Germany',
            'Ghana (British Empire, Gold Coast (British colony) → Ghana)': 'Ghana',
            'Greenland (Denmark)': 'Greenland',
            'Grenada (British Empire → Grenada)': 'Grenada',
            'Guam (US)': 'Guam',
            'Guinea (French Colonial Empire, French West Africa, French Guinea → Guinea': 'Guinea',
            'Guinea Bissau': 'Guinea-Bissau',
            'Guinea-Bissau (Portuguese Empire, Portuguese Guinea → Guinea-Bissau)': 'Guinea-Bissau',
            'Guyana (British Empire → Guyana)': 'Guyana',
            'Heard Island and McDonald Islands': 'Heard Island & McDonald Islands',
            'Hong Kong (British Empire, Hong Kong colony → China, Special administrative regions of China)': 'Hong Kong',
            'Hong Kong (China)': 'Hong Kong',
            'Hong Kong SAR, China': 'Hong Kong',
            'Iran (Islamic Republic of)': 'Iran',
            'Ivory Coast (French Colonial Empire, French West Africa, French Ivory Coast → Ivory Coast': 'Ivory Coast',
            'Jamaica (British Empire, Colony of Jamaica → Jamaica)': 'Jamaica',
            'Kazakh SSR (\xa0Soviet Union → Kazakhstan)': 'Kazakhstan',
            'Kenya (British Empire, Kenya Colony → Kenya)': 'Kenya',
            'Kirghiz SSR (\xa0Soviet Union → Kyrgyzstan)': 'Kyrgyzstan',
            'Kiribati (British Empire, Gilbert and Ellice Islands → Kiribati)': 'Kiribati',
            'Korea, North': 'North Korea',
            'Korea, Rep.': 'South Korea',
            'Korea, Republic of': 'South Korea',
            'Korea, South': 'South Korea',
            'Kuwait (British Empire, British Protectorate → Kuwait)': 'Kuwait',
            'Kyrgyz Republic': 'Kyrgyzstan',
            'Lao PDR': 'Laos',
            'Laos (French Colonial Empire, French Indochina, French Laos → Laos)': 'Laos',
            'Latvian SSR (\xa0Soviet Union → Latvia)': 'Latvia',
            'Lesotho (British Empire → Lesotho)': 'Lesotho',
            'Lithuanian SSR (\xa0Soviet Union → Lithuania)': 'Lithuania',
            'Macao SAR, China': 'Macau',
            'Macao': 'Macau',
            'Macau (China)': 'Macau',
            'Macau (Portuguese Empire, Portuguese Macau → China, Special administrative regions of China)': 'Macau',
            'Madagascar (French Colonial Empire, French Madagascar → Madagascar)': 'Madagascar',
            'Malawi (British Empire, Federation of Rhodesia and Nyasaland, Nyasaland Protectorate → Malawi)': 'Malawi',
            'Malaysia (British Empire, British Malaya and British Borneo → Malaysia)': 'Malaysia',
            'Maldives (British Empire, British Protectorate → Maldives)': 'Maldives',
            'Mali (French Colonial Empire, French West Africa, French Sudan → Mali)': 'Mali',
            'Malta (British Empire → Malta)': 'Malta',
            'Mauritania (French Colonial Empire, French West Africa, French Mauritania → Mauritania': 'Mauritania',
            'Mauritius (British Empire → Mauritius)': 'Mauritius',
            'Micronesia (Federated States of)': 'Federated States of Micronesia',
            'Micronesia (Trust Territory of the Pacific Islands → Micronesia)': 'Micronesia',
            'Moldavian SSR (\xa0Soviet Union → Moldova)': 'Moldova',
            'Moldova, Republic of': 'Moldova',
            'Montenegro (\xa0Yugoslavia → Montenegro)': 'Montenegro',
            'Mozambique (Portuguese Empire, Portuguese Mozambique → Mozambique)': 'Mozambique',
            'New Hebrides (British and French Condominium → Vanuatu)': 'Vanuatu',
            'Niger (French Colonial Empire, French Niger → Niger)': 'Niger',
            'Northern Rhodesia (British Empire, Federation of Rhodesia and Nyasaland → Zambia)': 'Zambia',
            'Qatar (British Empire, British Protectorate → Qatar)': 'Qatar',
            'Russian SFSR (\xa0Soviet Union → Russia)': 'Russia',
            'Rwanda (Belgian overseas colonies, Ruanda-Urundi → United Nations trust territories → Rwanda)': 'Rwanda',
            'SR Croatia (\xa0Yugoslavia → Croatia)': 'Croatia',
            'SR Macedonia (\xa0Yugoslavia → North Macedonia)': 'North Macedonia',
            'SR Serbia (\xa0Yugoslavia → Serbia and Montenegro → Serbia)': 'Serbia',
            'SR Slovenia (\xa0Yugoslavia → Slovenia)': 'Slovenia',
            'Saint Lucia (British Empire, West Indies Federation → Saint Lucia)': 'St. Lucia',
            'Myanmar (Burma)': 'Myanmar',
            'New Caledonia (France)': 'New Caledonia',
            'New Caledonia (French colonial Empire → France)': 'New Caledonia',
            'Nigeria (British Empire, British Nigeria → Nigeria': 'Nigeria',
            'Palestine (Gaza Strip and West Bank)': 'Palestine',
            'Palestine, State of': 'Palestine',
            'Papua and New Guinea (United Nations trust territories → Papua New Guinea': 'Papua New Guinea',
            'Puerto Rico (US)': 'Puerto Rico',
            'Republic of China (Taiwan)': 'Taiwan',
            'Republic of Congo': 'ROC',
            'Saint Vincent and the Grenadines (British Empire → Saint Vincent and the Grenadines)': 'St. Vincent & Grenadines',
            'Samoa (United Nations trust territories, Western Samoa → Samoa)': 'Samoa',
            'Senegal (French Colonial Empire, French West Africa, French Senegal → Senegal)': 'Senegal',
            'Sierra Leone (British Empire → Sierra Leone)': 'Sierra Leone',
            'Singapore (British Empire, British Singapore → Singapore)': 'Singapore',
            'Republic of the Congo': 'ROC',
            'Reunion': 'Réunion',
            'Russian Federation': 'Russia',
            'Saint Barthelemy': 'St. Barthélemy',
            'Saint Barthélemy': 'St. Barthélemy',
            'Saint Helena, Ascension & Tristan da Cunha': 'St. Helena, Ascension & Tristan da Cunha',
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
            'Solomon Islands (British Empire → Solomon Islands)': 'Solomon Islands',
            'Somalia (British Empire, British Somaliland and Trust Territory of Somaliland → Somalia)': 'Somalia',
            'South Sudan (British Empire, Anglo-Egyptian Sudan → Sudan → South Sudan)': 'South Sudan',
            'South West Africa (\xa0South Africa → Namibia)': 'Namibia',
            'Southern Rhodesia (British Empire, Federation of Rhodesia and Nyasaland → Zimbabwe)': 'Zimbabwe',
            'Sudan (British Empire, Anglo-Egyptian Sudan → Sudan)': 'Sudan',
            'Suriname (Kingdom of the Netherlands → Suriname)': 'Suriname',
            'Swaziland (British Empire → Swaziland)': 'Swaziland',
            'São Tomé and Príncipe (Portuguese Empire, Portuguese Sao Tome and Principe → São Tomé and Príncipe)': 'São Tomé & Príncipe',
            'Tajik SSR (\xa0Soviet Union → Tajikistan)': 'Tajikistan',
            'Tanzania (British Empire, Tanganyika and Zanzibar → Tanzania)': 'Tanzania',
            'Togo (United Nations trust territories, French Colonial Empire, French West Africa, French Togoland → Togo)': 'Togo',
            'Tonga (British Empire, British Protectorate → Tonga)': 'Tonga',
            'South Georgia and the South Sandwich Islands': 'South Georgia & the South Sandwich Islands',
            'São Tomé and Principe': 'São Tomé & Príncipe',
            'St. Kitts and Nevis': 'St. Kitts & Nevis',
            'St. Vincent and the Grenadines': 'St. Vincent & Grenadines',
            'Svalbard and Jan Mayen': 'Svalbard & Jan Mayen',
            'Syrian Arab Republic': 'Syria',
            'São Tomé and Príncipe': 'São Tomé & Príncipe',
            'Taiwan, Province of China': 'Taiwan',
            'Tanzania, United Republic of': 'Tanzania',
            'The Gambia': 'Gambia',
            'Timor Leste': 'Timor-Leste',
            'Trinidad and Tobago (British Empire, West Indies Federation → Trinidad and Tobago)': 'Trinidad & Tobago',
            'Tunisia (French Colonial Empire, French protectorate of Tunisia → Tunisia)': 'Tunisia',
            'Turkmen SSR (\xa0Soviet Union → Turkmenistan)': 'Turkmenistan',
            'Uganda (British Empire → Uganda)': 'Uganda',
            'Trinidad And Tobago': 'Trinidad & Tobago',
            'Trinidad and Tobago': 'Trinidad & Tobago',
            'Turkey': 'Turkiye',
            'Turks And Caicos Islands': 'Turks & Caicos Islands',
            'Turks and Caicos Islands': 'Turks & Caicos Islands',
            'U.S. Virgin Islands (US)': 'US Virgin Islands',
            'U.S. Virgin Islands': 'US Virgin Islands',
            'Ukrainian SSR (\xa0Soviet Union → Ukraine)': 'Ukraine',
            'Uzbek SSR (\xa0Soviet Union → Uzbekistan)': 'Uzbekistan',
            'United Arab Emirates (British Empire, Trucial States → United Arab Emirates)': 'UAE',
            'United Arab Emirates': 'UAE',
            'United Kingdom of Great Britain and Northern Ireland': 'UK',
            'United Kingdom': 'UK',
            'United States Virgin Islands': 'US Virgin Islands',
            'United States of America': 'USA',
            'United States': 'USA',
            'Venezuela (Bolivarian Republic of)': 'Venezuela',
            'Venezuela, RB': 'Venezuela',
            'Viet Nam': 'Vietnam',
            'Vietnam (French Colonial Empire, French Indochina, French Vietnam → North Vietnam and South Vietnam → Vietnam)': 'Vietnam',
            'Virgin Islands (British)': 'British Virgin Islands',
            'Virgin Islands (U.S.)': 'US Virgin Islands',
            'Wallis And Futuna': 'Wallis & Futuna',
            'Wallis and Futuna': 'Wallis & Futuna',
            'Yemen (\xa0North Yemen and South Yemen → Yemen)': 'Yemen',
            'Yemen, Rep.': 'Yemen',
        }
        self.oecd_countries_list = [
            'Austria', 'Australia', 'Belgium', 'Canada', 'Chile',
            'Colombia', 'Costa Rica', 'Czechia', 'Denmark',
            'Estonia', 'Finland', 'France', 'Germany', 'Greece',
            'Hungary', 'Iceland', 'Ireland', 'Israel', 'Italy',
            'Japan', 'Korea', 'Latvia', 'Lithuania', 'Luxembourg',
            'Mexico', 'Netherlands', 'New Zealand', 'Norway',
            'Poland', 'Portugal', 'Slovakia', 'Slovenia', 'Spain',
            'Sweden', 'Switzerland', 'Turkiye', 'UK', 'USA'
        ]
        
        # These countries cause redditors to make hurtful comments *sniff*
        self.derisable_countries_list = [
            'Channel Islands', 'Falkland Islands', 'Guernsey',
            'Hong Kong', 'Jersey', 'Macau', 'Puerto Rico'
        ]

        # ISO 3166-1 alpha-3 dictionaries
        self.alpha3_to_country_dict = {
            'ABW': 'Aruba',
            'AFG': 'Afghanistan',
            'AGO': 'Angola',
            'AIA': 'Anguilla',
            'ALA': 'Åland Islands',
            'ALB': 'Albania',
            'AND': 'Andorra',
            'ARE': 'United Arab Emirates',
            'ARG': 'Argentina',
            'ARM': 'Armenia',
            'ASM': 'American Samoa',
            'ATA': 'Antarctica',
            'ATF': 'French Southern Territories',
            'ATG': 'Antigua and Barbuda',
            'AUS': 'Australia',
            'AUT': 'Austria',
            'AZE': 'Azerbaijan',
            'BDI': 'Burundi',
            'BEL': 'Belgium',
            'BEN': 'Benin',
            'BES': 'Bonaire, Sint Eustatius and Saba',
            'BFA': 'Burkina Faso',
            'BGD': 'Bangladesh',
            'BGR': 'Bulgaria',
            'BHR': 'Bahrain',
            'BHS': 'Bahamas',
            'BIH': 'Bosnia and Herzegovina',
            'BLM': 'Saint Barthélemy',
            'BLR': 'Belarus',
            'BLZ': 'Belize',
            'BMU': 'Bermuda',
            'BOL': 'Bolivia (Plurinational State of)',
            'BRA': 'Brazil',
            'BRB': 'Barbados',
            'BRN': 'Brunei Darussalam',
            'BTN': 'Bhutan',
            'BVT': 'Bouvet Island',
            'BWA': 'Botswana',
            'CAF': 'Central African Republic',
            'CAN': 'Canada',
            'CCK': 'Cocos (Keeling) Islands',
            'CHE': 'Switzerland',
            'CHL': 'Chile',
            'CHN': 'China',
            'CIV': "Côte d'Ivoire",
            'CMR': 'Cameroon',
            'COD': 'Congo, Democratic Republic of the',
            'COG': 'Congo',
            'COK': 'Cook Islands',
            'COL': 'Colombia',
            'COM': 'Comoros',
            'CPV': 'Cabo Verde',
            'CRI': 'Costa Rica',
            'CUB': 'Cuba',
            'CUW': 'Curaçao',
            'CXR': 'Christmas Island',
            'CYM': 'Cayman Islands',
            'CYP': 'Cyprus',
            'CZE': 'Czechia',
            'DEU': 'Germany',
            'DJI': 'Djibouti',
            'DMA': 'Dominica',
            'DNK': 'Denmark',
            'DOM': 'Dominican Republic',
            'DZA': 'Algeria',
            'ECU': 'Ecuador',
            'EGY': 'Egypt',
            'ERI': 'Eritrea',
            'ESH': 'Western Sahara',
            'ESP': 'Spain',
            'EST': 'Estonia',
            'ETH': 'Ethiopia',
            'FIN': 'Finland',
            'FJI': 'Fiji',
            'FLK': 'Falkland Islands (Malvinas)',
            'FRA': 'France',
            'FRO': 'Faroe Islands',
            'FSM': 'Micronesia (Federated States of)',
            'GAB': 'Gabon',
            'GBR': 'United Kingdom of Great Britain and Northern Ireland',
            'GEO': 'Georgia',
            'GGY': 'Guernsey',
            'GHA': 'Ghana',
            'GIB': 'Gibraltar',
            'GIN': 'Guinea',
            'GLP': 'Guadeloupe',
            'GMB': 'Gambia',
            'GNB': 'Guinea-Bissau',
            'GNQ': 'Equatorial Guinea',
            'GRC': 'Greece',
            'GRD': 'Grenada',
            'GRL': 'Greenland',
            'GTM': 'Guatemala',
            'GUF': 'French Guiana',
            'GUM': 'Guam',
            'GUY': 'Guyana',
            'HKG': 'Hong Kong',
            'HMD': 'Heard Island and McDonald Islands',
            'HND': 'Honduras',
            'HRV': 'Croatia',
            'HTI': 'Haiti',
            'HUN': 'Hungary',
            'IDN': 'Indonesia',
            'IMN': 'Isle of Man',
            'IND': 'India',
            'IOT': 'British Indian Ocean Territory',
            'IRL': 'Ireland',
            'IRN': 'Iran (Islamic Republic of)',
            'IRQ': 'Iraq',
            'ISL': 'Iceland',
            'ISR': 'Israel',
            'ITA': 'Italy',
            'JAM': 'Jamaica',
            'JEY': 'Jersey',
            'JOR': 'Jordan',
            'JPN': 'Japan',
            'KAZ': 'Kazakhstan',
            'KEN': 'Kenya',
            'KGZ': 'Kyrgyzstan',
            'KHM': 'Cambodia',
            'KIR': 'Kiribati',
            'KNA': 'Saint Kitts and Nevis',
            'KOR': 'Korea, Republic of',
            'KWT': 'Kuwait',
            'LAO': "Lao People's Democratic Republic",
            'LBN': 'Lebanon',
            'LBR': 'Liberia',
            'LBY': 'Libya',
            'LCA': 'Saint Lucia',
            'LIE': 'Liechtenstein',
            'LKA': 'Sri Lanka',
            'LSO': 'Lesotho',
            'LTU': 'Lithuania',
            'LUX': 'Luxembourg',
            'LVA': 'Latvia',
            'MAC': 'Macao',
            'MAF': 'Saint Martin (French part)',
            'MAR': 'Morocco',
            'MCO': 'Monaco',
            'MDA': 'Moldova, Republic of',
            'MDG': 'Madagascar',
            'MDV': 'Maldives',
            'MEX': 'Mexico',
            'MHL': 'Marshall Islands',
            'MKD': 'North Macedonia',
            'MLI': 'Mali',
            'MLT': 'Malta',
            'MMR': 'Myanmar',
            'MNE': 'Montenegro',
            'MNG': 'Mongolia',
            'MNP': 'Northern Mariana Islands',
            'MOZ': 'Mozambique',
            'MRT': 'Mauritania',
            'MSR': 'Montserrat',
            'MTQ': 'Martinique',
            'MUS': 'Mauritius',
            'MWI': 'Malawi',
            'MYS': 'Malaysia',
            'MYT': 'Mayotte',
            'NAM': 'Namibia',
            'NCL': 'New Caledonia',
            'NER': 'Niger',
            'NFK': 'Norfolk Island',
            'NGA': 'Nigeria',
            'NIC': 'Nicaragua',
            'NIU': 'Niue',
            'NLD': 'Netherlands, Kingdom of the',
            'NOR': 'Norway',
            'NPL': 'Nepal',
            'NRU': 'Nauru',
            'NZL': 'New Zealand',
            'OMN': 'Oman',
            'PAK': 'Pakistan',
            'PAN': 'Panama',
            'PCN': 'Pitcairn',
            'PER': 'Peru',
            'PHL': 'Philippines',
            'PLW': 'Palau',
            'PNG': 'Papua New Guinea',
            'POL': 'Poland',
            'PRI': 'Puerto Rico',
            'PRK': "Korea (Democratic People's Republic of)",
            'PRT': 'Portugal',
            'PRY': 'Paraguay',
            'PSE': 'Palestine, State of',
            'PYF': 'French Polynesia',
            'QAT': 'Qatar',
            'REU': 'Réunion',
            'ROU': 'Romania',
            'RUS': 'Russian Federation',
            'RWA': 'Rwanda',
            'SAU': 'Saudi Arabia',
            'SDN': 'Sudan',
            'SEN': 'Senegal',
            'SGP': 'Singapore',
            'SGS': 'South Georgia and the South Sandwich Islands',
            'SHN': 'Saint Helena, Ascension and Tristan da Cunha',
            'SJM': 'Svalbard and Jan Mayen',
            'SLB': 'Solomon Islands',
            'SLE': 'Sierra Leone',
            'SLV': 'El Salvador',
            'SMR': 'San Marino',
            'SOM': 'Somalia',
            'SPM': 'Saint Pierre and Miquelon',
            'SRB': 'Serbia',
            'SSD': 'South Sudan',
            'STP': 'Sao Tome and Principe',
            'SUR': 'Suriname',
            'SVK': 'Slovakia',
            'SVN': 'Slovenia',
            'SWE': 'Sweden',
            'SWZ': 'Eswatini',
            'SXM': 'Sint Maarten (Dutch part)',
            'SYC': 'Seychelles',
            'SYR': 'Syrian Arab Republic',
            'TCA': 'Turks and Caicos Islands',
            'TCD': 'Chad',
            'TGO': 'Togo',
            'THA': 'Thailand',
            'TJK': 'Tajikistan',
            'TKL': 'Tokelau',
            'TKM': 'Turkmenistan',
            'TLS': 'Timor-Leste',
            'TON': 'Tonga',
            'TTO': 'Trinidad and Tobago',
            'TUN': 'Tunisia',
            'TUR': 'Türkiye',
            'TUV': 'Tuvalu',
            'TWN': 'Province of China',
            'TZA': 'Tanzania, United Republic of',
            'UGA': 'Uganda',
            'UKR': 'Ukraine',
            'UMI': 'United States Minor Outlying Islands',
            'URY': 'Uruguay',
            'USA': 'United States of America',
            'UZB': 'Uzbekistan',
            'VAT': 'Holy See',
            'VCT': 'Saint Vincent and the Grenadines',
            'VEN': 'Venezuela (Bolivarian Republic of)',
            'VGB': 'Virgin Islands (British)',
            'VIR': 'Virgin Islands (U.S.)',
            'VNM': 'Viet Nam',
            'VUT': 'Vanuatu',
            'WLF': 'Wallis and Futuna',
            'WSM': 'Samoa',
            'YEM': 'Yemen',
            'ZAF': 'South Africa',
            'ZMB': 'Zambia',
            'ZWE': 'Zimbabwe'
        }
        self.country_to_alpha3_dict = {
            'Aruba': 'ABW',
            'Afghanistan': 'AFG',
            'Angola': 'AGO',
            'Anguilla': 'AIA',
            'Åland Islands': 'ALA',
            'Albania': 'ALB',
            'Andorra': 'AND',
            'United Arab Emirates': 'ARE',
            'Argentina': 'ARG',
            'Armenia': 'ARM',
            'American Samoa': 'ASM',
            'Antarctica': 'ATA',
            'French Southern Territories': 'ATF',
            'Antigua and Barbuda': 'ATG',
            'Australia': 'AUS',
            'Austria': 'AUT',
            'Azerbaijan': 'AZE',
            'Burundi': 'BDI',
            'Belgium': 'BEL',
            'Benin': 'BEN',
            'Bonaire, Sint Eustatius and Saba': 'BES',
            'Burkina Faso': 'BFA',
            'Bangladesh': 'BGD',
            'Bulgaria': 'BGR',
            'Bahrain': 'BHR',
            'Bahamas': 'BHS',
            'Bosnia and Herzegovina': 'BIH',
            'Saint Barthélemy': 'BLM',
            'Belarus': 'BLR',
            'Belize': 'BLZ',
            'Bermuda': 'BMU',
            'Bolivia (Plurinational State of)': 'BOL',
            'Brazil': 'BRA',
            'Barbados': 'BRB',
            'Brunei Darussalam': 'BRN',
            'Bhutan': 'BTN',
            'Bouvet Island': 'BVT',
            'Botswana': 'BWA',
            'Central African Republic': 'CAF',
            'Canada': 'CAN',
            'Cocos (Keeling) Islands': 'CCK',
            'Switzerland': 'CHE',
            'Chile': 'CHL',
            'China': 'CHN',
            "Côte d'Ivoire": 'CIV',
            'Cameroon': 'CMR',
            'Congo, Democratic Republic of the': 'COD',
            'Congo': 'COG',
            'Cook Islands': 'COK',
            'Colombia': 'COL',
            'Comoros': 'COM',
            'Cabo Verde': 'CPV',
            'Costa Rica': 'CRI',
            'Cuba': 'CUB',
            'Curaçao': 'CUW',
            'Christmas Island': 'CXR',
            'Cayman Islands': 'CYM',
            'Cyprus': 'CYP',
            'Czechia': 'CZE',
            'Germany': 'DEU',
            'Djibouti': 'DJI',
            'Dominica': 'DMA',
            'Denmark': 'DNK',
            'Dominican Republic': 'DOM',
            'Algeria': 'DZA',
            'Ecuador': 'ECU',
            'Egypt': 'EGY',
            'Eritrea': 'ERI',
            'Western Sahara': 'ESH',
            'Spain': 'ESP',
            'Estonia': 'EST',
            'Ethiopia': 'ETH',
            'Finland': 'FIN',
            'Fiji': 'FJI',
            'Falkland Islands (Malvinas)': 'FLK',
            'France': 'FRA',
            'Faroe Islands': 'FRO',
            'Micronesia (Federated States of)': 'FSM',
            'Gabon': 'GAB',
            'United Kingdom of Great Britain and Northern Ireland': 'GBR',
            'Georgia': 'GEO',
            'Guernsey': 'GGY',
            'Ghana': 'GHA',
            'Gibraltar': 'GIB',
            'Guinea': 'GIN',
            'Guadeloupe': 'GLP',
            'Gambia': 'GMB',
            'Guinea-Bissau': 'GNB',
            'Equatorial Guinea': 'GNQ',
            'Greece': 'GRC',
            'Grenada': 'GRD',
            'Greenland': 'GRL',
            'Guatemala': 'GTM',
            'French Guiana': 'GUF',
            'Guam': 'GUM',
            'Guyana': 'GUY',
            'Hong Kong': 'HKG',
            'Heard Island and McDonald Islands': 'HMD',
            'Honduras': 'HND',
            'Croatia': 'HRV',
            'Haiti': 'HTI',
            'Hungary': 'HUN',
            'Indonesia': 'IDN',
            'Isle of Man': 'IMN',
            'India': 'IND',
            'British Indian Ocean Territory': 'IOT',
            'Ireland': 'IRL',
            'Iran (Islamic Republic of)': 'IRN',
            'Iraq': 'IRQ',
            'Iceland': 'ISL',
            'Israel': 'ISR',
            'Italy': 'ITA',
            'Jamaica': 'JAM',
            'Jersey': 'JEY',
            'Jordan': 'JOR',
            'Japan': 'JPN',
            'Kazakhstan': 'KAZ',
            'Kenya': 'KEN',
            'Kyrgyzstan': 'KGZ',
            'Cambodia': 'KHM',
            'Kiribati': 'KIR',
            'Saint Kitts and Nevis': 'KNA',
            'Korea, Republic of': 'KOR',
            'Kuwait': 'KWT',
            "Lao People's Democratic Republic": 'LAO',
            'Lebanon': 'LBN',
            'Liberia': 'LBR',
            'Libya': 'LBY',
            'Saint Lucia': 'LCA',
            'Liechtenstein': 'LIE',
            'Sri Lanka': 'LKA',
            'Lesotho': 'LSO',
            'Lithuania': 'LTU',
            'Luxembourg': 'LUX',
            'Latvia': 'LVA',
            'Macao': 'MAC',
            'Saint Martin (French part)': 'MAF',
            'Morocco': 'MAR',
            'Monaco': 'MCO',
            'Moldova, Republic of': 'MDA',
            'Madagascar': 'MDG',
            'Maldives': 'MDV',
            'Mexico': 'MEX',
            'Marshall Islands': 'MHL',
            'North Macedonia': 'MKD',
            'Mali': 'MLI',
            'Malta': 'MLT',
            'Myanmar': 'MMR',
            'Montenegro': 'MNE',
            'Mongolia': 'MNG',
            'Northern Mariana Islands': 'MNP',
            'Mozambique': 'MOZ',
            'Mauritania': 'MRT',
            'Montserrat': 'MSR',
            'Martinique': 'MTQ',
            'Mauritius': 'MUS',
            'Malawi': 'MWI',
            'Malaysia': 'MYS',
            'Mayotte': 'MYT',
            'Namibia': 'NAM',
            'New Caledonia': 'NCL',
            'Niger': 'NER',
            'Norfolk Island': 'NFK',
            'Nigeria': 'NGA',
            'Nicaragua': 'NIC',
            'Niue': 'NIU',
            'Netherlands, Kingdom of the': 'NLD',
            'Norway': 'NOR',
            'Nepal': 'NPL',
            'Nauru': 'NRU',
            'New Zealand': 'NZL',
            'Oman': 'OMN',
            'Pakistan': 'PAK',
            'Panama': 'PAN',
            'Pitcairn': 'PCN',
            'Peru': 'PER',
            'Philippines': 'PHL',
            'Palau': 'PLW',
            'Papua New Guinea': 'PNG',
            'Poland': 'POL',
            'Puerto Rico': 'PRI',
            "Korea (Democratic People's Republic of)": 'PRK',
            'Portugal': 'PRT',
            'Paraguay': 'PRY',
            'Palestine, State of': 'PSE',
            'French Polynesia': 'PYF',
            'Qatar': 'QAT',
            'Réunion': 'REU',
            'Romania': 'ROU',
            'Russian Federation': 'RUS',
            'Rwanda': 'RWA',
            'Saudi Arabia': 'SAU',
            'Sudan': 'SDN',
            'Senegal': 'SEN',
            'Singapore': 'SGP',
            'South Georgia and the South Sandwich Islands': 'SGS',
            'Saint Helena, Ascension and Tristan da Cunha': 'SHN',
            'Svalbard and Jan Mayen': 'SJM',
            'Solomon Islands': 'SLB',
            'Sierra Leone': 'SLE',
            'El Salvador': 'SLV',
            'San Marino': 'SMR',
            'Somalia': 'SOM',
            'Saint Pierre and Miquelon': 'SPM',
            'Serbia': 'SRB',
            'South Sudan': 'SSD',
            'Sao Tome and Principe': 'STP',
            'Suriname': 'SUR',
            'Slovakia': 'SVK',
            'Slovenia': 'SVN',
            'Sweden': 'SWE',
            'Eswatini': 'SWZ',
            'Sint Maarten (Dutch part)': 'SXM',
            'Seychelles': 'SYC',
            'Syrian Arab Republic': 'SYR',
            'Turks and Caicos Islands': 'TCA',
            'Chad': 'TCD',
            'Togo': 'TGO',
            'Thailand': 'THA',
            'Tajikistan': 'TJK',
            'Tokelau': 'TKL',
            'Turkmenistan': 'TKM',
            'Timor-Leste': 'TLS',
            'Tonga': 'TON',
            'Trinidad and Tobago': 'TTO',
            'Tunisia': 'TUN',
            'Türkiye': 'TUR',
            'Tuvalu': 'TUV',
            'Province of China': 'TWN',
            'Tanzania, United Republic of': 'TZA',
            'Uganda': 'UGA',
            'Ukraine': 'UKR',
            'United States Minor Outlying Islands': 'UMI',
            'Uruguay': 'URY',
            'United States of America': 'USA',
            'United States': 'USA',
            'Uzbekistan': 'UZB',
            'Holy See': 'VAT',
            'Saint Vincent and the Grenadines': 'VCT',
            'Venezuela (Bolivarian Republic of)': 'VEN',
            'Virgin Islands (British)': 'VGB',
            'Virgin Islands (U.S.)': 'VIR',
            'Viet Nam': 'VNM',
            'Vanuatu': 'VUT',
            'Wallis and Futuna': 'WLF',
            'Samoa': 'WSM',
            'Yemen': 'YEM',
            'South Africa': 'ZAF',
            'Zambia': 'ZMB',
            'Zimbabwe': 'ZWE'
        }
        if nu.pickle_exists('us_stats_df'): self.us_stats_df = nu.load_object('us_stats_df')
        if nu.pickle_exists('column_description_dict'):
            self.column_description_dict = nu.load_object('column_description_dict')
        self.us_states_abbreviation_dict = {
            'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
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
        self.disease_name_dict = {
            '1918 (Spanish) flu': '1918 Flu',
            'AIDS/HIV infection': 'HIV',
            'Andes hantavirus': 'Hantavirus',
            'Anthrax, cutaneous': 'Cutaneous Anthrax',
            'Anthrax, gastrointestinal, intestinal type': 'Intestinal Anthrax',
            'Anthrax, gastrointestinal, oropharyngeal type': 'Oropharyngeal Anthrax',
            'Anthrax, specifically the pulmonary form': 'Pulmonary Anthrax',
            'Asian (1956–58) flu': '1956 Flu',
            'Aspergillosis, invasive pulmonary form': 'Aspergillosis',
            'Bubonic plague': 'Bubonic Plague',
            'COVID-19 (Alpha variant)': 'COVID-19 Alpha',
            'COVID-19 (Delta variant)': 'COVID-19 Delta',
            'COVID-19 (Omicron variant)': 'COVID-19 Omicron',
            'COVID-19 (ancestral strain)': 'COVID-19',
            'Chickenpox (varicella)': 'Varicella',
            'Cholera, in Africa': 'Cholera',
            'Common cold (e.g., rhinovirus)': 'Rhinovirus',
            'Coronavirus disease 2019 (COVID-19)': 'COVID-19',
            'Cryptococcal meningitis': 'Meningitis',
            'Dengue haemorrhagic fever (DHF)': 'DHF',
            'Diphtheria, respiratory': 'Respiratory Diphtheria',
            'Eastern equine encephalitis virus': 'EEE',
            'Ebola (2014 outbreak)': '2014 Ebola',
            'Ebola virus disease – specifically EBOV': 'EBOV',
            'Glanders, septicemic': 'Glanders',
            'Granulomatous amoebic encephalitis': 'GAE',
            'HIV/AIDS': 'HIV',
            'Hand, foot and mouth disease, children < 5 years old': 'HFMD',
            'Hantavirus infection': 'Hantavirus',
            'Hantavirus pulmonary syndrome (HPS)': 'HPS',
            'Hepatitis A, adults > 50 years old': 'Hepatitis A',
            'Hong Kong (1968–69) flu': '1968 Flu',
            'Influenza (1918 pandemic strain)': '1918 Flu',
            'Influenza (2009 pandemic strain)': '2009 Flu',
            'Influenza (seasonal strains)': 'Seasonal Flu',
            'Influenza A virus subtype H5N1': 'H5N1 Flu',
            'Influenza A, typical pandemics': 'Influenza A',
            'Intestinal capillariasis': 'Capillariasis',
            'Lassa fever': 'Lassa',
            'Macanine alphaherpesvirus 1': 'Alphaherpesvirus',
            'Marburg virus disease – all outbreaks combined': 'Marburg',
            'Measles (rubeola), in developing countries': 'Rubeola',
            'Meningococcal disease': 'Meningitis',
            'Middle Eastern Respiratory Syndrome (MERS)': 'MERS',
            'Mucormycosis (Black fungus)': 'Mucormycosis',
            'Mumps encephalitis': 'ME',
            'Nipah virus': 'Nipah',
            'Pertussis (whooping cough), children in developing countries': 'Pertussis',
            'Pertussis (whooping cough), infants in developing countries': 'Pertussis',
            'Plague, pneumonic': 'Pneumonic Plague',
            'Plague, septicemic': 'Septicemic Plague',
            'Primary amoebic meningoencephalitis': 'Meningoencephalitis',
            'Seasonal Influenza, Worldwide': 'Seasonal Flu',
            'Severe acute respiratory syndrome (SARS)': 'SARS',
            'Smallpox Variola major – specifically the malignant (flat) or hemorrhagic type': 'Variola Major',
            'Smallpox, Variola major': 'Variola Major',
            'Smallpox, Variola major – in pregnant women': 'Variola Major',
            'Smallpox, Variola minor': 'Variola Minor',
            'Tetanus, Generalized': 'Tetanus',
            'Transmissible spongiform encephalopathies': 'Encephalopathies',
            'Tuberculosis, HIV Negative': 'Tuberculosis',
            'Tularemia, pneumonic': 'Pneumonic Tularemia',
            'Tularemia, typhoidal': 'Typhoidal Tularemia',
            'Typhoid fever': 'Typhoid',
            'Varicella (chickenpox), adults': 'Varicella',
            'Varicella (chickenpox), children': 'Varicella',
            'Varicella (chickenpox), in newborns': 'Varicella',
            'Venezuelan Equine Encephalitis (VEE)': 'VEE',
            'Visceral leishmaniasis': 'Leishmaniasis',
        }
    
    
    
    @staticmethod
    def get_driver(browser_name='FireFox', verbose=True):
        if verbose: print('Getting the {} driver'.format(browser_name))
        log_dir = '../log'
        os.makedirs(name=log_dir, exist_ok=True)
        if browser_name == 'FireFox': executable_name = 'geckodriver'
        elif browser_name == 'Chrome': executable_name = 'chromedriver80'
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
    
    
    
    @staticmethod
    def wait_for(wait_count, verbose=True):
        if verbose: print('Waiting for {} seconds'.format(wait_count))
        import time
        time.sleep(wait_count)
    
    
    
    @staticmethod
    def get_country_state_equivalents(
        countries_df, country_name_column, country_value_column,
        states_df, state_name_column, state_value_column,
        cn_col_explanation=None, st_col_explanation=None,
        countries_set=None, states_set=None, verbose=False
    ):
        if countries_set is None:
            countries_set = set([cn for cn in countries_df[country_name_column] if str(cn) != 'nan'])
        
        # Check for duplicate country names
        mask_series = countries_df.duplicated(subset=[country_name_column], keep=False)
        assert countries_df[mask_series].shape[0] == 0, "You've duplicated some country names"
        
        mask_series = countries_df[country_name_column].isin(countries_set)
        assert countries_df[country_value_column].dtype == np.dtype('int64'), "You have the make the country values integers"
        country_tuples_list = [
            (r[country_name_column], r[country_value_column]) for i, r in countries_df[mask_series].iterrows()
        ]
        
        if states_set is None: states_set = set([sn for sn in states_df[state_name_column] if str(sn) != 'nan'])
        
        # Check for duplicate state names
        mask_series = states_df.duplicated(subset=[state_name_column], keep=False)
        assert states_df[mask_series].shape[0] == 0, "You've duplicated some state names"
        
        mask_series = states_df[state_name_column].isin(states_set)
        state_tuples_list = [
            (r[state_name_column], r[state_value_column]) for i, r in states_df[mask_series].iterrows()
        ]
        
        # Get country-to-state equivalence dictionary
        rows_list = []
        if verbose:
            if cn_col_explanation is None: cn_col_explanation = country_value_column.replace('_', ' ')
            print()
            explanations_list = []
            if verbose:
                print(state_tuples_list)
                print(country_tuples_list)
        for country_tuple in country_tuples_list:
            candidate_tuple = sorted([s for s in state_tuples_list], key=lambda x: abs(x[1] - country_tuple[1]))[0]
            state_name = candidate_tuple[0]
            country_name = country_tuple[0]
            if verbose:
                explanations_list.append(
                    f'{country_name} ({country_tuple[1]:.2f}) is close to the {cn_col_explanation} of'
                    f' {state_name} ({candidate_tuple[1]:.2f})'
                )
            row_dict = {}
            row_dict['country_name'] = country_name
            row_dict['state_name'] = state_name
            rows_list.append(row_dict)
        c2s_equivalent_dict = pd.DataFrame(rows_list).set_index('country_name').state_name.to_dict()
        if verbose:
            for explanation in sorted(explanations_list): print(explanation.replace('.00)', ')'))

        
        # Get the state-to-country equivalence dictionary
        rows_list = []
        if verbose:
            if st_col_explanation is None: st_col_explanation = state_value_column.replace('_', ' ')
            print()
            explanations_list = []
        for state_tuple in state_tuples_list:
            candidate_tuple = sorted([s for s in country_tuples_list], key=lambda x: abs(x[1] - state_tuple[1]))[0]
            country_name = candidate_tuple[0]
            state_name = state_tuple[0]
            if verbose: explanations_list.append(
                f'{state_name} ({state_tuple[1]:,.2f}) is close to the {st_col_explanation}'
                f' of {country_name} ({candidate_tuple[1]:,.2f})'
            )
            row_dict = {}
            row_dict['state_name'] = state_name
            row_dict['country_name'] = country_name
            rows_list.append(row_dict)
        s2c_equivalent_dict = pd.DataFrame(rows_list).set_index('state_name').country_name.to_dict()
        if verbose:
            for explanation in sorted(explanations_list): print(explanation.replace('.00)', ')'))
        
        return s2c_equivalent_dict, c2s_equivalent_dict
    
    
    
    @staticmethod
    def get_max_rsquared_adj(df, columns_list, verbose=False):
        if verbose:
            t0 = time.time()
        rows_list = []
        n = len(columns_list)
        import statsmodels.api as sm
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

    
    
    
    @staticmethod
    def load_timeseries(
        name, is_global=True, base_url=None, nondate_columns_list=None, dropped_columns_list=None
    ):
        import requests
        if is_global: global_local = 'global'
        else: global_local = 'US'
        if (base_url is None): base_url = 'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series'
        url = f'{base_url}/time_series_covid19_{name}_{global_local}.csv'
        
        if (nondate_columns_list is None): nondate_columns_list = ['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Lat', 'Long_', 'Combined_Key', 'Population']
        if name == 'confirmed': columns_list = nondate_columns_list[:-1]
        elif is_global: columns_list = ['Country/Region', 'Province/State', 'Lat', 'Long']
        else: columns_list = nondate_columns_list
        df = pd.read_csv(url, index_col=columns_list)
        df['type'] = name.lower()
        df.columns.name = 'date'
        
        if (dropped_columns_list is None): dropped_columns_list = ['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Lat', 'Long_', 'Combined_Key', 'Population']
        if name == 'confirmed': columns_list = dropped_columns_list[:-1]
        elif is_global: columns_list = ['Lat', 'Long']
        else: columns_list = dropped_columns_list
        df = (df
                .set_index('type', append=True)
                .reset_index(columns_list, drop=True)
                .stack()
                .reset_index()
                .set_index('date')
             )
        df.index = pd.to_datetime(df.index)
        if is_global: df.columns = ['country', 'state', 'type', 'cases']
        else: df.columns = ['state', 'country', 'type', 'cases']

        if is_global:

            # Fix South Korea
            df.loc[df.country =='Korea, South', 'country'] = 'South Korea'

            # Move HK to country level
            df.loc[df.state =='Hong Kong', 'country'] = 'Hong Kong'
            df.loc[df.state =='Hong Kong', 'state'] = np.nan

        # Aggregate large countries split by states
        if is_global: global_local = 'country'
        else: global_local = 'state'
        df = (df
             .groupby(['date', global_local, 'type'])
             .sum()
             .reset_index()
             .sort_values([global_local, 'date'])
             .set_index('date')
             )

        return df
    
    
    
    def driver_get_url(self, driver, url_str, verbose=True):
        if verbose: print('Getting URL: {}'.format(url_str))
        finished = 0
        fails = 0
        while (finished == 0) and (fails < 8):
            
            # Message: Timeout loading page after 100000ms
            try:
                driver.set_page_load_timeout(300)
                driver.get(url_str)
                finished = 1
            
            # Wait for 10 seconds
            except Exception as e:
                message = str(e).strip()
                if verbose: print(message)
                fails += 1
                self.wait_for(10, verbose=verbose)
    
    
    
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
        cu.column_description_dict[st_col_name] = st_col_explanation
        nu.store_objects(us_stats_df=self.us_stats_df, column_description_dict=cu.column_description_dict)
    
    
    
    @staticmethod
    def get_countries_with_min_threshold_for_data_frame(df_cases, is_global=True, by='cases', min_threshold=10):
        countries = df_cases[df_cases[by].ge(min_threshold)].sort_values(by=by, ascending=False)
        if is_global: global_local = 'country'
        else: global_local = 'state'
        countries = countries[global_local].values
        
        return countries
    
    
    
    @staticmethod
    def get_countries_with_min_threshold(df_cases, is_global=True, by='cases', min_threshold=10):
        countries = df_cases[df_cases[by].ge(min_threshold)].sort_values(by=by, ascending=False)
        if is_global: global_local = 'country'
        else: global_local = 'state'
        countries = countries[global_local].unique()
        
        return countries
