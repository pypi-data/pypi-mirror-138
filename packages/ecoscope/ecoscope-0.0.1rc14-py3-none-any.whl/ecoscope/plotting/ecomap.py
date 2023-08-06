import geopandas as gpd
import leafmap
import leafmap.foliumap
import mapclassify
import pandas as pd
from shapely.geometry import MultiLineString
import typing

ESRI_TOPOLOGY_BASEMAP = 'https://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}'


class EcoMapMixin():
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

        return [float(i) for i in edges]

    def create_speedmap_df(
        self,
        multi_trajectory: gpd.GeoDataFrame,
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

        multi_trajectory['speed_colour'] = pd.cut(x=multi_trajectory.speed_kmhr,
                                                  bins=bins,
                                                  labels=speed_colors,
                                                  include_lowest=True)
        # Group the data according to speed and create multi-linestrings for each group
        speedmap_df = gpd.GeoDataFrame(geometry=multi_trajectory.groupby('speed_colour').apply(
            self.create_multi_linestring),
                                       crs=4326).reset_index()

        speedmap_df.sort_values(by='speed_colour', inplace=True)
        self.speedmap_labels = self._speedmap_labels(bins)
        return speedmap_df

    def add_speedmap(self,
                     multi_trajectory: gpd.GeoDataFrame,
                     basemap=ESRI_TOPOLOGY_BASEMAP,
                     classification_method: str = 'equal_interval',
                     linewidth: float = 1.,
                     no_class: int = 6,
                     speed_colors: typing.List = None,
                     bins: typing.List = None,
                     **kwargs: typing.Any):

        df = self.create_speedmap_df(multi_trajectory=multi_trajectory,
                                     classification_method=classification_method,
                                     no_class=no_class,
                                     speed_colors=speed_colors,
                                     bins=bins)

        self.add_gdf(df, style_callback=lambda x: dict(color=x['properties']['speed_colour']))

        df['speed_colour'] = df['speed_colour'].apply(lambda x: x[1:])
        self.add_legend(legend_dict=dict(zip(self.speedmap_labels, df.speed_colour)))


class EcoMapFolium(EcoMapMixin, leafmap.foliumap.Map):
    pass


EcoMap = EcoMapFolium


class EcoMapIPyLeaflet(EcoMapMixin, leafmap.Map):
    pass
