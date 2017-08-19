#This is the script
import argparse
from influxdb import InfluxDBClient
import pandas as pd
import datetime
from pandas import datetime
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.api import VAR, DynamicVAR

#This script's main funtion is predict.  This function managers the process of pulling data from influx db,
#procesing the datastructure so that we can model the data.  We have 2 statistical models implmented here:
#ARIMA and VAR.

default_value_from_query = -1
measurement = "stockpricedemo"
interval_length = "15m"

#pulls data from influxdb based on parameters, returning a list of data
def pull_influx_data(table_name, ticker, varlist, start_time, end_time, interval_length):
    host='localhost'
    port=8086
    user = 'root'
    password = 'root'
    dbname = 'mydb'
    query = 'SELECT mean(price) as price'
    for var in varlist:
        query = query + ", mean(" + var +")" + " as " + var
    query = query + ' from ' + table_name + ' Where time >= \'' + start_time + '\' and time <= \'' + end_time + '\' and ticker = \'' + ticker + \
    '\' GROUP BY time(' + interval_length + ') fill(' + str(default_value_from_query) + ') ;'
    client = InfluxDBClient(host, port, user, password, dbname)

    print("Queying data from influx db: " + query)


    result = client.query(query)
    return_this = ""
    for result in result:
        return_this = result

    return return_this

def process_list_to_dataframe(list_of_influx_results, varlist):
     #if no entry for a given timeframe, what does the data default to?
    varlist = ["price"] + varlist
    model_data = pd.DataFrame() #index=index = "time", columns = varlist
    for item in list_of_influx_results:
        #print(item)
        varvalues = [item['time']]
        for var in varlist:
            varvalues.append(float(item[var]))
        append_this = pd.Series(varvalues, index=["time"] + varlist)
        model_data = model_data.append(append_this, ignore_index = True)
    model_data.set_index(pd.DatetimeIndex(model_data["time"]), inplace = True)
    del model_data["time"]
    
    
    #remove lines where default values are zero
    for var in varlist:
        model_data = model_data[model_data[var] != default_value_from_query]
    
    #print("in process_list_to_dataframe3", model_data)
    return model_data
    
    
def ARIMAmodel(RawData, lags_to_forecast):
    RawData = RawData.values
    size = int(len(RawData) * 0.8)
    forecast_size = len(RawData)- size
    #split data into training and test sets
    train, test = RawData[0:size], RawData[size:len(RawData)]
    train = [x for x in train]
    test = [x[0] for x in test]

    bestp, bestd, bestq = -1, -1, -1
    best_error = 1000000
    forecasted_values = []
    for p in range(0,5):
        for d in range(0,5):
            for q in range(0,5):
                try:
                    #print(p,d,q)
                    model = ARIMA(train, order=(p,d,q))
                    model_fit = model.fit(disp=0, transparams = True)  # Add transparams = True, returns statsmodels.tsa.arima.ARIMAResults class
                    forecasted_values = [x for x in model_fit.forecast(forecast_size)[0]]
                    error = mean_squared_error(y_true = test, y_pred = forecasted_values)
                    if error < best_error:
                        bestp = p
                        bestd = d
                        bestq = q
                except:
                    pass

    print("Best ARIMA model (p,d,q) : (" + str(bestp) + "," + str(bestd) + "," + str(bestq) + ")")

    # forecast
    if not(bestp == -1 or bestd == -1 or bestq == -1):
        #Predict the next few lags
        model = ARIMA(RawData, order=(bestp,bestd,bestq))
        model_fit = model.fit(disp=0, transparams = True)
        forecasted_values = [x for x in model_fit.forecast(lags_to_forecast)[0]]
        return forecasted_values
    else:
        print("no valid ARIMA model")
        return None

    
def VARmodel(RawData, VAR, lags_to_forecast):
    size = int(len(RawData) * 0.8)
    forecast_size = len(RawData)- size

    #split data into training and test sets
    train, test = RawData[0:size], RawData[size:len(RawData)]

    bestp = -1
    best_error = 1000000
    forecasted_values = []
    for p in range(0,min(size,25)):
        try:
            #print("trying", p)
            train_model = VAR(train)
            var_model = train_model.fit(p) 
            lag_order = var_model.k_ar
            forecasted_values = [x[1] for x in var_model.forecast(train[-lag_order:].values, steps = forecast_size)]
            error = mean_squared_error(y_true = test["price"], y_pred = forecasted_values)
            if error < best_error:
                bestp = p
        except:
            pass

    # predict
    if bestp != -1:
        #Predict the next few lags
        model = VAR(RawData)
        var_model = train_model.fit(bestp) 
        lag_order = var_model.k_ar
        forecasted_values = [x[1] for x in var_model.forecast(RawData[-lag_order:].values, steps = lags_to_forecast)]
        return forecasted_values
    else:
        print("No VAR Model fitted")
        return None


#defaults to ARIMA model.  Include a list of variable names to include if you wish to use a VAR model.
def predict(varlist = [], ticker = "uso", lags_to_forecast = 5, table_name= measurement, start_time = "2017-08-17", end_time = "2017-08-19"):
    print("pulling data")
    list_of_data = pull_influx_data(table_name, ticker, varlist, start_time, end_time, interval_length) #add ticker
    print("making dataframe")
    dataframe_to_model = process_list_to_dataframe(list_of_data, varlist)
    if varlist == []:
        #use arima model
        print("Running ARIMA model")
        predicted_values = ARIMAmodel(dataframe_to_model, lags_to_forecast)
        print "----------------------"
        print "ARIMA model predicts the next", lags_to_forecast, "lags to be:" , predicted_values
        print "----------------------"
    else:
        #use VAR model
        hello=1
        print("Running VAR model")
        predicted_values = VARmodel(dataframe_to_model, VAR, lags_to_forecast)
        print "----------------------" 
        print "VAR model predicts the next", lags_to_forecast, "lags to be:" ,  predicted_values
        print "----------------------" 
    


