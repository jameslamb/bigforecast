# Train an ARIMA model
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

# Train a VAR model
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

    # plot
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

# make predictions
def predict(varlist = [], ticker = "uso", steps_ahead = 5, start_time = "2017-08-17", end_time = "2017-08-19", window_size = "15m"):
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