#!/usr/bin/env python

# Load Dependencies
import datetime
import bigforecast.influx as bgfi
import json
from yahoo_finance import Share
import sys
import time

# Read in and parse config. This acts as config
# validation as well (since you will get a keyError if
# anything is missing)
with open('macro_config.json', 'r') as f:
    macro_config = json.loads(f.read())

TICKERS = macro_config["tickers"]
DBNAME = macro_config["model_db"]
HOST = macro_config["influx_host"]
BACKFILL_START = macro_config["backfill_start"]
BACKFILL_END = macro_config["backfill_end"]

# Figure out backfill_end date if not supplied.
# Express below will return a date string of the
# form "2017-08-21"
if BACKFILL_END is None:
    BACKFILL_END = str(datetime.datetime.now())[:10]

# Create DB client
influxDB = bgfi.db_connect(host=HOST, database=DBNAME, client_type="dataframe")

# Create the DB if it doesn't exist yet
if not bgfi.db_exists(influxDB, DBNAME):
    msg = "Database {} does not exist in InfluxDB running at {}.\n Creating it.\n"
    sys.stdout.write(msg.format(DBNAME, HOST))
    influxDB.create_database(DBNAME)
else:
    msg = "Database {} already exists at {}! Not overwriting it.\n"
    sys.stdout.write(msg.format(DBNAME, HOST))

# Yahoo shut down support for the historical_data endpoint on its API
# in June 2017. But you can get around it because fuck them:
# https://stackoverflow.com/a/44050039
response = requests.get("https://finance.yahoo.com/quote/AAPL/history")

# Pull a historical dataset for each series
for ticker in TICKERS:

    msg = "Beginning backfill for {} from Yahoo Finance.\n"

    # Get the historical dataset
    histDF = bgfi.get_historical_data(ticker)

    # Extract close price, ticker, date

    # Interpolate to get a 5-minutely dataset

    # Format the points for upload to influxDB

    # Upload to influxDB
    influxDB.write_points([json_body])
    sys.stdout.write("Done backfilling ")


# Only run while the market is open
while True:

    # If the market is closed, sleep for a while
    if 

while (dt.hour == 9 & dt.minute > 30) | (dt.hour >10 & dt.hour < 16):

    # Get prices and write them out to the DB
    for ticker, yahoo_client in ticker_info.items():
        try:
            json_body = {"measurement": ticker,
                         "tags": {
                            "source": "Yahoo Finance"
                         },
                         "fields": {
                            "value": round(float(yahoo_client.get_price()),6)
                         }}

            # Write to the DB
            influxDB.write_points([json_body])
        except Exception as e:
            sys.stdout.write("macro_producer.py failed with error: {}\n".format(e))

    # chill out for 1 minute
    time.sleep(60)


# NOTE: Why are there no timestamps?
#
#   Timestamps in influxDB are optional:
#   https://docs.influxdata.com/influxdb/v1.3/guides/writing_data/
#   Since this is a "time right now" process, we don't need to do a bunch
#   of work figuring out timestamps
