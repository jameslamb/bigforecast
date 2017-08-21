import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.api import VAR, DynamicVAR
import numpy as np
import math


def train_model(target_series, exog_df=None, model_type="ARIMA"):
    """
    Train a timeseries model on some dataset pulled from influxDB.

    Args:
        target_var (Series): A time-series pandas Series of \
            numeric data \n
        exog_vars (DataFrame): An optional pandas DataFrame of \
            exogenous variables \n
        model_type (str): String defining the type \
            of time series model you want to fit. \
            For now, only "ARIMA" is supported. \n

    Returns:
        A fitted model.
    """

    # Check inputs
    assert isinstance(target_series, pd.Series)
    assert exog_df is None or \
           (isinstance(exog_df, pd.DataFrame) and target_series.shape[0] == exog_df.shape[0])
    assert isinstance(model_type, str)

    # Train model
    out_mod = ARIMA(target_series, order=(1,1,1)).fit(disp=0, transparams = True)

    return(out_mod)


def prediction_plots(model, trainDF, target_var, exog_vars=None, holdout_perc=0.15):
    """
    Plot forecasting results from a timeseries model.

    Args:
        trainDF (DataFrame): Pandas DataFrame that the \
            model was trained on. \n
        model: An ARIMA model from statsmodels. \n
        holdout_perc (float): A number between 0 and 1 \
            indicating how much data should be held out. \n

    Returns:
        Nothing. Just produces some sweet plots
    """

    # Check inputs
    assert isinstance(holdout_perc, float)

    # Size of the training data
    num_obs = trainDF.shape[0]

    # Number of points from the near-end of history to plot when
    # examining what predictions look like in the future
    end_of_history_points = math.floor(num_obs * (holdout_perc + 0.10))
    
    # Number of steps into the future for out-of-sample plots
    end_out_of_sample = num_obs + math.floor(num_obs * holdout_perc)

    # Index of the final point in history to plot
    last_in_sample = num_obs - end_of_history_points

    # Plot the forecast for recent history
    fig, ax = plt.subplots()
    ax = trainDF[target_var][0:last_in_sample].plot(ax=ax)
    fig = model.plot_predict(last_in_sample + 1, num_obs, dynamic=True, ax=ax, plot_insample=True)
    title = "Dynamic Forecast of the last {} of the Input Data:".format(str(round(100*holdout_perc, 4)) + "%")
    ax.set_title(title)
    plt.show()

    # Plot forecast outside of the training data
    fig, ax = plt.subplots()
    start_hist = trainDF.shape[0] - end_of_history_points
    end_hist = trainDF.shape[0] - 1
    ax = trainDF[target_var][start_hist:end_hist].plot(ax=ax)
    title = "Dynamic Forecast {} into the future:".format(str(round(100*holdout_perc, 4)) + "%")
    ax.set_title(title)
    fig = arima_model.plot_predict(end_hist, end_out_of_sample, dynamic=True, ax=ax, plot_insample=True)
    plt.show()
