
import os.path as osp

from .notebook_utils import NotebookUtilities
nu = NotebookUtilities(
    data_folder_path=osp.abspath('../data'),
    saves_folder_path=osp.abspath('../saves')
)

from .choropleth_utils import ChoroplethUtilities
us_stats_df = nu.load_object('us_stats_df')
if nu.pickle_exists('all_countries_df'):
    try:
        all_countries_df = nu.load_object('all_countries_df')
    except:
        all_countries_df = None
else:
    all_countries_df = None
cu = ChoroplethUtilities(
    iso_3166_2_code='us',
    one_country_df=us_stats_df,
    all_countries_df=all_countries_df
)

from .stats_charting_utils import StatsChartingUtilities
scu = StatsChartingUtilities()

from .stats_scraping_utils import StatsScrapingUtilities
ssu = StatsScrapingUtilities()

# print(f"from StatsByCountry import ({', '.join(dir())})")
# print(r'\b(' + '|'.join(dir()) + r')\b')