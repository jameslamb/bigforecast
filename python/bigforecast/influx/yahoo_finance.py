
import datetime
from io import StringIO
import pandas as pd
import re
import requests
import time


def _get_yahoo_crumb_cookie():
    """
    Get Yahoo crumb cookie value. This is necessary to hit historical \
    data, since Yahoo disabled support for historical datasets \
    in June 2017.

    References:
        https://stackoverflow.com/a/44445027
    """
    res = requests.get('https://finance.yahoo.com/quote/SPY/history')
    yahoo_cookie = res.cookies['B']
    yahoo_crumb = None
    pattern = re.compile('.*"CrumbStore":\{"crumb":"(?P<crumb>[^"]+)"\}')
    for line in res.text.splitlines():
        m = pattern.match(line)
        if m is not None:
            yahoo_crumb = m.groupdict()['crumb']
    return yahoo_cookie, yahoo_crumb


def get_historical_data(ticker_symbol, retries=5, sleep_time=30):
    """
    Pull historical data from Yahoo Finance. This funciton defaults \
    to just pulling all data up to the moment it is called. \n

    Args:
        ticker_symbol (str): A valid ticker symbol string \
            to hit the Yahoo Finance API. \n
        retries (int): How many times should we try hitting \
            Yahoo Finance before giving up on a query? \n
        sleep_time (int): Time (in seconds) to sleep between \
            retries. \n

    References:
        https://stackoverflow.com/a/44445027 \n
        http://machinelearningmastery.com/resample-interpolate-time-series-data-python/ \n
        https://stackoverflow.com/questions/13035764/remove-rows-with-duplicate-indices-pandas-dataframe-and-timeseries \n
    """

    # Check inputs
    assert isinstance(ticker_symbol, str)

    # Go get the data from Yahoo. May have to try a few times
    retry_count = 0
    while True:
        try:
            # Re-request cookie info
            cookie_tuple = _get_yahoo_crumb_cookie()

            # Build up URL
            url_kwargs = {
                'symbol': ticker_symbol.upper(),
                'timestamp_end': int(time.time()),
                'crumb': cookie_tuple[1],  # yahoo cookie crumb -> str
            }
            url_price = 'https://query1.finance.yahoo.com/v7/finance/download/' \
                        '{symbol}?period1=0&period2={timestamp_end}&interval=1d&events=history' \
                        '&crumb={crumb}'.format(**url_kwargs)

            # Get data
            response = requests.get(url_price, cookies={'B': cookie_tuple[0]})
            break
        except Exception as e:
            if retry_count < retries:
                print("Hit error {}. Waiting for {} seconds.".format(e, sleep_time))
                retry_count += 1
                time.sleep(sleep_time)
            else:
                raise ValueError(e)
                break

    # Format response into a pandas DataFrame. Convert dates
    # and be sure you have a DateTimeIndex
    outDF = pd.read_csv(StringIO(response.text),
                        parse_dates=['Date'],
                        index_col=['Date'],
                        squeeze=False,
                        date_parser=lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))

    # It is possible to get back duplicate rows, because entropy always wins. 
    # Try to avoid this issue.
    # Shout out to the internet. See references.
    outDF = outDF[~outDF.index.duplicated(keep='first')]

    return(outDF)
