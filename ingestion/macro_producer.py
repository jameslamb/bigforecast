#!/usr/bin/env python

# Load Dependencies
import bigforecast.influx as bgfi
import datetime
import json
from yahoo_finance import Share
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

# Create yahoo-finance clients for whatever tickers
# the user specified in macro_config.json. You can totally
# Share() for currencies which makes this easier.
ticker_info = {ticker: Share(ticker) for ticker in SYMBOLS}

# Create DB client
influxDB = bgfi.db_connect(host=HOST, database=DBNAME)

# Create the DB if it doesn't exist yet
if not bgfi.db_exists(influxDB, DBNAME):
    msg = "[{}] Database {} does not exist in InfluxDB running at {}. Creating it.\n"
    sys.stdout.write(msg.format(now(), DBNAME, HOST))
    influxDB.create_database(DBNAME)
else:
    msg = "[{}] Database {} already exists at {}! Not overwriting it.\n"
    sys.stdout.write(msg.format(now(), DBNAME, HOST))

# Only run while the market is open
# while (dt.hour == 9 & dt.minute > 30) | (dt.hour >10 & dt.hour < 16):
while True:

    # Get prices and write them out to the DB
    msg = "[{}] Pulling current prices for symbols in macro_config.\n"
    sys.stdout.write(msg.format(now()))
    for ticker, yahoo_client in ticker_info.items():
        try:
            json_body = {"measurement": ticker.replace('=X', ''),
                         "tags": {
                            "source": "Yahoo Finance",
                            "ingestion_process": "streaming",
                            "created_date": int(time.time())
                         },
                         "fields": {
                            "value": round(float(yahoo_client.get_price()),6)
                         }}

            # Write to the DB
            influxDB.write_points([json_body])
        except Exception as e:
            sys.stdout.write("[{}] (on {}) macro_producer.py failed with error: {}\n".format(now(), ticker, e))

    # chill out for 1 minute
    sys.stdout.write("[{}] Done with this round. Sleeping for 60 seconds.\n".format(now()))
    time.sleep(60)


# NOTE: Why are there no timestamps?
#
#   Timestamps in influxDB are optional:
#   https://docs.influxdata.com/influxdb/v1.3/guides/writing_data/
#   Since this is a "time right now" process, we don't need to do a bunch
#   of work figuring out timestamps
