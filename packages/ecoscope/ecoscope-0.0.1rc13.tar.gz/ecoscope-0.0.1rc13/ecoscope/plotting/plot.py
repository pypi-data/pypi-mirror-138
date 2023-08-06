import matplotlib.ticker
import typing
import ast
import uuid
import logging

import geopandas
import mapclassify
import pandas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import seaborn as sns
import movdata
from shapely.geometry import MultiLineString
from ecoscope.plotting import GEOMAP
from ecoscope.io.utils import extract_voltage

ESRI_TOPOLOGY_BASEMAP = 'https://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}'
plt.rcParams.update({'figure.max_open_warning': 0})
sns.set_theme()
logger = logging.getLogger(__name__)


class SPEEDMAP(GEOMAP):
    speedmap_labels = []

    @property
    def default_speed_color(self):
        return ['#1a9850', '#91cf60', '#d9ef8b', '#fee08b', '#fc8d59', '#d73027']

    @staticmethod
    def _speedmap_labels(bins):
        return [f'{bins[i]:.1f} - {bins[i + 1]:.1f} km/hr' for i in range(len(bins) - 1)]

    @property
    def classification_methods(self):
        return {
            "equal_interval": mapclassify.EqualInterval,
            "natural_breaks": mapclassify.NaturalBreaks,
            "quantile": mapclassify.Quantiles,
            "std_mean": mapclassify.StdMean,
            "max_breaks": mapclassify.MaximumBreaks,
            "fisher_jenks": mapclassify.FisherJenks,
        }

    @staticmethod
    def create_multi_linestring(s):
        return MultiLineString(s['geometry'].tolist())

    def apply_classification(self, x, k, cls_method='natural_breaks', multiples=None):
        """
        Function to select which classifier to apply to the speed distributed data.

        Args:
        __________
        x (array)          : The input array to be classified. Must be 1-dimensional
        k (int)            : Number of classes required.
        cls_method (str)   : Classification method
        multiples (array)  : the multiples of the standard deviation to add/subtract from
                             the sample mean to define the bins.
                             defaults=[-2,-1,1,2]
        """
        if multiples is None:
            multiples = [-2, -1, 1, 2]

        classifier = self.classification_methods.get(cls_method)
        if not classifier:
            return

        map_classifier = classifier(x, multiples) if cls_method == 'std_mean' else classifier(x, k)
        edges, _, _ = mapclassify.classifiers._format_intervals(map_classifier, fmt="{:.2f}")

        print(map_classifier)
        return [float(i) for i in edges]

    def create_speedmap_df(self,
                           multi_trajectory: geopandas.GeoDataFrame,
                           classification_method: str = 'equal_interval',
                           no_class: int = 6,
                           speed_colors: typing.List = None,
                           bins: typing.List = None,
                           ):
        if not bins:
            # apply classification on speed data.
            bins = self.apply_classification(multi_trajectory.speed_kmhr, no_class, cls_method=classification_method)
        else:
            no_class = len(bins) - 1

        if speed_colors is None:
            speed_colors = self.default_speed_color[:no_class]

        multi_trajectory['speed_colour'] = pandas.cut(x=multi_trajectory.speed_kmhr,
                                                      bins=bins, labels=speed_colors,
                                                      include_lowest=True)
        # Group the data according to speed and create multi-linestrings for each group
        speedmap_df = geopandas.GeoDataFrame(geometry=multi_trajectory.groupby('speed_colour').apply(
            self.create_multi_linestring), crs=4326).reset_index()

        speedmap_df.sort_values(by='speed_colour', inplace=True)
        self.speedmap_labels = self._speedmap_labels(bins)
        return speedmap_df

    def _add_layers(self, df, basemap, linewidth):
        self.add_tiled_layer(source=basemap, crs=df.crs)
        self.add_vector_layer(df,
                              color=df.speed_colour.unique(),
                              column='speed_colour',
                              linewidth=linewidth,
                              linestyle='-', marker=0,
                              label=self.speedmap_labels)

    def plot_speedmap(self,
                      multi_trajectory: geopandas.GeoDataFrame,
                      basemap=ESRI_TOPOLOGY_BASEMAP,
                      classification_method: str = 'equal_interval',
                      linewidth: float = 1.,
                      no_class: int = 6,
                      speed_colors: typing.List = None,
                      bins: typing.List = None,
                      **kwargs: typing.Any
                      ):

        df = self.create_speedmap_df(multi_trajectory=multi_trajectory,
                                     classification_method=classification_method,
                                     no_class=no_class,
                                     speed_colors=speed_colors,
                                     bins=bins)
        self._add_layers(df=df, basemap=basemap, linewidth=linewidth)
        return super(SPEEDMAP, self).plot(**kwargs)


