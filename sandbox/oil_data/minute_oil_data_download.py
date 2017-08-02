#!/usr/bin/env python3
'''#!/home/chris/anaconda3/bin/python3'''
import time
from yahoo_finance import Share

oil = Share("CL=F")
def get_price():
     oil.refresh()
     return oil.get_price(), time.time()

def log_minute_data():
    oil.refresh()
    price = oil.get_price()
    now = time.time()
    with open("minute_oil_data.csv", 'a') as f:
        f.write("\n" + str(price) + ", " + str(now))


if __name__ == "__main__":
    log_minute_data()
    print("logged data")
