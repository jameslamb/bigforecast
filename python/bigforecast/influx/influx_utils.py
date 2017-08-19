from influxdb import DataFrameClient
import pandas as pd


def db_connect(host="198.11.200.86", database="example"):
    """
    Connect to modeling DB. Just assumed you are connecting
    on the same box this notebook is running on.
    We can just hard-code this so we control what people do.

    Returns:
        DataFrameClient: An instance of influxdb.DataFrameClient \
            connected to the bigforecast modelling database.
    """

    # Check inputs
    assert isinstance(host, str)
    assert isinstance(database, str)

    # Create and return the client
    client = DataFrameClient(host=host,
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
        db_client (DataFrameClient): A valid instance of \
            influxdb.DataFrameClient \n

    Returns:
        list: A list of series names available in the modelling database
    """

    # Check inputs
    assert isinstance(db_client, DataFrameClient)

    # Grab measurements and parse results
    response = db_client.query("SHOW MEASUREMENTS")
    series_names = [namelist[0] for namelist in response.raw['series'][0]['values']]
    print("Series available in this DB:")
    return(series_names)


def build_dataset(db_client, var_list, start_time,
                  end_time, window_size="15m"):
    """
    Hit the modelling database and build a dataset.

    Args:
        db_client (DataFrameClient): A valid instance of \
            influxdb.DataFrameClient \n
        var_list (list): A list of field names to query. \
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
    assert isinstance(db_client, DataFrameClient)
    assert isinstance(var_list, list)
    assert isinstance(start_time, str)
    assert isinstance(end_time, str)
    assert isinstance(window_size, str)

    # Format the query
    query_body = _make_query(var_list, start_time, end_time, window_size)

    # Execute the query
    response = db_client.query(query_body)

    # Return a pandas DF
    return(response.raw)


def _make_query(var_list, table_name, start_time, end_time, window_size):
    """
    Create a valid InfluxDB query. See docs for bigforecast.build_dataset.
    """

    # Check inputs
    assert isinstance(var_list, list)
    assert isinstance(table_name, str)
    assert isinstance(start_time, str)
    assert isinstance(end_time, str)
    assert isinstance(window_size, str)

    # TODO (jaylamb20@gmail.com): actually write this
    pass


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
    model_

    # TODO (jaylamb20@gmail.com): actually write this
    pass