# alias
SpeedMap = SPEEDMAP


def timeseries(data: typing.Union[pandas.DataFrame, geopandas.GeoDataFrame],
               x: typing.Union[str, pandas.Series, geopandas.GeoSeries],
               y: typing.Union[str, typing.List[str], pandas.Series, geopandas.GeoSeries],
               upper: typing.Union[str, pandas.Series, geopandas.GeoSeries] = None,
               lower: typing.Union[str, pandas.Series, geopandas.GeoSeries] = None,
               figsize: typing.Tuple[int, int] = (15, 7),
               xlabel: str = '',
               ylabel: str = '',
               title: str = '',
               lineplot_kwgs: typing.Union[typing.Dict, typing.List[typing.Dict]] = None,
               fill_kwargs: typing.Dict = None,
               xlim: typing.Dict = None,
               ylim: typing.Dict = None,
               locator: matplotlib.ticker.Locator = None,
               formater: matplotlib.ticker.Formatter = None,
               legend: bool = True,
               legend_kwgs: typing.Dict = None
               ):
    if lineplot_kwgs is None:
        lineplot_kwgs = dict(linestyle='solid', marker='o', linewidth=1.)
    if fill_kwargs is None:
        fill_kwargs = dict(alpha=0.1, color='green')
    if legend_kwgs is None:
        legend_kwgs = dict(loc=0)

    fig, ax = plt.subplots(figsize=figsize)
    if isinstance(y, list) and isinstance(lineplot_kwgs, list):
        for yvalue, plot_kwargs in zip(y, lineplot_kwgs):
            sns.lineplot(data=data, x=x, y=yvalue, **plot_kwargs)
    elif isinstance(y, list):
        for yvalue in y:
            sns.lineplot(data=data, x=x, y=yvalue, **lineplot_kwgs)
    else:
        sns.lineplot(data=data, x=x, y=y, **lineplot_kwgs)

    if upper is not None and lower is not None:
        if isinstance(upper, str):
            upper = data[upper]
        if isinstance(lower, str):
            lower = data[lower]
        ax.fill_between(x=x, y1=upper, y2=lower, **fill_kwargs)
    if xlim:
        ax.set_xlim(**xlim)
    if ylim:
        ax.set_ylim(**ylim)
    if locator:
        ax.xaxis.set_major_locator(locator)
    if formater:
        ax.xaxis.set_major_formatter(formater)
    if legend:
        ax.legend(**legend_kwgs)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True)
    fig.autofmt_xdate()
    return ax, fig


def datacount(data, grouping_column, figsize=(20, 10), title='', xlabel=None, ylabel=None, rotation=90, **countplot):
    sns.set(rc={'figure.figsize': figsize})
    ax = sns.countplot(x=grouping_column, data=data, **countplot)
    plt.xticks(rotation=rotation)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax


def seasonal_window(data,
                    x='start',
                    y='season_code',
                    xlabel='',
                    ylabel='Season (1=wet, 0=dry)',
                    draw_style='steps-post',
                    step='post',
                    color='blue',
                    alpha=0.3):
    ax = sns.lineplot(x=x, y=y, data=data, drawstyle=draw_style)
    l1 = ax.lines[0]
    x1 = l1.get_xydata()[:, 0]
    y1 = l1.get_xydata()[:, 1]
    ax.fill_between(x1, y1, step=step, color=color, alpha=alpha)
    ax.set(xlabel=xlabel, ylabel=ylabel)
    return ax


