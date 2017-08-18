import csv
import datetime
import time
from yahoo_finance import Share
import argparse
from influxdb import InfluxDBClient
import datetime
import pytz
import time

#Notes for Producer:
#This script is meant to continuously run in the background.  When the stock market is open, the script pulls
#data from Yahoo finance every 15 minutes and saves it to a influx database called "mydb".
#Here, we assume that mydb is already set up in influx

#[prepping box - macro producer]
#[root@] pip install yahoo-finance
#[root@] vi macro_producer.py
#[root@] chmod +x macro_producer.py
#[root@] python macro_producer.py &
#[root@] pkill -f macro_producer.py

def dateToUnixConverter(date):
    date_convert = [date.split(" ")[0].split("/"), date.split(" ")[1].split(":")]
    dateDT = datetime.datetime(int(date_convert[0][0]), int(date_convert[0][1]), int(date_convert[0][2]), \
                               int(date_convert[1][0])-3, int(date_convert[1][1]), int(date_convert[1][2]))#,\
                               #tzinfo = est)
    return int(time.mktime(dateDT.timetuple()))*1000000000


class EST5EDT(datetime.tzinfo):
    
    def utcoffset(self, dt):
        return datetime.timedelta(hours=-5) + self.dst(dt)
    
    def dst(self, dt):
        d = datetime.datetime(dt.year, 3, 8)
        self.dston = d + datetime.timedelta(days=6-d.weekday())
        d = datetime.datetime(dt.year, 11, 1)
        self.dstoff = d + datetime.timedelta(days=6-d.weekday())
        if self.dston <= dt.replace(tzinfo=None) < self.dstoff:
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(0)

    def tzname(self, dt):
        return 'EST5EDT'


dt = datetime.datetime.now(tz=EST5EDT())

while (dt.hour == 9 & dt.minute > 30) | (dt.hour >10 & dt.hour < 16):
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
           
    host='localhost'
    port=8086
    user = 'root'
    password = 'root'
    dbname = 'mydb'
    client = InfluxDBClient(host, port, user, password, dbname)
    ticker = ["uso", "cad", "goog", "aapl"]
    prices = [float(oil.get_price()) , float(cad.get_price()) , float(goog.get_price()) , float(aapl.get_price())]
    for counter in range(len(ticker)):
        json_body = [{
                     "measurement": "stockprice",
                     "tags": {
                     "ticker": ticker[counter]
                     },
                     "time": dateToUnixConverter(year+"/"+month+"/"+day+" "+hour+":"+minute+":"+second),
                            "fields": {
                     "price": prices[counter]}
                     }]

        print("Write points: {0}".format(json_body))
        client.write_points(json_body)
               
    time.sleep(15*60)

