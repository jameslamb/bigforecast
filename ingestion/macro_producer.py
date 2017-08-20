#!/usr/bin/env python

# Load Dependencies
import bigforecast.influx as bgf
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

# Create yahoo-finance clients for whatever tickers
# the user specified in macro_config.json
ticker_info = {ticker: Share(ticker) for ticker in TICKERS}

# Create DB client
influxDB = bgf.db_connect(host=HOST, database=DBNAME)

# Create the DB if it doesn't exist yet
if not bgf.db_exists(influxDB, DBNAME):
    msg = "Database {} does not exist in InfluxDB running at {}. Creating it.\n"
    sys.stdout.write(msg.format(DBNAME, HOST))
    influxDB.create_database(DBNAME)
else:
    msg = "Database {} already exists at {}! Not overwriting it.\n"
    sys.stdout.write(msg.format(DBNAME, HOST))

# Only run while the market is open
#while (dt.hour == 9 & dt.minute > 30) | (dt.hour >10 & dt.hour < 16):
while True:

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
            sys.stdout.write("macro_producer.py failed with error: {}".format(e))

    # chill out for 1 minute
    time.sleep(60)


# NOTE: Why are there no timestamps?
#
#   Timestamps in influxDB are optional:
#   https://docs.influxdata.com/influxdb/v1.3/guides/writing_data/
#   Since this is a "time right now" process, we don't need to do a bunch
#   of work figuring out timestamps
