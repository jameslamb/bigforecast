#Macro Producer that Inputs into influx db:

import csv
import datetime
import pytz
import time
import argparse
from influxdb import InfluxDBClient
from yahoo_finance import Share


measurement = "tablename"
#####functions

def dateToUnixConverter(date):
    #est = pytz.timezone('America/New_York')
    date_convert = [date.split(" ")[0].split("/"), date.split(" ")[1].split(":")]
    dateDT = datetime.datetime(int(date_convert[0][0]), int(date_convert[0][1]), int(date_convert[0][2]), \
                           int(date_convert[1][0])-3, int(date_convert[1][1]), int(date_convert[1][2]))#,\
                          #tzinfo = est)
    return int(time.mktime(dateDT.timetuple()))*1000000000

class EST5EDT(datetime.tzinfo):

    def utcoffset(self, dt):
        return datetime.timedelta(hours=-5) + self.dst(dt)

    def dst(self, dt):
        d = datetime.datetime(dt.year, 3, 8)        #2nd Sunday in March
        self.dston = d + datetime.timedelta(days=6-d.weekday())
        d = datetime.datetime(dt.year, 11, 1)       #1st Sunday in Nov
        self.dstoff = d + datetime.timedelta(days=6-d.weekday())
        if self.dston <= dt.replace(tzinfo=None) < self.dstoff:
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(0)

    def tzname(self, dt):
        return 'EST5EDT'

###open file, iterate through each row, storing the stock prices for 4 stocks for each row/time sample

dt = datetime.datetime.now(tz=EST5EDT())

while (dt.hour == 9 & dt.minute > 30) | (dt.hour >10 & dt.hour < 16):
    
    #pulling stock price data from Yahoo
    oil = Share('uso')
    cad = Share('cad')
    goog = Share('goog')
    aapl = Share('aapl')

    dt = datetime.datetime.now(tz=EST5EDT())
    year = str(dt.year)
    month = str(dt.month)
    day = str(dt.day)
    hour = str(dt.hour)
    minute = str(dt.minute)
    second = str(dt.second)

    row = [year+"/"+month+"/"+day+" "+hour+":"+minute+":"+second , \
           str(oil.get_price()) , str(cad.get_price()) , str(goog.get_price()) , str(aapl.get_price())]
    #print(row)

    #creating json datastructure to pass to influx
    date = year+"/"+month+"/"+day+" "+hour+":"+minute+":"+second
    stocks = ["uso", "cad", "goog", "aapl"]
    price = [oil.get_price() , cad.get_price(), goog.get_price(), aapl.get_price()]
    for counter in range(4):
        this_stock = counter
        json_body = [
            {
                "measurement": measurement,
                "tags": {
                    "ticker": stocks[counter]
                },
                "time": dateToUnixConverter(date),
                "fields": {
                    "price": row[counter + 1]}
            }
        ]
        #print(json_body)
        
        #saving to ifnflux DB, included flag for testing in an environment where influx does not exist
        if True:
            host='localhost'
            port=8086
            user = 'root'
            password = 'root'
            dbname = 'mydb'
            client = InfluxDBClient(host, port, user, password, dbname)
            print("Write points: {0}".format(json_body))
            client.write_points(json_body)

