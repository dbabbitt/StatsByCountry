
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
import re
import urllib
import warnings

warnings.filterwarnings('ignore')
class StatsScrapingUtilities(object):
    """
    This class implements the core of the utility functions
    needed to scrape statistical content off web pages.
    
    Example:
        import sys
        sys.path.insert(1, osp.join('..', 'py'))
        from stats_scraping_utils import StatsScrapingUtilities
        ssu = StatsScrapingUtilities()
    """
    
    def __init__(self, verbose=False):
        
        # Obscuration error and url patterns
        self.obscure_regex = re.compile('<([^ ]+)[^>]*class="([^"]+)"[^>]*>')
        
        # Renaming dictionaries, use it something like:
        # df.Country = df.Country.map(lambda x: ssu.country_name_dict.get(x, x))
        self.country_name_dict = {
            "Côte d'Ivoire": "Côte d'Ivoire",
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
            'Armenian SSR (Soviet Union → Armenia )': 'Armenia',
            'Aruba (Netherlands)': 'Aruba',
            'Azerbaijan SSR (Soviet Union → Azerbaijan)': 'Azerbaijan',
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
            'Bosnia and Herzegovina (Yugoslavia → Bosnia and Herzegovina)': 'Bosnia & Herzegovina',
            'Bosnia and Herzegovina': 'Bosnia & Herzegovina',
            'Botswana (British Empire, Bechuanaland Protectorate → Botswana)': 'Botswana',
            'Brunei (British Empire, British Protectorate → Brunei)': 'Brunei',
            'Brunei Darussalam': 'Brunei',
            'Burkina Faso (French Colonial Empire, French West Africa → Republic of Upper Volta → Burkina Faso)': 'Burkina Faso',
            'Burma (→ Myanmar)': 'Myanmar',
            'Burundi (Belgian overseas colonies, Ruanda-Urundi → United Nations trust territories → Burundi)': 'Burundi',
            'Byelorussian SSR (Soviet Union → Belarus)': 'Belarus',
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
            'Eritrea (Ethiopia → Eritrea)': 'Eritrea',
            'Estonian SSR (Soviet Union → Estonia)': 'Estonia',
            'Falkland Islands (UK)': 'Falkland Islands',
            'Fiji (British Empire → Fiji)': 'Fiji',
            'French Guiana (French Colonial Empire → France)': 'French Guiana',
            'French Polynesia (France)': 'French Polynesia',
            'French Polynesia (French Colonial Empire → France)': 'French Polynesia',
            'Gabon (French Colonial Empire, French Congo, French Equatorial Africa → Gabon': 'Gabon',
            'Gambia (British Empire, Gambia Colony and Protectorate → Gambia)': 'Gambia',
            'Gambia, The': 'Gambia',
            'Georgian SSR (Soviet Union → Georgia)': 'Georgia',
            'Germany (West Germany and East Germany → Germany)': 'Germany',
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
            'Kazakh SSR (Soviet Union → Kazakhstan)': 'Kazakhstan',
            'Kenya (British Empire, Kenya Colony → Kenya)': 'Kenya',
            'Kirghiz SSR (Soviet Union → Kyrgyzstan)': 'Kyrgyzstan',
            'Kiribati (British Empire, Gilbert and Ellice Islands → Kiribati)': 'Kiribati',
            'North Korea': 'North Korea',
            'Korea, Rep.': 'South Korea',
            'Korea, Republic of': 'South Korea',
            'Korea, South': 'South Korea',
            'Kuwait (British Empire, British Protectorate → Kuwait)': 'Kuwait',
            'Kyrgyz Republic': 'Kyrgyzstan',
            'Lao PDR': 'Laos',
            'Laos (French Colonial Empire, French Indochina, French Laos → Laos)': 'Laos',
            'Latvian SSR (Soviet Union → Latvia)': 'Latvia',
            'Lesotho (British Empire → Lesotho)': 'Lesotho',
            'Lithuanian SSR (Soviet Union → Lithuania)': 'Lithuania',
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
            'Moldavian SSR (Soviet Union → Moldova)': 'Moldova',
            'Moldova, Republic of': 'Moldova',
            'Montenegro (Yugoslavia → Montenegro)': 'Montenegro',
            'Mozambique (Portuguese Empire, Portuguese Mozambique → Mozambique)': 'Mozambique',
            'New Hebrides (British and French Condominium → Vanuatu)': 'Vanuatu',
            'Niger (French Colonial Empire, French Niger → Niger)': 'Niger',
            'Northern Rhodesia (British Empire, Federation of Rhodesia and Nyasaland → Zambia)': 'Zambia',
            'Qatar (British Empire, British Protectorate → Qatar)': 'Qatar',
            'Russian SFSR (Soviet Union → Russia)': 'Russia',
            'Rwanda (Belgian overseas colonies, Ruanda-Urundi → United Nations trust territories → Rwanda)': 'Rwanda',
            'SR Croatia (Yugoslavia → Croatia)': 'Croatia',
            'SR Macedonia (Yugoslavia → North Macedonia)': 'North Macedonia',
            'SR Serbia (Yugoslavia → Serbia and Montenegro → Serbia)': 'Serbia',
            'SR Slovenia (Yugoslavia → Slovenia)': 'Slovenia',
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
            'South West Africa (South Africa → Namibia)': 'Namibia',
            'Southern Rhodesia (British Empire, Federation of Rhodesia and Nyasaland → Zimbabwe)': 'Zimbabwe',
            'Sudan (British Empire, Anglo-Egyptian Sudan → Sudan)': 'Sudan',
            'Suriname (Kingdom of the Netherlands → Suriname)': 'Suriname',
            'Swaziland (British Empire → Swaziland)': 'Swaziland',
            'São Tomé and Príncipe (Portuguese Empire, Portuguese Sao Tome and Principe → São Tomé and Príncipe)': 'São Tomé & Príncipe',
            'Tajik SSR (Soviet Union → Tajikistan)': 'Tajikistan',
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
            'Turkmen SSR (Soviet Union → Turkmenistan)': 'Turkmenistan',
            'Uganda (British Empire → Uganda)': 'Uganda',
            'Trinidad And Tobago': 'Trinidad & Tobago',
            'Trinidad and Tobago': 'Trinidad & Tobago',
            'Turkey': 'Türkiye',
            'Turkiye': 'Türkiye',
            'Turks And Caicos Islands': 'Turks & Caicos Islands',
            'Turks and Caicos Islands': 'Turks & Caicos Islands',
            'U.S. Virgin Islands (US)': 'US Virgin Islands',
            'U.S. Virgin Islands': 'US Virgin Islands',
            'Ukrainian SSR (Soviet Union → Ukraine)': 'Ukraine',
            'Uzbek SSR (Soviet Union → Uzbekistan)': 'Uzbekistan',
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
            'Yemen (North Yemen and South Yemen → Yemen)': 'Yemen',
            'Yemen, Rep.': 'Yemen',
        }
        self.oecd_countries_list = [
            'Austria', 'Australia', 'Belgium', 'Canada', 'Chile',
            'Colombia', 'Costa Rica', 'Czechia', 'Denmark',
            'Estonia', 'Finland', 'France', 'Germany', 'Greece',
            'Hungary', 'Iceland', 'Ireland', 'Israel', 'Italy',
            'Japan', 'South Korea', 'Latvia', 'Lithuania', 'Luxembourg',
            'Mexico', 'Netherlands', 'New Zealand', 'Norway',
            'Poland', 'Portugal', 'Slovakia', 'Slovenia', 'Spain',
            'Sweden', 'Switzerland', 'Türkiye', 'UK', 'USA'
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
            'Turkiye': 'TUR',
            'Turkey': 'TUR',
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
        
        # From https://www.cia.gov/the-world-factbook/field/geographic-coordinates/
        self.country_centroids_dict = {
            "Afghanistan": "33 00 N, 65 00 E",
            
            # Akrotiri and Dhekelia
            "Akrotiri": "34 37 N, 32 58 E",
            "Dhekelia": "34 59 N, 33 45 E",
            
            "Albania": "41 00 N, 20 00 E",
            "Algeria": "28 00 N, 3 00 E",
            "American Samoa": "14 20 S, 170 00 W",
            "Andorra": "42 30 N, 1 30 E",
            "Angola": "12 30 S, 18 30 E",
            "Anguilla": "18 15 N, 63 10 W",
            "Antarctica": "90 00 S, 0 00 E",
            "Antigua and Barbuda": "17 03 N, 61 48 W",
            "Arctic Ocean": "90 00 N, 0 00 E",
            "Argentina": "34 00 S, 64 00 W",
            "Armenia": "40 00 N, 45 00 E",
            "Aruba": "12 30 N, 69 58 W",
            "Ashmore and Cartier Islands": "12 25 S, 123 20 E",
            "Ashmore Reef": "12 14 S, 123 05 E",
            "Cartier Islet": "12 32 S, 123 32 E",
            "Atlantic Ocean": "0 00 N, 25 00 W",
            "Australia": "27 00 S, 133 00 E",
            "Austria": "47 20 N, 13 20 E",
            "Azerbaijan": "40 30 N, 47 30 E",
            "Bahamas, The": "24 15 N, 76 00 W",
            "Bahrain": "26 00 N, 50 33 E",
            "Bangladesh": "24 00 N, 90 00 E",
            "Barbados": "13 10 N, 59 32 W",
            "Belarus": "53 00 N, 28 00 E",
            "Belgium": "50 50 N, 4 00 E",
            "Belize": "17 15 N, 88 45 W",
            "Benin": "9 30 N, 2 15 E",
            "Bermuda": "32 20 N, 64 45 W",
            "Bhutan": "27 30 N, 90 30 E",
            "Bolivia": "17 00 S, 65 00 W",
            "Bosnia and Herzegovina": "44 00 N, 18 00 E",
            "Botswana": "22 00 S, 24 00 E",
            "Bouvet Island": "54 26 S, 3 24 E",
            "Brazil": "10 00 S, 55 00 W",
            "British Indian Ocean Territory": "6 00 S, 71 30 E",
            "Diego Garcia": "7 20 S, 72 25 E",
            "British Virgin Islands": "18 30 N, 64 30 W",
            "Brunei": "4 30 N, 114 40 E",
            "Bulgaria": "43 00 N, 25 00 E",
            "Burkina Faso": "13 00 N, 2 00 W",
            "Burma": "22 00 N, 98 00 E",
            "Burundi": "3 30 S, 30 00 E",
            "Cabo Verde": "16 00 N, 24 00 W",
            "Cambodia": "13 00 N, 105 00 E",
            "Cameroon": "6 00 N, 12 00 E",
            "Canada": "60 00 N, 95 00 W",
            "Cayman Islands": "19 30 N, 80 30 W",
            "Central African Republic": "7 00 N, 21 00 E",
            "Chad": "15 00 N, 19 00 E",
            "Czech Republic": "49 45 N, 15 30 E",
            "Chile": "30 00 S, 71 00 W",
            "China": "35 00 N, 105 00 E",
            "Christmas Island": "10 30 S, 105 40 E",
            "Clipperton Island": "10 17 N, 109 13 W",
            "Cocos (Keeling) Islands": "12 30 S, 96 50 E",
            "Colombia": "4 00 N, 72 00 W",
            "Comoros": "12 10 S, 44 15 E",
            "Congo, Democratic Republic of the": "0 00 N, 25 00 E",
            "Congo, Republic of the": "1 00 S, 15 00 E",
            "Cook Islands": "21 14 S, 159 46 W",
            "Coral Sea Islands": "18 00 S, 152 00 E",
            "Costa Rica": "10 00 N, 84 00 W",
            "Côte d'Ivoire": "8 00 N, 5 00 W",
            "Croatia": "45 10 N, 15 30 E",
            "Cuba": "21 30 N, 80 00 W",
            "Curacao": "<p>12 10 N, 69 00 W",
            "Cyprus": "35 00 N, 33 00 E",
            "Czechia": "49 45 N, 15 30 E",
            "Democratic Republic of the Congo": "2 00 S, 23 00 E",
            "Denmark": "56 00 N, 10 00 E",
            "Djibouti": "11 30 N, 43 00 E",
            "Dominica": "15 25 N, 61 20 W",
            "Dominican Republic": "19 00 N, 70 40 W",
            "East Timor": "8 33 S, 125 34 E",
            "Ecuador": "2 00 S, 77 30 W",
            "Egypt": "27 00 N, 30 00 E",
            "El Salvador": "13 50 N, 88 55 W",
            "Equatorial Guinea": "2 00 N, 10 00 E",
            "Eritrea": "15 00 N, 39 00 E",
            "Estonia": "59 00 N, 26 00 E",
            "Eswatini": "26 30 S, 31 30 E",
            "Ethiopia": "8 00 N, 38 00 E",
            "Falkland Islands (Islas Malvinas)": "51 45 S, 59 00 W",
            "Faroe Islands": "62 00 N, 7 00 W",
            "Fiji": "18 00 S, 175 00 E",
            "Finland": "64 00 N, 26 00 E",
            
            # France
            "France": "46 00 N, 2 00 E", # Metropolitan
            "French Guiana": "4 00 N, 53 00 W",
            "Guadeloupe": "16 15 N, 61 35 W",
            "Martinique": "14 40 N, 61 00 W",
            "Mayotte": "12 50 S, 45 10 E",
            "Reunion": "21 06 S, 55 36 E",
            
            "French Polynesia": "15 00 S, 140 00 W",
            
            # French Southern and Antarctic Lands
            "Ile Amsterdam (Ile Amsterdam et Ile Saint-Paul)": "37 50 S, 77 32 E",
            "Ile Saint-Paul (Ile Amsterdam et Ile Saint-Paul)": "38 72 S, 77 53 E",
            "Iles Crozet": "46 25 S, 51 00 E",
            "Iles Kerguelen": "49 15 S, 69 35 E",
            "Bassas da India (Iles Eparses)": "21 30 S, 39 50 E",
            "Europa Island (Iles Eparses)": "22 20 S, 40 22 E",
            "Glorioso Islands (Iles Eparses)": "11 30 S, 47 20 E",
            "Juan de Nova Island (Iles Eparses)": "17 03 S, 42 45 E",
            "Tromelin Island (Iles Eparses)": "15 52 S, 54 25 E",
            
            "Gabon": "1 00 S, 11 45 E",
            "Gambia": "13 28 N, 16 34 W",
            "Gaza Strip": "31 25 N, 34 20 E",
            "Georgia": "42 00 N, 43 30 E",
            "Germany": "51 00 N, 9 00 E",
            "Ghana": "8 00 N, 2 00 W",
            "Gibraltar": "36 08 N, 5 21 W",
            "Greece": "39 00 N, 22 00 E",
            "Greenland": "72 00 N, 40 00 W",
            "Grenada": "12 07 N, 61 40 W",
            "Guam": "13 28 N, 144 47 E",
            "Guatemala": "15 30 N, 90 15 W",
            "Guernsey": "49 28 N, 2 35 W",
            "Guinea": "11 00 N, 10 00 W",
            "Guinea-Bissau": "12 00 N, 15 00 W",
            "Guyana": "5 00 N, 59 00 W",
            "Haiti": "19 00 N, 72 25 W",
            "Heard Island and McDonald Islands": "53 06 S, 72 31 E",
            "Holy See": "41 54 N, 12 27 E",
            "Honduras": "15 00 N, 86 30 W",
            "Hong Kong": "22 15 N, 114 10 E",
            "Hungary": "47 00 N, 20 00 E",
            "Iceland": "65 00 N, 18 00 W",
            "India": "20 00 N, 77 00 E",
            "Indian Ocean": "20 00 S, 80 00 E",
            "Indonesia": "5 00 S, 120 00 E",
            "Iran": "32 00 N, 53 00 E",
            "Iraq": "33 00 N, 44 00 E",
            "Ireland": "53 00 N, 8 00 W",
            "Isle of Man": "54 15 N, 4 30 W",
            "Israel": "31 30 N, 34 45 E",
            "Italy": "42 50 N, 12 50 E",
            "Jamaica": "18 15 N, 77 30 W",
            "Jan Mayen": "71 00 N, 8 00 W",
            "Japan": "36 00 N, 138 00 E",
            "Jersey": "49 15 N, 2 10 W",
            "Jordan": "31 00 N, 36 00 E",
            "Kazakhstan": "48 00 N, 68 00 E",
            "Kenya": "1 00 N, 38 00 E",
            "Kiribati": "1 25 N, 173 00 E",
            "North Korea": "40 00 N, 127 00 E",
            "South Korea": "37 00 N, 127 30 E",
            "Kosovo": "42 35 N, 21 00 E",
            "Kuwait": "29 30 N, 45 45 E",
            "Kyrgyzstan": "41 00 N, 75 00 E",
            "Laos": "18 00 N, 105 00 E",
            "Latvia": "57 00 N, 25 00 E",
            "Lebanon": "33 50 N, 35 50 E",
            "Lesotho": "29 30 S, 28 30 E",
            "Liberia": "6 30 N, 9 30 W",
            "Libya": "25 00 N, 17 00 E",
            "Liechtenstein": "47 16 N, 9 32 E",
            "Lithuania": "56 00 N, 24 00 E",
            "Luxembourg": "49 45 N, 6 10 E",
            "Macau": "22 10 N, 113 33 E",
            "Madagascar": "20 00 S, 47 00 E",
            "Malawi": "13 30 S, 34 00 E",
            "Malaysia": "2 30 N, 112 30 E",
            "Maldives": "3 15 N, 73 00 E",
            "Mali": "17 00 N, 4 00 W",
            "Malta": "35 50 N, 14 35 E",
            "Marshall Islands": "9 00 N, 168 00 E",
            "Mauritania": "20 00 N, 12 00 W",
            "Mauritius": "20 17 S, 57 33 E",
            "Mexico": "23 00 N, 102 00 W",
            "Micronesia, Federated States of": "6 55 N, 158 15 E",
            "Moldova": "47 00 N, 29 00 E",
            "Monaco": "43 44 N, 7 24 E",
            "Mongolia": "46 00 N, 105 00 E",
            "Montenegro": "42 30 N, 19 18 E",
            "Montserrat": "16 45 N, 62 12 W",
            "Morocco": "28 30 N, 10 00 W",
            "Mozambique": "18 15 S, 35 00 E",
            "Myanmar": "21 00 N, 96 00 E",
            "Namibia": "22 00 S, 17 00 E",
            "Nauru": "0 32 S, 166 55 E",
            "Navassa Island": "18 25 N, 75 02 W",
            "Nepal": "28 00 N, 84 00 E",
            "Netherlands": "52 31 N, 5 46 E",
            "New Caledonia": "21 30 S, 165 30 E",
            "New Zealand": "41 00 S, 174 00 E",
            "Nicaragua": "13 00 N, 85 00 W",
            "Niger": "16 00 N, 8 00 E",
            "Nigeria": "10 00 N, 8 00 E",
            "Niue": "19 02 S, 169 52 W",
            "Norfolk Island": "29 02 S, 167 57 E",
            "North Macedonia": "41 50 N, 22 00 E",
            "Northern Mariana Islands": "15 12 N, 145 45 E",
            "Norway": "62 00 N, 10 00 E",
            "Oman": "21 00 N, 57 00 E",
            "Pacific Ocean": "0 00 N, 160 00 W",
            "Pakistan": "30 00 N, 70 00 E",
            "Palau": "7 30 N, 134 30 E",
            "Palestine": "31 55 N, 35 12 E",
            "Panama": "9 00 N, 80 00 W",
            "Papua New Guinea": "6 00 S, 147 00 E",
            "Paracel Islands": "16 30 N, 112 00 E",
            "Paraguay": "23 00 S, 58 00 W",
            "Peru": "10 00 S, 76 00 W",
            "Philippines": "13 00 N, 122 00 E",
            "Pitcairn Islands": "25 04 S, 130 06 W",
            "Poland": "52 00 N, 20 00 E",
            "Portugal": "39 30 N, 8 00 W",
            "Puerto Rico": "18 15 N, 66 30 W",
            "Qatar": "25 30 N, 51 15 E",
            "Republic of the Congo": "1 00 S, 15 00 E",
            "Romania": "46 00 N, 25 00 E",
            "Russia": "60 00 N, 100 00 E",
            "Rwanda": "2 00 S, 30 00 E",
            "Saint Barthelemy": "17 90 N, 62 85 W",
            
            # Saint Helena, Ascension, and Tristan da Cunha
            "Saint Helena": "15 57 S, 5 42 W",
            "Ascension Island": "7 57 S, 14 22 W",
            "Tristan da Cunha island group": "37 15 S, 12 30 W",
            
            "Saint Kitts and Nevis": "17 20 N, 62 45 W",
            "Saint Lucia": "13 53 N, 60 58 W",
            "Saint Martin": "18 05 N, 63 57 W",
            "Saint Pierre and Miquelon": "46 50 N, 56 20 W",
            "Saint Vincent and the Grenadines": "13 15 N, 61 12 W",
            "Samoa": "13 35 S, 172 20 W",
            "San Marino": "43 46 N, 12 25 E",
            "Sao Tome and Principe": "1 00 N, 7 00 E",
            "Saudi Arabia": "25 00 N, 45 00 E",
            "Senegal": "14 00 N, 14 00 W",
            "Serbia": "44 00 N, 21 00 E",
            "Seychelles": "4 35 S, 55 40 E",
            "Sierra Leone": "8 30 N, 11 30 W",
            "Singapore": "1 22 N, 103 48 E",
            "Sint Maarten": "<p>18 4 N, 63 4 W",
            "Slovakia": "48 40 N, 19 30 E",
            "Slovenia": "46 07 N, 14 49 E",
            "Solomon Islands": "8 00 S, 159 00 E",
            "Somalia": "10 00 N, 49 00 E",
            "South Africa": "29 00 S, 24 00 E",
            "South Georgia and South Sandwich Islands": "54 30 S, 37 00 W",
            "South Ossetia": "42 21 N, 44 6 E",
            "South Sudan": "8 00 N, 30 00 E",
            "Southern Ocean": "60 00 S, 90 00 E",
            "Spain": "40 00 N, 4 00 W",
            "Spratly Islands": "8 38 N, 111 55 E",
            "Sri Lanka": "7 00 N, 81 00 E",
            "Sudan": "15 00 N, 30 00 E",
            "Suriname": "4 00 N, 56 00 W",
            "Svalbard": "78 00 N, 20 00 E",
            "Sweden": "62 00 N, 15 00 E",
            "Switzerland": "47 00 N, 8 00 E",
            "Syria": "35 00 N, 38 00 E",
            "Taiwan": "23 30 N, 121 00 E",
            "Tajikistan": "39 00 N, 71 00 E",
            "Tanzania": "6 00 S, 35 00 E",
            "Thailand": "15 00 N, 100 00 E",
            "Timor-Leste": "8 50 S, 125 55 E",
            "Togo": "8 00 N, 1 10 E",
            "Tokelau": "9 00 S, 172 00 W",
            "Tonga": "20 00 S, 175 00 W",
            "Trinidad and Tobago": "11 00 N, 61 00 W",
            "Tunisia": "34 00 N, 9 00 E",
            "Türkiye": "39 00 N, 35 00 E",
            "Turkmenistan": "40 00 N, 60 00 E",
            "Turks and Caicos Islands": "21 45 N, 71 35 W",
            "Tuvalu": "8 00 S, 178 00 E",
            "Uganda": "1 00 N, 32 00 E",
            "Ukraine": "49 00 N, 32 00 E",
            "United Arab Emirates": "24 00 N, 54 00 E",
            "United Kingdom": "54 00 N, 2 00 W",
            "United States": "38 00 N, 97 00 W",
            
            # United States Pacific Island Wildlife Refuges
            "Baker Island": "0 13 N, 176 28 W",
            "Howland Island": "0 48 N, 176 38 W",
            "Jarvis Island": "0 23 S, 160 01 W",
            "Johnston Atoll": "16 45 N, 169 31 W",
            "Kingman Reef": "6 23 N, 162 25 W",
            "Midway Islands": "28 12 N, 177 22 W",
            "Palmyra Atoll": "5 53 N, 162 05 W",
            
            "Uruguay": "33 00 S, 56 00 W",
            "Uzbekistan": "41 00 N, 64 00 E",
            "Vanuatu": "16 00 S, 167 00 E",
            "Venezuela": "8 00 N, 66 00 W",
            "Vietnam": "16 10 N, 107 50 E",
            "Virgin Islands": "18 20 N, 64 50 W",
            "Wake Island": "19 17 N, 166 39 E",
            "Wallis and Futuna": "13 18 S, 176 12 W",
            "West Bank": "32 00 N, 35 15 E",
            "Western Sahara": "24 30 N, 13 00 W",
            "Yemen": "15 00 N, 48 00 E",
            "Zambia": "15 00 S, 30 00 E",
            "Zimbabwe": "20 00 S, 30 00 E",
        }
        
        # From https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_number_of_land_borders
        self.country_borders_dict = {
            "Afghanistan": [
                "China",
                "Iran",
                "Pakistan",
                "Tajikistan",
                "Turkmenistan",
                "Uzbekistan",
            ],
            "Albania": [
                "Greece",
                "Kosovo",
                "North Macedonia",
                "Montenegro",
            ],
            "Algeria": [
                "Libya",
                "Mali",
                "Mauritania",
                "Morocco",
                "Niger",
                "Tunisia",
                "Western Sahara",
            ],
            "Andorra": ["France", "Spain"],
            "Angola": [
                "Democratic Republic of the Congo",
                "Republic of the Congo",
                "Namibia",
                "Zambia",
            ],
            "Antigua and Barbuda": [],
            "Argentina": [
                "Bolivia",
                "Brazil",
                "Chile",
                "Paraguay",
                "Uruguay",
            ],
            "Armenia": ["Azerbaijan", "Georgia", "Iran", "Türkiye"],
            "Australia": [],
            "Austria": [
                "Czech Republic",
                "Germany",
                "Hungary",
                "Italy",
                "Liechtenstein",
                "Slovakia",
                "Slovenia",
                "Switzerland",
            ],
            "Azerbaijan": [
                "Armenia",
                "Georgia",
                "Iran",
                "Russia",
                "Türkiye",
            ],
            "Bahamas": [],
            "Bahrain": ["Saudi Arabia"],
            "Bangladesh": ["India", "Myanmar"],
            "Barbados": [],
            "Belarus": [
                "Latvia",
                "Lithuania",
                "Poland",
                "Russia",
                "Ukraine",
            ],
            "Belgium": [
                "France",
                "Germany",
                "Luxembourg",
                "Netherlands",
            ],
            "Belize": ["Guatemala", "Mexico"],
            "Benin": ["Burkina Faso", "Niger", "Nigeria", "Togo"],
            "Bhutan": ["China", "India"],
            "Bolivia": [
                "Argentina",
                "Brazil",
                "Chile",
                "Paraguay",
                "Peru",
            ],
            "Bosnia and Herzegovina": [
                "Croatia",
                "Montenegro",
                "Serbia",
            ],
            "Botswana": [
                "Namibia",
                "South Africa",
                "Zambia",
                "Zimbabwe",
            ],
            "Brazil": [
                "Argentina",
                "Bolivia",
                "Colombia",
                "Guyana",
                "Paraguay",
                "Peru",
                "Suriname",
                "Uruguay",
                "Venezuela",
            ],
            "Brunei": ["Malaysia"],
            "Bulgaria": [
                "Greece",
                "North Macedonia",
                "Romania",
                "Serbia",
                "Türkiye",
            ],
            "Burkina Faso": [
                "Benin",
                "Côte d'Ivoire",
                "Ghana",
                "Mali",
                "Niger",
                "Togo",
            ],
            "Burundi": [
                "Democratic Republic of the Congo",
                "Rwanda",
                "Tanzania",
            ],
            "Cambodia": ["Laos", "Thailand", "Vietnam"],
            "Cameroon": [
                "Central African Republic",
                "Chad",
                "Republic of the Congo",
                "Equatorial Guinea",
                "Gabon",
                "Nigeria",
            ],
            "Canada": ["United States"],
            "Cape Verde": [],
            "Central African Republic": [
                "Cameroon",
                "Chad",
                "Democratic Republic of the Congo",
                "Republic of the Congo",
                "South Sudan",
                "Sudan",
            ],
            "Chad": [
                "Cameroon",
                "Central African Republic",
                "Libya",
                "Niger",
                "Nigeria",
                "Sudan",
            ],
            "Chile": ["Argentina", "Bolivia", "Peru"],
            "China": [
                "Afghanistan",
                "Bhutan",
                "India",
                "Kazakhstan",
                "North Korea",
                "Kyrgyzstan",
                "Laos",
                "Mongolia",
                "Myanmar",
                "Nepal",
                "Pakistan",
                "Russia",
                "Tajikistan",
                "Vietnam",
            ],
            "Colombia": [
                "Brazil",
                "Ecuador",
                "Panama",
                "Peru",
                "Venezuela",
            ],
            "Comoros": [],
            "Democratic Republic of the Congo": [
                "Angola",
                "Burundi",
                "Central African Republic",
                "Republic of the Congo",
                "Rwanda",
                "South Sudan",
                "Tanzania",
                "Uganda",
                "Zambia",
            ],
            "Republic of the Congo": [
                "Angola",
                "Cameroon",
                "Central African Republic",
                "Democratic Republic of the Congo",
                "Gabon",
            ],
            "Costa Rica": ["Nicaragua", "Panama"],
            "Côte d'Ivoire": [
                "Burkina Faso",
                "Ghana",
                "Guinea",
                "Liberia",
                "Mali",
            ],
            "Croatia": [
                "Bosnia and Herzegovina",
                "Hungary",
                "Montenegro",
                "Serbia",
                "Slovenia",
            ],
            "Cuba": [],
            "Cyprus": [],
            "Czech Republic": [
                "Austria",
                "Germany",
                "Poland",
                "Slovakia",
            ],
            "Denmark": ["Germany"],
            "Djibouti": ["Eritrea", "Ethiopia"],
            "Dominica": [],
            "Dominican Republic": ["Haiti"],
            "East Timor": ["Indonesia"],
            "Ecuador": ["Colombia", "Peru"],
            "Egypt": ["Palestine", "Israel", "Libya", "Sudan"],
            "El Salvador": ["Guatemala", "Honduras"],
            "Equatorial Guinea": ["Cameroon", "Gabon"],
            "Eritrea": ["Djibouti", "Ethiopia", "Sudan"],
            "Estonia": ["Latvia", "Russia"],
            "Eswatini": ["Mozambique", "South Africa"],
            "Ethiopia": [
                "Djibouti",
                "Eritrea",
                "Kenya",
                "Somalia",
                "South Sudan",
                "Sudan",
            ],
            "Fiji": [],
            "Finland": ["Norway", "Sweden", "Russia"],
            "France": [
                "Andorra",
                "Belgium",
                "Germany",
                "Italy",
                "Luxembourg",
                "Monaco",
                "Spain",
                "Switzerland",
            ],
            "Gabon": [
                "Cameroon",
                "Republic of the Congo",
                "Equatorial Guinea",
            ],
            "Gambia": ["Senegal"],
            "Georgia": [
                "Armenia",
                "Azerbaijan",
                "Russia",
                "Türkiye",
                "South Ossetia",
            ],
            "Germany": [
                "Austria",
                "Belgium",
                "Czech Republic",
                "Denmark",
                "France",
                "Luxembourg",
                "Netherlands",
                "Poland",
                "Switzerland",
            ],
            "Ghana": ["Burkina Faso", "Côte d'Ivoire", "Togo"],
            "Greece": [
                "Albania",
                "Bulgaria",
                "Türkiye",
                "North Macedonia",
            ],
            "Grenada": [],
            "Guatemala": [
                "Belize",
                "El Salvador",
                "Honduras",
                "Mexico",
            ],
            "Guinea": [
                "Côte d'Ivoire",
                "Guinea",
                "Liberia",
                "Mali",
                "Senegal",
                "Sierra Leone",
            ],
            "Guinea-Bissau": ["Guinea", "Senegal"],
            "Guyana": ["Brazil", "Suriname", "Venezuela"],
            "Haiti": ["Dominican Republic"],
            "Honduras": ["Guatemala", "El Salvador", "Nicaragua"],
            "Hong Kong": ["China"],
            "Hungary": [
                "Austria",
                "Croatia",
                "Romania",
                "Serbia",
                "Slovakia",
                "Slovenia",
                "Ukraine",
            ],
            "Iceland": [],
            "India": [
                "Bangladesh",
                "Bhutan",
                "China",
                "Myanmar",
                "Nepal",
                "Pakistan",
                "Sri Lanka",
                "India",
            ],
            "Indonesia": [
                "East Timor",
                "Malaysia",
                "Papua New Guinea",
            ],
            "Iran": [
                "Afghanistan",
                "Armenia",
                "Azerbaijan",
                "Iraq",
                "Pakistan",
                "Türkiye",
                "Turkmenistan",
            ],
            "Iraq": [
                "Iran",
                "Jordan",
                "Kuwait",
                "Saudi Arabia",
                "Syria",
                "Türkiye",
            ],
            "Ireland": ["United Kingdom"],
            "Israel": [
                "Egypt",
                "Palestine",
                "Jordan",
                "Lebanon",
                "Syria",
                "Palestine",
            ],
            "Italy": [
                "Austria",
                "France",
                "San Marino",
                "Slovenia",
                "Switzerland",
                "Holy See",
            ],
            "Jamaica": [],
            "Japan": [],
            "Jordan": [
                "Iraq",
                "Israel",
                "Saudi Arabia",
                "Syria",
                "Palestine",
            ],
            "Kazakhstan": [
                "China",
                "Kyrgyzstan",
                "Russia",
                "Turkmenistan",
                "Uzbekistan",
            ],
            "Kenya": [
                "Ethiopia",
                "Somalia",
                "South Sudan",
                "Tanzania",
                "Uganda",
            ],
            "Kiribati": [],
            "North Korea": [
                "China",
                "South Korea",
                "Russia",
            ],
            "South Korea": ["North Korea"],
            "Kosovo": [
                "Albania",
                "Montenegro",
                "North Macedonia",
                "Serbia",
            ],
            "Kuwait": ["Iraq", "Saudi Arabia"],
            "Kyrgyzstan": [
                "China",
                "Kazakhstan",
                "Tajikistan",
                "Uzbekistan",
            ],
            "Laos": [
                "Cambodia",
                "China",
                "Myanmar",
                "Thailand",
                "Vietnam",
            ],
            "Latvia": ["Belarus", "Estonia", "Lithuania", "Russia"],
            "Lebanon": ["Israel", "Syria"],
            "Lesotho": ["South Africa"],
            "Liberia": ["Guinea", "Côte d'Ivoire", "Sierra Leone"],
            "Libya": [
                "Algeria",
                "Chad",
                "Egypt",
                "Niger",
                "Sudan",
                "Tunisia",
            ],
            "Liechtenstein": ["Austria", "Switzerland"],
            "Lithuania": ["Belarus", "Latvia", "Poland", "Russia"],
            "Luxembourg": ["Belgium", "France", "Germany"],
            "Macau": ["China"],
            "Madagascar": [],
            "Madeira": [],
            "Malawi": ["Mozambique", "Tanzania", "Zambia"],
            "Malaysia": ["Brunei", "Indonesia", "Thailand"],
            "Maldives": [],
            "Mali": [
                "Algeria",
                "Burkina Faso",
                "Côte d'Ivoire",
                "Guinea",
                "Mauritania",
                "Niger",
                "Senegal",
            ],
            "Malta": [],
            "Marshall Islands": [],
            "Mauritania": [
                "Algeria",
                "Mali",
                "Senegal",
                "Western Sahara",
            ],
            "Mauritius": [],
            "Mexico": ["Belize", "Guatemala", "United States"],
            "Federated States of Micronesia": [],
            "Moldova": ["Romania", "Ukraine"],
            "Monaco": ["France"],
            "Mongolia": ["China", "Russia"],
            "Montenegro": [
                "Albania",
                "Bosnia and Herzegovina",
                "Croatia",
                "Kosovo",
                "Serbia",
            ],
            "Morocco": ["Algeria", "Western Sahara"], # Fixed the consideration of the Straight of Gilbraltor as a border
            "Mozambique": [
                "Eswatini",
                "Malawi",
                "South Africa",
                "Tanzania",
                "Zambia",
                "Zimbabwe",
            ],
            "Myanmar": [
                "Bangladesh",
                "China",
                "India",
                "Laos",
                "Thailand",
            ],
            "Namibia": [
                "Angola",
                "Botswana",
                "South Africa",
                "Zambia",
            ],
            "Nauru": [],
            "Nepal": ["China", "India"],
            "Netherlands": ["Belgium", "Germany"],
            "New Zealand": [],
            "Nicaragua": ["Costa Rica", "Honduras"],
            "Niger": [
                "Algeria",
                "Benin",
                "Burkina Faso",
                "Chad",
                "Libya",
                "Mali",
                "Nigeria",
            ],
            "Nigeria": ["Benin", "Cameroon", "Chad", "Niger"],
            "North Macedonia": [
                "Albania",
                "Bulgaria",
                "Greece",
                "Kosovo",
                "Serbia",
            ],
            "Norway": ["Finland", "Sweden", "Russia"],
            "Oman": [
                "Saudi Arabia",
                "United Arab Emirates",
                "Yemen",
            ],
            "Pakistan": [
                "Afghanistan",
                "India",
                "Iran",
                "China",
            ],
            "Palau": [],
            "Palestine": ["Egypt", "Israel", "Jordan"],
            "Panama": ["Colombia", "Costa Rica"],
            "Papua New Guinea": ["Indonesia"],
            "Paraguay": ["Argentina", "Bolivia", "Brazil"],
            "Peru": [
                "Bolivia",
                "Brazil",
                "Chile",
                "Colombia",
                "Ecuador",
            ],
            "Philippines": [],
            "Poland": [
                "Belarus",
                "Czech Republic",
                "Germany",
                "Lithuania",
                "Russia",
                "Slovakia",
                "Ukraine",
            ],
            "Portugal": ["Spain"],
            "Qatar": ["Saudi Arabia"],
            "Romania": [
                "Bulgaria",
                "Hungary",
                "Moldova",
                "Serbia",
                "Ukraine",
            ],
            "Russia": [
                "Azerbaijan",
                "Belarus",
                "China",
                "Estonia",
                "Finland",
                "Georgia",
                "Kazakhstan",
                "North Korea",
                "Latvia",
                "Lithuania",
                "Mongolia",
                "Norway",
                "Poland",
                "Ukraine",
            ],
            "Rwanda": [
                "Burundi",
                "Democratic Republic of the Congo",
                "Tanzania",
                "Uganda",
            ],
            "Saint Kitts and Nevis": [],
            "Saint Lucia": [],
            "Saint Pierre and Miquelon": ["Canada"],
            "Saint Vincent and the Grenadines": [],
            "Samoa": [],
            "San Marino": ["Italy"],
            "São Tomé and Príncipe": [],
            "Saudi Arabia": [
                "Bahrain",
                "Iraq",
                "Jordan",
                "Kuwait",
                "Oman",
                "Qatar",
                "United Arab Emirates",
                "Yemen",
            ],
            "Senegal": [
                "Gambia",
                "Guinea",
                "Guinea",
                "Mali",
                "Mauritania",
            ],
            "Serbia": [
                "Bosnia and Herzegovina",
                "Bulgaria",
                "Croatia",
                "Hungary",
                "Kosovo",
                "Montenegro",
                "North Macedonia",
                "Romania",
            ],
            "Seychelles": [],
            "Sierra Leone": ["Guinea", "Liberia"],
            "Singapore": [],
            "Slovakia": [
                "Austria",
                "Czech Republic",
                "Hungary",
                "Poland",
                "Ukraine",
            ],
            "Slovenia": ["Austria", "Croatia", "Italy", "Hungary"],
            "Solomon Islands": [],
            "Somalia": ["Djibouti", "Ethiopia", "Kenya"],
            "South Africa": [
                "Botswana",
                "Eswatini",
                "Lesotho",
                "Mozambique",
                "Namibia",
                "Zimbabwe",
            ],
            "South Ossetia": ["Russia", "Georgia"],
            "South Sudan": [
                "Central African Republic",
                "Democratic Republic of the Congo",
                "Ethiopia",
                "Kenya",
                "Sudan",
                "Uganda",
            ],
            "Spain": [
                "Andorra",
                "France",
                "Portugal",
            ],
            "Sri Lanka": [],
            "Sudan": [
                "Central African Republic",
                "Chad",
                "Egypt",
                "Eritrea",
                "Ethiopia",
                "Libya",
                "South Sudan",
            ],
            "Suriname": ["Brazil", "Guyana"],
            "Sweden": ["Finland", "Norway"],
            "Switzerland": [
                "Austria",
                "France",
                "Italy",
                "Liechtenstein",
                "Germany",
            ],
            "Syria": [
                "Iraq",
                "Israel",
                "Jordan",
                "Lebanon",
                "Türkiye",
            ],
            "Taiwan": [],
            "Tajikistan": [
                "Afghanistan",
                "China",
                "Kyrgyzstan",
                "Uzbekistan",
            ],
            "Tanzania": [
                "Burundi",
                "Democratic Republic of the Congo",
                "Kenya",
                "Malawi",
                "Mozambique",
                "Rwanda",
                "Uganda",
                "Zambia",
            ],
            "Thailand": ["Cambodia", "Laos", "Malaysia", "Myanmar"],
            "Togo": ["Benin", "Burkina Faso", "Ghana"],
            "Tonga": [],
            "Trinidad and Tobago": [],
            "Tunisia": ["Algeria", "Libya"],
            "Türkiye": [
                "Armenia",
                "Azerbaijan",
                "Bulgaria",
                "Georgia",
                "Greece",
                "Iran",
                "Iraq",
                "Syria",
            ],
            "Turkmenistan": [
                "Afghanistan",
                "Iran",
                "Kazakhstan",
                "Uzbekistan",
            ],
            "Tuvalu": [],
            "Uganda": [
                "Democratic Republic of the Congo",
                "Kenya",
                "Rwanda",
                "South Sudan",
                "Tanzania",
            ],
            "Ukraine": [
                "Belarus",
                "Hungary",
                "Moldova",
                "Poland",
                "Romania",
                "Russia",
                "Slovakia",
            ],
            "United Arab Emirates": ["Oman", "Saudi Arabia"],
            "United Kingdom": ["Ireland"],
            "United States": ["Canada", "Mexico"],
            "Uruguay": ["Argentina", "Brazil"],
            "Uzbekistan": [
                "Afghanistan",
                "Kazakhstan",
                "Kyrgyzstan",
                "Tajikistan",
                "Turkmenistan",
            ],
            "Vanuatu": [],
            "Holy See": ["Italy"],
            "Venezuela": ["Brazil", "Colombia", "Guyana"],
            "Vietnam": [
                "Cambodia",
                "China",
                "Laos",
            ],
            "Western Sahara": ["Algeria", "Mauritania", "Morocco"],
            "Yemen": ["Oman", "Saudi Arabia"],
            "Zambia": [
                "Angola",
                "Botswana",
                "Democratic Republic of the Congo",
                "Malawi",
                "Mozambique",
                "Namibia",
                "Tanzania",
                "Zimbabwe",
            ],
            "Zimbabwe": [
                "Botswana",
                "Mozambique",
                "South Africa",
                "Zambia",
            ],
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
    def parse_to_decimal(coord_string):
        try:
            def convert_part(part):
                # Match degrees, minutes, direction
                match = re.match(r"(\d+)\s+(\d+)\s+([NSEW])", part)
                if not match:
                    raise ValueError(f"Invalid coordinate part: {part}")
                degrees, minutes, direction = match.groups()
                decimal = float(degrees) + float(minutes) / 60
                # Negate for south and west
                if direction in "SW":
                    decimal = -decimal
                return decimal
            
            # Split coordinate string into latitude and longitude parts
            lat_str, lon_str = coord_string.split(", ")
            latitude = convert_part(lat_str)
            longitude = convert_part(lon_str)
            
            return (latitude, longitude)
        except:
            from geopy import Point
            point = Point(coord_string)
            
            return (point.latitude, point.longitude)
    
    
    
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
