
#!/usr/bin/env python
# Utility Functions to Visualize datasets.
# Dave Babbitt <dave.babbitt@gmail.com>
# Author: Dave Babbitt, Data Scientist
# coding: utf-8

# Soli Deo gloria

"""
StatsChartingUtilities: A set of utility functions common to stats visualization
"""

# Use the following only if you are on a high definition device
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('retina')

from cycler import cycler
from matplotlib.pyplot import figure, xlabel, ylabel, annotate, cm
from numpy import linspace, logical_and, logical_not, isinf, isnan
from os import path, makedirs, remove
from random import choice
from scipy.stats import pearsonr
from seaborn import regplot
import warnings
warnings.filterwarnings('ignore')

class StatsChartingUtilities(object):
    """
    This class implements the core of the utility functions
    needed to visualize statistical content.
    
    Examples
    --------
    
    import sys
    
    # Insert at 1, 0 is the script path (or '' in REPL)
    sys.path.insert(1, '../py')
    
    from storage import Storage
    from stats_charting_utils import StatsChartingUtilities
    
    s = Storage()
    scu = StatsChartingUtilities(s=s)
    """
    
    def __init__(self, s=None, verbose=False):
        if s is None:
            from storage import Storage
            self.s = Storage()
        else:
            self.s = s
        
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
        self.facebook_aspect_ratio = 1.91
        self.twitter_aspect_ratio = 16/9

    def r(self, string_list=None):
        if string_list is None:
            string_list = self.colormaps_list

        return choice(string_list)

    def first_order_linear_scatterplot(self, df, xname, yname,
                                       xlabel_str='Overall Capitalism (explanatory variable)',
                                       ylabel_str='World Bank Gini % (response variable)',
                                       x_adj='capitalist', y_adj='unequal',
                                       title='"Wealth inequality is huge in the capitalist societies"',
                                       idx_reference='United States', annot_reference='most evil',
                                       aspect_ratio=None,
                                       least_x_xytext=(40, -10), most_x_xytext=(-150, 55),
                                       least_y_xytext=(-200, -10), most_y_xytext=(45, 0),
                                       reference_xytext=(-75, 25), color_list=None, verbose=False):
        '''
        Create a first order (linear) scatter plot assuming the data frame
        has a index called Country or something
        '''
        if aspect_ratio is None:
            aspect_ratio = self.facebook_aspect_ratio
        df = df[[xname, yname]].dropna()
        fig_width = 18
        fig_height = fig_width/aspect_ratio
        fig = figure(figsize=(fig_width, fig_height))
        ax = fig.add_subplot(111, autoscale_on=True)
        line_kws = dict(color='k', zorder=1, alpha=.25)
        if color_list is None:
            scatter_kws = dict(s=30, lw=.5, edgecolors='k', zorder=2)
        else:
            scatter_kws = dict(s=30, lw=.5, edgecolors='k', zorder=2, color=color_list)
        merge_axes_subplot = regplot(x=xname, y=yname, scatter=True, data=df, ax=ax,
                                     scatter_kws=scatter_kws, line_kws=line_kws)
        if not xlabel_str.endswith(' (explanatory variable)'):
            xlabel_str = '{} (explanatory variable)'.format(xlabel_str)
        xlabel_text = xlabel(xlabel_str)
        if not ylabel_str.endswith(' (response variable)'):
            ylabel_str = '{} (response variable)'.format(ylabel_str)
        ylabel_text = ylabel(ylabel_str)
        kwargs = dict(textcoords='offset points', ha='left', va='bottom',
                      bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                      arrowprops=dict(arrowstyle='->',
                                      connectionstyle='arc3,rad=0'))
        
        xdata = df[xname].values
        least_x = xdata.min()
        most_x = xdata.max()
        
        ydata = df[yname].values
        most_y = ydata.max()
        least_y = ydata.min()
        
        least_x_tried = most_x_tried = least_y_tried = most_y_tried = False
        if verbose:
            print(least_x, most_x, most_y, least_y)
        for label, x, y in zip(df.index, xdata, ydata):
            if verbose:
                print(label, x, y)
            if (x == least_x) and not least_x_tried:
                annotation = annotate('{} (least {})'.format(label, x_adj),
                                      xy=(x, y), xytext=least_x_xytext, **kwargs)
                least_x_tried = True
            elif (x == most_x) and not most_x_tried:
                annotation = annotate('{} (most {})'.format(label, x_adj),
                                      xy=(x, y), xytext=most_x_xytext, **kwargs)
                most_x_tried = True
            elif (y == least_y) and not least_y_tried:
                annotation = annotate('{} (least {})'.format(label, y_adj),
                                      xy=(x, y), xytext=least_y_xytext, **kwargs)
                least_y_tried = True
            elif (y == most_y) and not most_y_tried:
                annotation = annotate('{} (most {})'.format(label, y_adj),
                                      xy=(x, y), xytext=most_y_xytext, **kwargs)
                most_y_tried = True
            elif (label == idx_reference):
                annotation = annotate('{} ({})'.format(label, annot_reference),
                                      xy=(x, y), xytext=reference_xytext, **kwargs)
        title_obj = fig.suptitle(t=title, x=0.5, y=0.91)
        
        # Get r squared value
        inf_nan_mask = self.get_inf_nan_mask(xdata, ydata)
        pearsonr_tuple = pearsonr(xdata[inf_nan_mask], ydata[inf_nan_mask])
        pearson_r = pearsonr_tuple[0]
        pearsonr_statement = str('%.2f' % pearson_r)
        coefficient_of_determination_statement = str('%.2f' % pearson_r**2)
        p_value = pearsonr_tuple[1]
        if p_value < 0.0001:
            pvalue_statement = '<0.0001'
        else:
            pvalue_statement = '=' + str('%.4f' % p_value)
        s_str = r'$r^2=' + coefficient_of_determination_statement + ',\ p' + pvalue_statement + '$'
        text_tuple = ax.text(0.75, 0.9, s_str, alpha=0.5, transform=ax.transAxes, fontsize='x-large')
        
        return fig
    
    def population_pyramid(self, sample1_df, year=2019, county_column_name='County_Name',
                           state_column_name='State_Name', show=True, size_inches_tuple=None,
                           male_xticks_list=None, female_xticks_list=None, verbose=False):
        if size_inches_tuple is None:
            height_inches = 6
            width_inches = height_inches * self.twitter_aspect_ratio
            size_inches_tuple = (width_inches, height_inches)
        male_0_to_4_column_name = f'AGE04_MALE_{year}PE'
        male_5_to_9_column_name = f'AGE59_MALE_{year}PE'
        male_10_to_14_column_name = f'AGE1014_MALE_{year}PE'
        male_15_to_19_column_name = f'AGE1519_MALE_{year}PE'
        male_20_to_24_column_name = f'AGE2024_MALE_{year}PE'
        male_25_to_29_column_name = f'AGE2529_MALE_{year}PE'
        male_30_to_34_column_name = f'AGE3034_MALE_{year}PE'
        male_35_to_39_column_name = f'AGE3539_MALE_{year}PE'
        male_40_to_44_column_name = f'AGE4044_MALE_{year}PE'
        male_45_to_49_column_name = f'AGE4549_MALE_{year}PE'
        male_50_to_54_column_name = f'AGE5054_MALE_{year}PE'
        male_55_to_59_column_name = f'AGE5559_MALE_{year}PE'
        male_60_to_64_column_name = f'AGE6064_MALE_{year}PE'
        male_65_to_69_column_name = f'AGE6569_MALE_{year}PE'
        male_70_to_74_column_name = f'AGE7074_MALE_{year}PE'
        male_75_to_79_column_name = f'AGE7579_MALE_{year}PE'
        male_80_to_84_column_name = f'AGE8084_MALE_{year}PE'
        male_85_years_and_over_column_name = f'AGE85PLUS_MALE_{year}PE'
        female_0_to_4_column_name = f'AGE04_FEM_{year}PE'
        female_5_to_9_column_name = f'AGE59_FEM_{year}PE'
        female_10_to_14_column_name = f'AGE1014_FEM_{year}PE'
        female_15_to_19_column_name = f'AGE1519_FEM_{year}PE'
        female_20_to_24_column_name = f'AGE2024_FEM_{year}PE'
        female_25_to_29_column_name = f'AGE2529_FEM_{year}PE'
        female_30_to_34_column_name = f'AGE3034_FEM_{year}PE'
        female_35_to_39_column_name = f'AGE3539_FEM_{year}PE'
        female_40_to_44_column_name = f'AGE4044_FEM_{year}PE'
        female_45_to_49_column_name = f'AGE4549_FEM_{year}PE'
        female_50_to_54_column_name = f'AGE5054_FEM_{year}PE'
        female_55_to_59_column_name = f'AGE5559_FEM_{year}PE'
        female_60_to_64_column_name = f'AGE6064_FEM_{year}PE'
        female_65_to_69_column_name = f'AGE6569_FEM_{year}PE'
        female_70_to_74_column_name = f'AGE7074_FEM_{year}PE'
        female_75_to_79_column_name = f'AGE7579_FEM_{year}PE'
        female_80_to_84_column_name = f'AGE8084_FEM_{year}PE'
        female_85_years_and_over_column_name = f'AGE85PLUS_FEM_{year}PE'
        
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
        plot_title = f'Population Pyramid, {sample1_df[county_column_name].squeeze()}, '
        plot_title += f'{sample1_df[state_column_name].squeeze()}, {year}'
        fig.patch.set_facecolor('xkcd:light grey')
        plt.figtext(.5, .925, plot_title, fontsize=15, ha='center')

        # Define male and female bars
        male_ax.barh(y, df.Male, align='center', color='royalblue')
        male_ax.set(title='Males')
        female_ax.barh(y, df.Female, align='center', color='lightpink')
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

    def save_fig_as_various(self, fig, chart_name, dir_names_list=['pgf', 'png', 'svg'],
                            size_inches_tuple=None, verbose=False):
        """
        scu.save_fig_as_various(fig, 'relative_search_strength_of_unprecedented', verbose=True)
        """
        if size_inches_tuple is None:
            height_inches = 6
            width_inches = height_inches * self.twitter_aspect_ratio
            size_inches_tuple = (width_inches, height_inches)
        for dir_name in dir_names_list:
            try:
                dir_path = path.join(self.s.saves_folder, dir_name)
                makedirs(name=dir_path, exist_ok=True)
                file_path = path.join(dir_path, f'{chart_name}.{dir_name}')
                if path.exists(file_path):
                    remove(file_path)
                if verbose:
                    print('Saving plot to {}'.format(path.abspath(file_path)))
                fig.set_size_inches(size_inches_tuple[0], size_inches_tuple[1])
                fig.savefig(file_path, dpi=100)#, bbox_inches='tight'
            except Exception as e:
                print(f'{dir_name} got a {e.__class__} error: {str(e).strip()}')
    
    def make_a_movie(self, movie_prefix, file_names_list, max_width=None, verbose=True):
        
        # Get the maximum width of the images
        png_dir = path.join(self.s.saves_folder, 'png')
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
        gif_dir = path.join(self.s.saves_folder, 'gif')
        makedirs(name=gif_dir, exist_ok=True)
        gif_file_path = path.join(gif_dir, f'{movie_prefix}_movie.gif')
        
        # Save the movie
        kwargs = {'duration': 1}
        if verbose:
            print(f'Saving movie to {path.abspath(gif_file_path)}')
        imageio.mimsave(gif_file_path, images_list, **kwargs)

    def get_color_cycler(self, n):
        """
        color_cycler = scu.get_color_cycler(len(possible_cause_list))
        for possible_cause, face_color_dict in zip(possible_cause_list, color_cycler()):
            face_color = face_color_dict['color']
        """
        color_cycler = None
        if n < 9:
            color_cycler = cycler('color', cm.Accent(linspace(0, 1, n)))
        elif n < 11:
            color_cycler = cycler('color', cm.tab10(linspace(0, 1, n)))
        elif n < 13:
            color_cycler = cycler('color', cm.Paired(linspace(0, 1, n)))
        else:
            color_cycler = cycler('color', cm.tab20(linspace(0, 1, n)))
        
        return color_cycler

    def ball_and_chain(self, ax, index, values, c):
        """
        colormap = scu.r()
        cmap = mpl.cm.get_cmap(colormap)
        norm = LogNorm(vmin=values.min(), vmax=values.max())
        scu.ball_and_chain(ax, index, values, c=cmap(norm(values)))
        """
        ax.plot(index, values, c='k', zorder=1, alpha=.25)
        ax.scatter(index, values, s=30, lw=.5, c=c, edgecolors='k', zorder=2)

    def get_inf_nan_mask(self, x_list, y_list):
        x_mask = logical_and(logical_not(isinf(x_list)), logical_not(isnan(x_list)))
        y_mask = logical_and(logical_not(isinf(y_list)), logical_not(isnan(y_list)))
        
        return logical_and(x_mask, y_mask)