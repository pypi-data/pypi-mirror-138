import typing
import datetime
import ee
import pandas
import logging
import numpy
import sklearn.mixture as gauss
from sklearn.preprocessing import LabelEncoder
from scipy.stats import norm
import movdata.eetools as eetools
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class Seasons:
    start: datetime.datetime = None
    end: datetime.datetime = None
    image_col: str = 'MODIS/MCD43A4_006_NDVI'
    band: str = 'NDVI'
    analysis_scale_metre: int = 500
    analysis_geo: typing.Any = None
    analysis_date_chunks: int = 3
    calibration_func: typing.Callable = None
    season_num: int = 2
    season_labels: typing.Any = None
    values: float = field(init=False, repr=False, default=None)
    season_cut: float = field(init=False, repr=False, default=None)

    def extract_seasonal_vals(self):
        # TODO: define an identity calibration function if none exists

        secs = self.end.timestamp() - self.start.timestamp()
        chunk_size = secs // self.analysis_date_chunks
        date_slices = []
        cur_timestamp = self.start.timestamp()
        while cur_timestamp < self.end.timestamp():
            date_slices.append(cur_timestamp)
            cur_timestamp += chunk_size
        date_slices.append(self.end.timestamp() + 1)

        result_df = []

        for i in range(len(date_slices) - 1):

            start = datetime.datetime.fromtimestamp(date_slices[i])
            end = datetime.datetime.fromtimestamp(date_slices[i + 1] - 1)
            print('Processing date range: ', start, end)

            # get the image stack
            img_coll = ee.ImageCollection(self.image_col).select(self.band). \
                filterBounds(self.analysis_geo).filter(ee.Filter.date(start, end)). \
                sort('system:time_start', False)

            # add time info
            tmpColl = img_coll.map(eetools.add_img_time).toArray()

            # extract the pixel values falling within the region and for the given dates
            ee_result = tmpColl.reduceRegion(ee.Reducer.toList(), self.analysis_geo,
                                             self.analysis_scale_metre).getInfo()

            vals = pandas.DataFrame([[x[0], eetools.convertUnixTimeToDateTime(x[1])] for y in ee_result.get('array')
                                     for x in y], columns=['val', 'datetime'])

            if vals is not None:
                if self.calibration_func is not None:
                    vals['val'].apply(self.calibration_func)
                result_df.append(vals)

        self.values = pandas.concat(result_df, axis=0).sort_values(by='datetime')
        return self.values

    def seasonal_cutvals(self):
        try:
            if self.values is not None:
                distr = gauss.GaussianMixture(n_components=self.season_num, max_iter=500)
                vals = self.values['val'].values.reshape(-1, 1)
                distr.fit(vals)
                mu_vars = numpy.array(sorted(zip(distr.means_.flatten(),
                                                 distr.covariances_.flatten()), key=lambda x: x[0]))
                print('mu_vars', mu_vars)
                cuts = []
                x = numpy.linspace(0, 1.0, 1000)
                for i in range(1, len(mu_vars)):
                    cuts.append(numpy.max(x[tuple([norm.sf(x, loc=mu_vars[tuple([i - 1, 0])],
                                                           scale=numpy.sqrt(mu_vars[tuple([i - 1, 1])])) >
                                                   norm.cdf(x, loc=mu_vars[tuple([i, 0])],
                                                            scale=numpy.sqrt(mu_vars[tuple([i, 1])]))])]))
                cuts.append(float("inf"))
                cuts.append(float("-inf"))
                self.season_num = sorted(cuts)

            else:
                logger.exception('Could not run EM algorithm on null vals array.')
        finally:
            return self.season_cut

    def seasonal_windows(self, reducer_func=numpy.mean):
        result = None

        try:
            self.extract_seasonal_vals()
            self.seasonal_cutvals()

            if self.season_cut is None:
                logger.exception('Could not determine_seasonal_windows on null cut values array.')

            if self.values is None:
                logger.exception('Could not determine_seasonal_windows on null values array.')

            def g(group):
                group['reduce_val'] = group['val'].agg(reducer_func)
                return group.iloc[0]  # return first row only

            df = self.values.groupby('datetime').apply(g)
            df.drop(labels=['val'], axis=1, inplace=True)

            season_labels = self.season_labels
            if season_labels is None:
                season_labels = ['season_' + str(x) for x in range(len(self.season_cut))]

            df['season'] = pandas.cut(df['reduce_val'], bins=self.season_cut, labels=season_labels)

            enc = LabelEncoder()
            df['season_code'] = enc.fit_transform(df['season'])

            '''Adapted from https://stackoverflow.com/questions/26911851/
            how-to-use-pandas-to-find-consecutive-same-data-in-time-series'''
            df['Unique Season'] = (df['season_code'].diff(1) != 0).astype('int').cumsum()
            df['end'] = df['datetime'].shift(-1)

            # data = OrderedDict([('start', df.groupby('Unique Season')['datetime'].first()),
            #                     ('end', df.groupby('Unique Season')['end'].last()),
            #                     ('season', df.groupby('Unique Season')['season'].first())])
            #
            # result = pd.DataFrame(data, columns=data.keys())

            result = pandas.concat([pandas.Series([grp['datetime'][0] for name, grp in df.groupby('Unique Season')]),
                                    pandas.Series([grp['datetime'][-1] for name, grp in df.groupby('Unique Season')]),
                                    pandas.Series([name for name, _ in df.groupby('Unique Season')]),
                                    pandas.Series(grp['season'][0] for name, grp in df.groupby('Unique Season'))], axis=1)
            result.columns = ['start', 'end', 'unique_season', 'season']
            result.set_index('unique_season', inplace=True)

        except Exception as e:
            print(e)

        finally:
            return result
