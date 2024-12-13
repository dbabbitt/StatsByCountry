
# Add the path to the shared utilities directory
import os.path as osp

# Define the shared folder path using join for better compatibility
shared_folder = osp.abspath(osp.join(
    osp.dirname(__file__), os.pardir, os.pardir, os.pardir, 'share'
))

# Add the shared folder to sys.path if it's not already included
import sys
if shared_folder not in sys.path:
    sys.path.insert(1, shared_folder)

# Attempt to import the Storage object
try:
    from notebook_utils import NotebookUtilities
except ImportError as e:
    print(f"Error importing NotebookUtilities: {e}")

# Initialize with data and saves folder paths
nu = NotebookUtilities(
    data_folder_path=osp.abspath(osp.join(
        osp.dirname(__file__), os.pardir, os.pardir, 'data'
    )),
    saves_folder_path=osp.abspath(osp.join(
        osp.dirname(__file__), os.pardir, os.pardir, 'saves'
    ))
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