from influxdb import DataFrameClient
from influxdb import InfluxDBClient
import pandas as pd


def db_connect(host="198.11.200.86", database="example", client_type="influx"):
    """
    Connect to modeling DB. Just assumed you are connecting
    on the same box this notebook is running on.
    We can just hard-code this so we control what people do.

    Args:
        host (str): A valid IP address identifying an InfluxDB. \n
        database (str): Name of the DB to hit with queries. \n
        client_type (str): Set to "dataframe" to get an instance \
            of influxdb.DataFrameClient. Otherwise, this function \
            will return an instance of influxdb.InfluxDBClient

    Returns:
        InfluxDBClient: An instance of influxdb.InfluxDBClient \
            or influxdb.DataFrameClient connected to the \
            bigforecast modelling database. \n
    """

    # Check inputs
    assert isinstance(host, str)
    assert isinstance(database, str)

    if client_type == "dataframe":
        clientClass = DataFrameClient
    else:
        clientClass = InfluxDBClient

    # Create and return the client
    client = clientClass(host=host,
                         port=8086,
                         username="root",
                         password="root",
                         database=database)
    return(client)


def list_series(db_client):
    """
    Hit the database and list out which series
    are already stored there.

    Args:
        db_client (InfluxDBClient): A valid instance of \
            influxdb.InfluxDBClient or influxdb.DataFrameClient \n

    Returns:
        list: A list of series names available in the modelling database
    """

    # Check inputs
    assert isinstance(db_client, InfluxDBClient) or isinstance(db_client, DataFrameClient)

    # Grab measurements and parse results
    response = db_client.query("SHOW MEASUREMENTS")
    series_names = [namelist[0] for namelist in response.raw['series'][0]['values']]
    print("Series available in this DB:")
    return(series_names)


def db_exists(db_client, database):
    """
    Check if a database exists in InfluxDB \n

    Args:
        db_client (InfluxDBClient): A valid instance of \
            influxdb.InfluxDBClient or influxdb.DataFrameClient \n
        database (str): Name of the DB to hit with queries. \n

    Returns:
        bool: True if the database exists in InfluxDB. False otherwise.
    """

    # Check inputs
    assert isinstance(db_client, InfluxDBClient) or isinstance(db_client, DataFrameClient)
    assert isinstance(database, str)

    # Get a list of active databases in InfluxDB
    query_response = db_client.query("SHOW DATABASES").raw['series'][0]['values']
    active_dbs = [db[0] for db in query_response]

    return(database in active_dbs)


def build_dataset(db_client, var_list, start_time,
                  end_time, window_size="15m"):
    """
    Hit the modelling database and build a dataset.

    Args:
        db_client (InfluxDBClient): A valid instance of \
            influxdb.InfluxDBClient or influxdb.DataFrameClient \n
        var_list (list): A list of measurement names to query. \
            See bigforecast.list_series \n
        start_time (str): A date string of the form "2017-08-01T10:00:00Z", \
            indicating the earliest date from which to return data. \n
        end_time (str): A date string of the form "2017-08-01T10:00:00Z", \
            indicating the most recent date from which to return data. \n
        window_size (str): A valid duration string indicating the granularity \
            of the resulting dataset. This will be like "15m" for \
            15-minute windows, "2h" for 2-hour windows, etc. See \
            https://docs.influxdata.com/influxdb/v0.8/api/aggregate_functions/ \
            for more. \n

    Returns:
        (DataFrame): Pandas DataFrame with data to be passed to training stage.
    """

    # Check inputs
    assert isinstance(db_client, InfluxDBClient) or isinstance(db_client, DataFrameClient)
    assert isinstance(var_list, list)
    assert isinstance(start_time, str)
    assert isinstance(end_time, str)
    assert isinstance(window_size, str)

    # Format the query
    query_body = _make_query(var_list, start_time, end_time, window_size)

    # Execute the query
    response = db_client.query(query_body)

    # Return a pandas DF
    return(_response_to_dataframe(response))


def _make_query(var_list, start_time, end_time, window_size):
    """
    Create a valid InfluxDB aggregation query. See docs for \
    bigforecast.build_dataset. This function assumes that \
    the desired output is a set of windowed means of several \
    measurements. \n

    Args:
        var_list (list): A list of measurement names to query. \
            See bigforecast.list_series \n
        start_time (str): A date string of the form "2017-08-01T10:00:00Z", \
            indicating the earliest date from which to return data. \n
        end_time (str): A date string of the form "2017-08-01T10:00:00Z", \
            indicating the most recent date from which to return data. \n
        window_size (str): A valid duration string indicating the granularity \
            of the resulting dataset. This will be like "15m" for \
            15-minute windows, "2h" for 2-hour windows, etc. See \
            https://docs.influxdata.com/influxdb/v0.8/api/aggregate_functions/ \
            for more. \n

    Returns:
        str: A query to send to InfluxDB \n
    """

    # Check inputs
    assert isinstance(var_list, list)
    assert isinstance(start_time, str)
    assert isinstance(end_time, str)
    assert isinstance(window_size, str)

    # Set up a template to fill in
    template = "SELECT mean(value) " +\
               "FROM {fields} " + \
               "WHERE time > \'{gte}\' AND time < \'{lte}\' " +\
               "GROUP BY time({window})"

    # Build query string
    query_string = template.format(fields=",".join(var_list),
                                   gte=start_time,
                                   lte=end_time,
                                   window=window_size)

    return(query_string)


def _response_to_dataframe(response):
    """
    Given a response from the InfluxDB DataFrameClient, \
    merge the resulting DFs and give back a single DataFrame. \
    Note that this function assumes that you have issued \
    a query only for the mean of each measurement and that \
    your query used "GROUP BY time()" syntax. \n

    Args:
        response: A response from a query sent by an instance \
            of influxdb.DataFrameClient \n

    Returns:
        DataFrame: A single pandas DataFrame representation of \
            the result. \n
    """

    # Parse into a list of DataFrames, change column names
    df_list = []
    for name in response.keys():
        thisDF = response[name]
        thisDF.columns = [name]
        df_list.append(thisDF)

    # Join the results (each DF will have a dateTimeIndex already)
    outDF = df_list[0]
    if len(df_list) > 1:
        for nextDF in df_list[1:]:
            outDF = outDF.join(nextDF)

    return(outDF)


# TODO (jaylamb20@gmail.com): move this out of influx section of
# the package
def train_model(trainDF, dep_var, model_type="ARIMA"):
    """
    Train a timeseries model on some dataset pulled from influxDB.

    Args:
        trainDF (DataFrame): A time-series pandas DataFrame of \
            numeric data \n
        dep_var (str): Name of the column in trainDF to use as \
            the dependent variable. \n
        model_type (str): One of "VAR" or "ARIMA", defining the type \
            of time series model you want to fit. \n

    Returns:
        A fitted model.
    """

    # Check inputs
    assert isinstance(trainDF, pd.DataFrame)
    assert isinstance(dep_var, str)
    assert isinstance(model_type, str)

    # Train model

    # TODO (jaylamb20@gmail.com): actually write this
    pass
