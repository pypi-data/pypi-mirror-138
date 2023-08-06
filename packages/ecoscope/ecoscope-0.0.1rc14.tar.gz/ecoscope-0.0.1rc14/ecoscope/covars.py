import datetime
import pandas
import numpy
import ee


def extract_ee_img_coll_vals(region=None, img_coll_name='MODIS/006/MOD13Q1',
                             band_name='NDVI', scaling_const=0.0001, start=None,  end=None,
                             raster_resolution=500.0):

    ee.Initialize()

    def convertUnixTimeToDateTime(unixTime):
        t = datetime.datetime.utcfromtimestamp(int(unixTime / 1000))
        return t.strftime('%Y-%m-%d %H:%M:%S')

    def convertDateTimeToUnixTime(inputTime):
        epoch = datetime.datetime(1970, 1, 1, 0, 0, 0)
        return int((inputTime - epoch).total_seconds() * 1000)

    def ComputePolygonTimeSeries(region, t1, t2):

        """Returns a series of brightness over time for the polygon."""
        #     d2=datetime.strptime(t2_String,'%Y-%m-%d %H:%M:%S')
        #     d1=datetime.strptime(t1_String,'%Y-%m-%d %H:%M:%S')

        collection_now = ee.ImageCollection(img_coll_name).filterDate(convertDateTimeToUnixTime(t1),
                                                                      convertDateTimeToUnixTime(t2))

        collection_historic = ee.ImageCollection(img_coll_name).filter(ee.Filter.dayOfYear(t1.timetuple().tm_yday,
                                                                                           t2.timetuple().tm_yday))
        collection_now = collection_now.sort('system:time_start')
        collection_historic = collection_historic.sort('system:time_start')

        # Compute the mean brightness in the region in each image.
        def ComputeMean(img):
            reduction = img.select(band_name).reduceRegion(ee.Reducer.mean(),
                                                           region,
                                                           raster_resolution,
                                                           bestEffort=True)

            return ee.Feature(None, {band_name: reduction.get(band_name),
                                     'system:time_end': img.get('system:time_end')})

        # Extract the results as a list of lists.
        def ExtractMean(feature):
            return (feature.get('properties').get('system:time_end'),
                    feature.get('properties').get(band_name)) or numpy.NaN

        cur_data = collection_now.map(ComputeMean).getInfo()
        cur_data = map(ExtractMean, cur_data['features'])
        cur_vals = [(convertUnixTimeToDateTime(x[0]), x[1]) for x in cur_data]
        cur_data = pandas.DataFrame(cur_vals, columns=['time', band_name])
        cur_data[band_name] = cur_data[band_name] * scaling_const
        cur_data[band_name] = pandas.to_numeric(cur_data[band_name])
        cur_data.dropna(inplace=True)

        hist_data = collection_historic.map(ComputeMean).getInfo()
        hist_data = map(ExtractMean, hist_data['features'])
        hist_vals = [(convertUnixTimeToDateTime(x[0]), x[1]) for x in hist_data]
        hist_data = pandas.DataFrame(hist_vals, columns=['time', band_name])
        hist_data[band_name] = hist_data[band_name] * scaling_const
        hist_data[band_name] = pandas.to_numeric(hist_data[band_name])
        hist_data.dropna(inplace=True)

        return cur_data, hist_data

    cur_data, hist_data = ComputePolygonTimeSeries(region, t1=start, t2=end)

    cur_data['time'] = pandas.to_datetime(cur_data['time'])
    cur_data['day_of_year'] = cur_data['time'].apply(lambda x: int(x.timetuple().tm_yday))

    hist_data['time'] = pandas.to_datetime(hist_data['time'])
    hist_data['day_of_year'] = hist_data['time'].apply(lambda x: int(x.timetuple().tm_yday))

    # Calculate the mean & std dev of the historic values
    df_mean = hist_data.groupby(['day_of_year'])[band_name].agg([numpy.mean, numpy.std])
    df_mean.head()

    # Merge historic avg/stddev data with cur values
    final_df = pandas.merge(df_mean, cur_data, left_index=True, right_on='day_of_year', how='inner')
    final_df.sort_values('time', inplace=True)
    final_df.set_index('time', drop=True, inplace=True)
    return final_df