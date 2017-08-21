#!/usr/bin/env python

# Load Dependencies
import datetime
import bigforecast.influx as bgfi
import json
import pandas as pd
import sys
import time

# Tiny function to get current time (for logging)
def now():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return(current_time)

# Read in and parse config. This acts as config
# validation as well (since you will get a keyError if
# anything is missing)
with open('macro_config.json', 'r') as f:
    macro_config = json.loads(f.read())

EQUITIES = [ticker.upper() for ticker in macro_config["equities"]]
CURRENCIES = [currency.upper() for currency in macro_config["currencies"]]
SYMBOLS = EQUITIES + CURRENCIES
DBNAME = macro_config["model_db"]
HOST = macro_config["influx_host"]

# Create DB client
influxDB = bgfi.db_connect(host=HOST, database=DBNAME, client_type="dataframe")

# Create the DB if it doesn't exist yet
if not bgfi.db_exists(influxDB, DBNAME):
    msg = "[{}] Database {} does not exist in InfluxDB running at {}.\n Creating it.\n"
    sys.stdout.write(msg.format(now(), DBNAME, HOST))
    influxDB.create_database(DBNAME)
else:
    msg = "[{}] Database {} already exists at {}! Not overwriting it.\n"
    sys.stdout.write(msg.format(now(), DBNAME, HOST))

# Pull a historical dataset for each series
# Currencies and symbols are pulled the same way
for ticker in SYMBOLS:

    msg = "[{}] Beginning backfill for {} from Yahoo Finance.\n"
    sys.stdout.write(msg.format(now(), ticker))

    # Get the historical dataset. Note that extracting
    # a single column from a pandas DataFrame will return
    # a Series, not a 1-column DataFrame
    sys.stdout.write("[{}] Pulling data...\n".format(now()))
    hist_series = bgfi.get_historical_data(ticker)['Close']
    sys.stdout.write("[{}] Returned dataset has {} observations.\n".format(now(), hist_series.shape[0]))

    # Make sure it is numeric
    # Ref: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.to_numeric.html
    hist_series = pd.to_numeric(hist_series, errors = 'coerce')

    # Drop anything converted to NaN by the above
    hist_series = hist_series.dropna(how="any")

    # Rename 'Close' to the ticker symbol
    hist_series.name = "value"

    # Interpolate with a cubic spline to get a 5-minutely dataset
    sys.stdout.write("[{}] Performing Imputation...\n".format(now()))
    hist_series = hist_series.resample('300S').interpolate(method='spline', order=3)
    sys.stdout.write("[{}] Resulting dataset has {} observations.\n".format(now(), hist_series.shape[0]))

    # You have to query for currencies with a trailing "=X".
    # Remove that before we write it.
    measurement = ticker.replace('=X', '')

    # Upload to influxDB
    sys.stdout.write("[{}] Writing to InfluxDB...\n".format(now()))
    influxDB.write_points(dataframe=pd.DataFrame(hist_series),
                          measurement=measurement,
                          protocol="json",
                          tags={"source": "Yahoo Finance",
                                "ingestion_process": "backfill",
                                "created_date": int(time.time())},
                          batch_size=500)

    # Clean up
    del hist_series

    sys.stdout.write("[{}] Done backfilling {}\n".format(now(), ticker))

# We are done!
sys.stdout.write("[{}] Done backfilling all symbols.\n".format(now()))


# NOTE: Why are there no timestamps?
#
#   Timestamps in influxDB are optional:
#   https://docs.influxdata.com/influxdb/v1.3/guides/writing_data/
#   Since this is a "time right now" process, we don't need to do a bunch
#   of work figuring out timestamps
