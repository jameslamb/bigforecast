import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.api import VAR, DynamicVAR


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