def ndvi_seasonal_transition(vals,
                             season_cut_values,
                             xlabel='',
                             ylabel='',
                             title='',
                             subplot_kwargs=None,
                             histplot_kwargs=None,
                             axvline_kwargs=None):
    xmin = min(vals) - 0.1 * min(vals)
    xmax = max(vals) + 0.1 * min(vals)
    fig, ax = plt.subplots(**subplot_kwargs)
    ax.set_xlim(xmin, xmax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    sns.histplot(vals, **histplot_kwargs, ax=ax)
    [ax.axvline(x=i, **axvline_kwargs) for i in season_cut_values[1:-1]]
    return ax


def plot_collar_voltage(multirelocations:movdata.base.MultiRelocations,
                        start_time,
                        extract_fn=extract_voltage,
                        output_folder=None,
                        xhline_kwargs=None):
    multirelocations.unpack_additional(keyname=['subject_name', 'subject_source_id',
                                                'subject_source_end', 'additional'],
                                       colname=['subject_name', 'subject_source_id',
                                                'subject_source_end', 'metadata'])

    multirelocations_df = multirelocations.df().rename(columns={'metadata': 'additional',
                                                                'additional': 'metadata'})
    groups = multirelocations_df.groupby(by=['subject_name', 'subject_source_id'])
    for group, dataframe in groups:
        try:
            subject_source_end = dataframe.subject_source_end.unique()
            is_source_active = subject_source_end >= start_time or pandas.isna(subject_source_end)[0]

            if is_source_active:
                logger.info(group[0])

                dataframe = dataframe.sort_values(by=['fixtime'])
                dataframe['voltage'] = dataframe.apply(extract_fn, axis=1)

                time = dataframe[dataframe.fixtime >= start_time].fixtime.tolist()
                # time_rev = time[::-1]
                voltage = dataframe[dataframe.fixtime >= start_time].voltage.tolist()

                # Calculate the historical voltage
                hist_voltage = dataframe[dataframe.fixtime <= start_time].voltage.tolist()
                if hist_voltage:
                    volt_upper, volt_lower = np.nanpercentile(hist_voltage, [97.5, 2.5])
                    hist_voltage_mean = np.nanmean(hist_voltage)
                else:
                    volt_upper, volt_lower = np.nan, np.nan
                    hist_voltage_mean = None
                volt_diff = volt_upper - volt_lower
                volt_upper = np.full((len(time)), volt_upper, dtype=np.float32)
                volt_lower = np.full((len(time)), volt_lower, dtype=np.float32)

                if np.all(volt_diff == 0):
                    # jitter = np.random.random_sample((len(volt_upper,)))
                    volt_upper = volt_upper + 0.025 * max(volt_upper)
                    volt_lower = volt_lower - 0.025 * max(volt_lower)

                if not any(hist_voltage or voltage):
                    continue

                try:
                    lower_y = min(np.nanmin(np.array(hist_voltage)), np.nanmin(np.array(voltage)))
                    upper_y = max(np.nanmax(np.array(hist_voltage)), np.nanmax(np.array(voltage)))
                except ValueError:
                    lower_y = min(hist_voltage or voltage)
                    upper_y = max(hist_voltage or voltage)
                finally:
                    lower_y = lower_y - 0.1 * lower_y
                    upper_y = upper_y + 0.1 * upper_y

                voltage = np.array(voltage, dtype=np.float32)
                data = pandas.DataFrame({'voltage': voltage, 'time': time,
                                         'volt_lower': volt_lower, 'volt_upper': volt_upper})
                if voltage.size:
                    continue

                # set-ylim
                ylim = {'bottom': lower_y, 'top': upper_y} if not all([np.isnan(lower_y), np.isnan(upper_y)]) else None
                ax, fig = timeseries(data=data,
                                     x=data.time,
                                     y=data.voltage,
                                     figsize=(25, 10),
                                     lower='volt_lower',
                                     upper='volt_upper',
                                     lineplot_kwgs=dict(linestyle='solid', linewidth=1, label=group,
                                                        color='#0000FF'),
                                     fill_kwargs={'color': '#00aeff', 'alpha': 0.2,
                                                  'label': 'Historic 2.5% - 97.5%'},
                                     ylabel='Collar Voltage',
                                     xlabel='Time',
                                     ylim=ylim,
                                     formater=mdates.DateFormatter('%d %b, %y'),
                                     legend=True)
                xhline_kwargs = xhline_kwargs if xhline_kwargs else dict(color='r',
                                                                         linestyle='-',
                                                                         label='Historic average')
                ax.axhline(y=hist_voltage_mean, **xhline_kwargs) if hist_voltage_mean else None
                plt.legend()
                if output_folder:
                    fig.savefig(f'{output_folder}/_{group}_{str(uuid.uuid4())[:4]}.png', dpi=300)
        except ValueError as exc:
            logger.error(exc)
