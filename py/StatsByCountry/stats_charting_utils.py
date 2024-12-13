
#!/usr/bin/env python
# Utility Functions to Visualize datasets.
# Dave Babbitt <dave.babbitt@gmail.com>
# Author: Dave Babbitt, Data Scientist
# coding: utf-8

# Soli Deo gloria

"""
StatsChartingUtilities: A set of utility functions common to stats visualization
"""
from . import nu
from IPython.display import set_matplotlib_formats
from cycler import cycler
from matplotlib.pyplot import figure, xlabel, ylabel, annotate, cm, subplots
from numpy import linspace, logical_and, logical_not, isinf, isnan
from os import path, makedirs, remove
from random import choice
from scipy.stats import pearsonr
from seaborn import regplot
import warnings

set_matplotlib_formats('retina')
warnings.filterwarnings('ignore')
class StatsChartingUtilities(object):
    """
    This class implements the core of the utility functions
    needed to visualize statistical content.
    
    Examples:
        import sys
        sys.path.insert(1, osp.join(os.pardir, 'py'))
        from stats_charting_utils import StatsChartingUtilities
        scu = StatsChartingUtilities()
    """
    
    def __init__(self, verbose=False):
        
        # Colormaps and ascpect ratios
        self.colormaps_list = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r',
                               'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r',
                               'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges',
                               'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r',
                               'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r',
                               'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r',
                               'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r',
                               'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r',
                               'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r',
                               'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r',
                               'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r',
                               'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm',
                               'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r',
                               'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat',
                               'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r',
                               'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2',
                               'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r',
                               'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma',
                               'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean',
                               'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow',
                               'rainbow_r', 'rocket', 'rocket_r', 'seismic', 'seismic_r', 'spring', 'spring_r',
                               'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b',
                               'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'twilight',
                               'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r',
                               'vlag', 'vlag_r', 'winter', 'winter_r']

    def r(self, string_list=None):
        if string_list is None:
            string_list = self.colormaps_list

        return choice(string_list)
    
    @staticmethod
    def population_pyramid(sample1_df, year=2019, county_column_name='County_Name',
                           state_column_name='State_Name', show=True, size_inches_tuple=None,
                           male_xticks_list=None, female_xticks_list=None, verbose=False):
        if size_inches_tuple is None:
            height_inches = 6
            width_inches = height_inches * nu.twitter_aspect_ratio
            size_inches_tuple = (width_inches, height_inches)
        male_0_to_4_column_name = f'AGE04_MALE_{year}PE'
        if male_0_to_4_column_name not in sample1_df.columns: male_0_to_4_column_name = f'AGE04_MALE'
        male_5_to_9_column_name = f'AGE59_MALE_{year}PE'
        if male_5_to_9_column_name not in sample1_df.columns: male_5_to_9_column_name = f'AGE59_MALE'
        male_10_to_14_column_name = f'AGE1014_MALE_{year}PE'
        if male_10_to_14_column_name not in sample1_df.columns: male_10_to_14_column_name = f'AGE1014_MALE'
        male_15_to_19_column_name = f'AGE1519_MALE_{year}PE'
        if male_15_to_19_column_name not in sample1_df.columns: male_15_to_19_column_name = f'AGE1519_MALE'
        male_20_to_24_column_name = f'AGE2024_MALE_{year}PE'
        if male_20_to_24_column_name not in sample1_df.columns: male_20_to_24_column_name = f'AGE2024_MALE'
        male_25_to_29_column_name = f'AGE2529_MALE_{year}PE'
        if male_25_to_29_column_name not in sample1_df.columns: male_25_to_29_column_name = f'AGE2529_MALE'
        male_30_to_34_column_name = f'AGE3034_MALE_{year}PE'
        if male_30_to_34_column_name not in sample1_df.columns: male_30_to_34_column_name = f'AGE3034_MALE'
        male_35_to_39_column_name = f'AGE3539_MALE_{year}PE'
        if male_35_to_39_column_name not in sample1_df.columns: male_35_to_39_column_name = f'AGE3539_MALE'
        male_40_to_44_column_name = f'AGE4044_MALE_{year}PE'
        if male_40_to_44_column_name not in sample1_df.columns: male_40_to_44_column_name = f'AGE4044_MALE'
        male_45_to_49_column_name = f'AGE4549_MALE_{year}PE'
        if male_45_to_49_column_name not in sample1_df.columns: male_45_to_49_column_name = f'AGE4549_MALE'
        male_50_to_54_column_name = f'AGE5054_MALE_{year}PE'
        if male_50_to_54_column_name not in sample1_df.columns: male_50_to_54_column_name = f'AGE5054_MALE'
        male_55_to_59_column_name = f'AGE5559_MALE_{year}PE'
        if male_55_to_59_column_name not in sample1_df.columns: male_55_to_59_column_name = f'AGE5559_MALE'
        male_60_to_64_column_name = f'AGE6064_MALE_{year}PE'
        if male_60_to_64_column_name not in sample1_df.columns: male_60_to_64_column_name = f'AGE6064_MALE'
        male_65_to_69_column_name = f'AGE6569_MALE_{year}PE'
        if male_65_to_69_column_name not in sample1_df.columns: male_65_to_69_column_name = f'AGE6569_MALE'
        male_70_to_74_column_name = f'AGE7074_MALE_{year}PE'
        if male_70_to_74_column_name not in sample1_df.columns: male_70_to_74_column_name = f'AGE7074_MALE'
        male_75_to_79_column_name = f'AGE7579_MALE_{year}PE'
        if male_75_to_79_column_name not in sample1_df.columns: male_75_to_79_column_name = f'AGE7579_MALE'
        male_80_to_84_column_name = f'AGE8084_MALE_{year}PE'
        if male_80_to_84_column_name not in sample1_df.columns: male_80_to_84_column_name = f'AGE8084_MALE'
        male_85_years_and_over_column_name = f'AGE85PLUS_MALE_{year}PE'
        if male_85_years_and_over_column_name not in sample1_df.columns: male_85_years_and_over_column_name = f'AGE85PLUS_MALE'
        female_0_to_4_column_name = f'AGE04_FEM_{year}PE'
        if female_0_to_4_column_name not in sample1_df.columns: female_0_to_4_column_name = f'AGE04_FEM'
        female_5_to_9_column_name = f'AGE59_FEM_{year}PE'
        if female_5_to_9_column_name not in sample1_df.columns: female_5_to_9_column_name = f'AGE59_FEM'
        female_10_to_14_column_name = f'AGE1014_FEM_{year}PE'
        if female_10_to_14_column_name not in sample1_df.columns: female_10_to_14_column_name = f'AGE1014_FEM'
        female_15_to_19_column_name = f'AGE1519_FEM_{year}PE'
        if female_15_to_19_column_name not in sample1_df.columns: female_15_to_19_column_name = f'AGE1519_FEM'
        female_20_to_24_column_name = f'AGE2024_FEM_{year}PE'
        if female_20_to_24_column_name not in sample1_df.columns: female_20_to_24_column_name = f'AGE2024_FEM'
        female_25_to_29_column_name = f'AGE2529_FEM_{year}PE'
        if female_25_to_29_column_name not in sample1_df.columns: female_25_to_29_column_name = f'AGE2529_FEM'
        female_30_to_34_column_name = f'AGE3034_FEM_{year}PE'
        if female_30_to_34_column_name not in sample1_df.columns: female_30_to_34_column_name = f'AGE3034_FEM'
        female_35_to_39_column_name = f'AGE3539_FEM_{year}PE'
        if female_35_to_39_column_name not in sample1_df.columns: female_35_to_39_column_name = f'AGE3539_FEM'
        female_40_to_44_column_name = f'AGE4044_FEM_{year}PE'
        if female_40_to_44_column_name not in sample1_df.columns: female_40_to_44_column_name = f'AGE4044_FEM'
        female_45_to_49_column_name = f'AGE4549_FEM_{year}PE'
        if female_45_to_49_column_name not in sample1_df.columns: female_45_to_49_column_name = f'AGE4549_FEM'
        female_50_to_54_column_name = f'AGE5054_FEM_{year}PE'
        if female_50_to_54_column_name not in sample1_df.columns: female_50_to_54_column_name = f'AGE5054_FEM'
        female_55_to_59_column_name = f'AGE5559_FEM_{year}PE'
        if female_55_to_59_column_name not in sample1_df.columns: female_55_to_59_column_name = f'AGE5559_FEM'
        female_60_to_64_column_name = f'AGE6064_FEM_{year}PE'
        if female_60_to_64_column_name not in sample1_df.columns: female_60_to_64_column_name = f'AGE6064_FEM'
        female_65_to_69_column_name = f'AGE6569_FEM_{year}PE'
        if female_65_to_69_column_name not in sample1_df.columns: female_65_to_69_column_name = f'AGE6569_FEM'
        female_70_to_74_column_name = f'AGE7074_FEM_{year}PE'
        if female_70_to_74_column_name not in sample1_df.columns: female_70_to_74_column_name = f'AGE7074_FEM'
        female_75_to_79_column_name = f'AGE7579_FEM_{year}PE'
        if female_75_to_79_column_name not in sample1_df.columns: female_75_to_79_column_name = f'AGE7579_FEM'
        female_80_to_84_column_name = f'AGE8084_FEM_{year}PE'
        if female_80_to_84_column_name not in sample1_df.columns: female_80_to_84_column_name = f'AGE8084_FEM'
        female_85_years_and_over_column_name = f'AGE85PLUS_FEM_{year}PE'
        if female_85_years_and_over_column_name not in sample1_df.columns: female_85_years_and_over_column_name = f'AGE85PLUS_FEM'
        
        # Create dataframe
        import pandas as pd
        df = pd.DataFrame({
            'Age': ['0 to 4', '5 to 9', '10 to 14', '15 to 19', '20 to 24', '25 to 29', '30 to 34', '35 to 39',
                    '40 to 44', '45 to 49', '50 to 54', '55 to 59', '60 to 64', '65 to 69', '70 to 74',
                    '75 to 79', '80 to 84', '85 years and over'],
            'Male': [
                sample1_df[male_0_to_4_column_name].squeeze(), # Male population age 0 to 4
                sample1_df[male_5_to_9_column_name].squeeze(), # Male population age 5 to 9
                sample1_df[male_10_to_14_column_name].squeeze(), # Male population age 10 to 14
                sample1_df[male_15_to_19_column_name].squeeze(), # Male population age 15 to 19
                sample1_df[male_20_to_24_column_name].squeeze(), # Male population age 20 to 24
                sample1_df[male_25_to_29_column_name].squeeze(), # Male population age 25 to 29
                sample1_df[male_30_to_34_column_name].squeeze(), # Male population age 30 to 34
                sample1_df[male_35_to_39_column_name].squeeze(), # Male population age 35 to 39
                sample1_df[male_40_to_44_column_name].squeeze(), # Male population age 40 to 44
                sample1_df[male_45_to_49_column_name].squeeze(), # Male population age 45 to 49
                sample1_df[male_50_to_54_column_name].squeeze(), # Male population age 50 to 54
                sample1_df[male_55_to_59_column_name].squeeze(), # Male population age 55 to 59
                sample1_df[male_60_to_64_column_name].squeeze(), # Male population age 60 to 64
                sample1_df[male_65_to_69_column_name].squeeze(), # Male population age 65 to 69
                sample1_df[male_70_to_74_column_name].squeeze(), # Male population age 70 to 74
                sample1_df[male_75_to_79_column_name].squeeze(), # Male population age 75 to 79
                sample1_df[male_80_to_84_column_name].squeeze(), # Male population age 80 to 84
                sample1_df[male_85_years_and_over_column_name].squeeze(), # Male population age 85 years and over
            ],
            'Female': [
                sample1_df[female_0_to_4_column_name].squeeze(), # Female population age 0 to 4
                sample1_df[female_5_to_9_column_name].squeeze(), # Female population age 5 to 9
                sample1_df[female_10_to_14_column_name].squeeze(), # Female population age 10 to 14
                sample1_df[female_15_to_19_column_name].squeeze(), # Female population age 15 to 19
                sample1_df[female_20_to_24_column_name].squeeze(), # Female population age 20 to 24
                sample1_df[female_25_to_29_column_name].squeeze(), # Female population age 25 to 29
                sample1_df[female_30_to_34_column_name].squeeze(), # Female population age 30 to 34
                sample1_df[female_35_to_39_column_name].squeeze(), # Female population age 35 to 39
                sample1_df[female_40_to_44_column_name].squeeze(), # Female population age 40 to 44
                sample1_df[female_45_to_49_column_name].squeeze(), # Female population age 45 to 49
                sample1_df[female_50_to_54_column_name].squeeze(), # Female population age 50 to 54
                sample1_df[female_55_to_59_column_name].squeeze(), # Female population age 55 to 59
                sample1_df[female_60_to_64_column_name].squeeze(), # Female population age 60 to 64
                sample1_df[female_65_to_69_column_name].squeeze(), # Female population age 65 to 69
                sample1_df[female_70_to_74_column_name].squeeze(), # Female population age 70 to 74
                sample1_df[female_75_to_79_column_name].squeeze(), # Female population age 75 to 79
                sample1_df[female_80_to_84_column_name].squeeze(), # Female population age 80 to 84
                sample1_df[female_85_years_and_over_column_name].squeeze(), # Female population age 85 years and over
            ]
        })

        # View dataframe 
        if verbose:
            display(df)


        # Define x and y limits
        y = range(0, len(df))

        # Define plot parameters
        import matplotlib.pyplot as plt
        fig, (male_ax, female_ax) = plt.subplots(ncols=2, sharey=True, figsize=size_inches_tuple)
        plt.subplots_adjust(wspace=0, hspace=0)

        # Specify background color and plot title
        plot_title = f'Population Pyramid, '
        county_name = sample1_df[county_column_name].squeeze()
        if county_name: plot_title += f'{county_name}, '
        plot_title += f'{sample1_df[state_column_name].squeeze()}, {year}'
        fig.patch.set_facecolor('xkcd:light grey')
        plt.figtext(.5, .925, plot_title, fontsize=15, ha='center')

        # Define male and female bars
        male_ax.barh(y, df.Male, align='center', color='xkcd:baby blue')
        male_ax.set(title='Males')
        female_ax.barh(y, df.Female, align='center', color='xkcd:baby pink')
        female_ax.set(title='Females')

        # Adjust grid parameters and specify labels for y-axis
        female_ax.grid()
        male_ax.set(yticks=y, yticklabels=df['Age'])
        male_ax.invert_xaxis()
        male_ax.grid()
        
        if male_xticks_list is not None:
            male_ax.set_xticks(male_xticks_list)
        if female_xticks_list is not None:
            female_ax.set_xticks(female_xticks_list)
        
        if not show:
            plt.close(fig)
        
        return fig

    @staticmethod
    def save_fig_as_various(fig, chart_name, dir_names_list=['pgf', 'png', 'svg'],
                            size_inches_tuple=None, verbose=False):
        """
        scu.save_fig_as_various(fig, 'relative_search_strength_of_unprecedented', verbose=True)
        """
        if size_inches_tuple is None:
            height_inches = 6
            width_inches = height_inches * nu.twitter_aspect_ratio
            size_inches_tuple = (width_inches, height_inches)
        for dir_name in dir_names_list:
            try:
                dir_path = path.join(nu.saves_folder, dir_name)
                makedirs(name=dir_path, exist_ok=True)
                file_path = path.join(dir_path, f'{chart_name}.{dir_name}')
                if path.exists(file_path):
                    remove(file_path)
                if verbose:
                    print('Saving plot to {}'.format(path.abspath(file_path)))
                fig.set_size_inches(size_inches_tuple[0], size_inches_tuple[1])
                fig.savefig(file_path, dpi=100)#, bbox_inches='tight'
            except Exception as e:
                print(f'{dir_name} got a {e.__class__.__name__} error: {str(e).strip()}')
    
    @staticmethod
    def make_a_movie(movie_prefix, file_names_list, max_width=None, verbose=True):
        
        # Get the maximum width of the images
        png_dir = path.join(nu.saves_folder, 'png')
        import imageio
        if max_width is None:
            max_width = 0
            for file_name in file_names_list:
                file_path = path.join(png_dir, file_name)
                if path.isfile(file_path):
                    imageio_array = imageio.imread(file_path)
                    if imageio_array.shape[1] > max_width:
                        max_width = imageio_array.shape[1]
        
        # Get right-most column to use as fill
        base_array = imageio.imread(path.join(png_dir, file_names_list[-1]))
        base_height = base_array.shape[0]
        base_width = base_array.shape[1]
        base_depth = base_array.shape[2]
        reshape_tuple = (base_height, 1, base_depth)
        last_column = base_array[:, -1].reshape(reshape_tuple)
        
        # Get images file paths in the right order
        images_list = []
        for file_name in file_names_list:
            file_path = path.join(png_dir, file_name)
            if path.isfile(file_path):
                imageio_array = imageio.imread(file_path)
                while imageio_array.shape[1] < max_width:
                    arrays_tuple = (imageio_array, last_column)
                    imageio_array = np.hstack(arrays_tuple)
                images_list.append(imageio_array)
        
        # Let the viewer hang out at the last one a while
        for i in range(9):
            if path.isfile(file_path):
                images_list.append(imageio.imread(file_path))
        
        # Get movie file path
        gif_dir = path.join(nu.saves_folder, 'gif')
        makedirs(name=gif_dir, exist_ok=True)
        gif_file_path = path.join(gif_dir, f'{movie_prefix}_movie.gif')
        
        # Save the movie
        kwargs = {'duration': 1}
        if verbose:
            print(f'Saving movie to {path.abspath(gif_file_path)}')
        imageio.mimsave(gif_file_path, images_list, **kwargs)

    @staticmethod
    def ball_and_chain(ax, index, values, c):
        """
        colormap = scu.r()
        cmap = mpl.cm.get_cmap(colormap)
        norm = LogNorm(vmin=values.min(), vmax=values.max())
        scu.ball_and_chain(ax, index, values, c=cmap(norm(values)))
        """
        ax.plot(index, values, c='k', zorder=1, alpha=.25)
        ax.scatter(index, values, s=30, lw=.5, c=c, edgecolors='k', zorder=2)
    
    @staticmethod
    def get_fontsize(rect_width, label_length):
        """
        Get the widest text size that will fit in the rectangle width,
        given the count of characters in the label.

        Parameters:
            rect_width (float): width in pixels of the rectangle
            label_length (int): count of characters in the label.
        
        Returns:
            float: font size
        
        Note:
            Based on Wyoming: f(4.701557080830737, 7) = 10.0
        """
        fontsize = 14.888684492506771 * (rect_width / label_length)
        
        return fontsize
    
    @staticmethod
    def get_text_rgba(backround_rgba):
        """Get the color most contrasting with the background.

        Parameters
        ----------
        backround_rgba
            RGBA tuple of floats in the range of zero to one.

        Returns
        -------
        tuple
            RGBA tuple of floats in the range of zero to one
        """
        
        from math import sqrt
        
        text_rgba = (0.0, 0.0, 0.0, 1.0)
        if backround_rgba != (1.0, 1.0, 1.0, 1.0):
            text_colors_list = []
            for from_color in [(1.0, 1.0, 1.0, 1.0), (0.0, 0.0, 0.0, 1.0)]:
                green_diff = from_color[0] - backround_rgba[0]
                blue_diff = from_color[1] - backround_rgba[1]
                red_diff = from_color[2] - backround_rgba[2]
                color_distance = sqrt(green_diff**2 + blue_diff**2 + red_diff**2)
                color_tuple = (color_distance, from_color)
                text_colors_list.append(color_tuple)
            text_rgba = sorted(text_colors_list, key=lambda x: x[0])[-1][1]
        
        return text_rgba
    
    
    
    def draw_text(self, ax, s, r, c, va, text_kwargs):
        """
        Drawing text with Matplotlib.
    
        Parameters:
            ax: Matplotlib Axes instance
            s (str): The text
            r (dict): keyword arguments that describe the rectangle
            c (tuple): RGBA color tuple of floats in the range of zero to one
            va (str): {'center', 'top', 'bottom', 'baseline', 'center_baseline'}
                      passed to matplotlib.Axes.text for vertical alignment
            text_kwargs (dict): keyword arguments passed to matplotlib.Axes.text.
        """
        
        # Get text position and draw text
        x = r['x'] + (r['dx'] / 2)
        y = r['y'] + (r['dy'] / 2)
        text_obj = ax.text(x=x, y=y, s=s, va=va, ha='center', **text_kwargs)
        
        # Set text color to the highest contrast between black and white
        if not (('color' in text_kwargs) or ('c' in text_kwargs)):
            text_rgba = self.get_text_rgba(c)
            text_obj.set_color(text_rgba)
        
        # Set text size to the widest that will fit in the rectangle
        if not (('fontsize' in text_kwargs) or ('size' in text_kwargs)):
            fontsize = self.get_fontsize(r['dx'], len(s))
            text_obj.set_fontsize(fontsize)
    
    def plot_treemap_layout(self, values_list, colors_list, labels_list, ax, verbose=False):
        """Plotting with Matplotlib.

        Parameters
        ----------
        values_list
            sizes input for squarify
        colors_list
            list of rgba tuples (see Matplotlib documentation for details)
        labels_list
            list of label texts
        ax
            Matplotlib Axes instance
        """
        
        # Get the list of rectangles
        from squarify import normalize_sizes, squarify
        rects_list = squarify(normalize_sizes(values_list, 100, 100), 0, 0, 100, 100)
        
        # Draw the rectangles as horizontal bars with the bottom at y
        lefts_list = [rect['x'] for rect in rects_list]
        bottoms_list = [rect['y'] for rect in rects_list]
        widths_list = [rect['dx'] for rect in rects_list]
        heights_list = [rect['dy'] for rect in rects_list]
        ax.bar(x=lefts_list, height=heights_list, width=widths_list, bottom=bottoms_list,
               color=colors_list, label=labels_list, align='edge')
        
        # Draw the labels in the centers of the rectangles
        for label_str, rect, color_tuple in zip(labels_list, rects_list, colors_list):
            self.draw_text(ax, label_str, rect, color_tuple, 'center', text_kwargs={})
        
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
    
    def create_colored_labeled_treemap(self, df, size_column_name, color_column_name, fig_wdth=18, cmap=None, verbose=False):
        """Plotting Treemap layouts with Matplotlib.

        Parameters
        ----------
        df : pandas.DataFrame
            contains the size and color columns and the index labels needed to make the treemap
        size_column_name : str
            column that determines the relative sizes of the rectangles
        color_column_name : str
            column that determines the relative colors of the rectangles
        fig_wdth: float
            width and height of the figure in inches
        cmap : matplotlib.colors.ListedColormap
            color map used to map the `color_column_name` floats
        verbose : boolean
            prints debug information, if any
        """
        columns_list = [size_column_name, color_column_name]
        
        # Values must be sorted descending (and positive, obviously)
        df = df[columns_list].dropna().sort_values(size_column_name, ascending=False)
        color_column_series = df[color_column_name]
        
        fig, ax = subplots(figsize=(fig_wdth, fig_wdth))
        if cmap is None:
            from matplotlib.cm import get_cmap
            cmap = get_cmap()
        colors_list = [cmap(i) for i in color_column_series]
        AxesSubplot_obj = self.plot_treemap_layout(values_list=df[size_column_name].tolist(),
                                                   colors_list=colors_list, labels_list=df.index,
                                                   ax=ax, verbose=verbose)
