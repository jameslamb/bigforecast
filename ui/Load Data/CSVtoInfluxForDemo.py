#Read data from csv and input into influx db:

import csv
import datetime
import pytz
import time
import argparse
from influxdb import InfluxDBClient

#variables that are needed
measurement = "stockpricedemo"
csvname = "stockdatafordemo.csv"

#####functions
def dateToUnixConverter(date):
    date_convert = [date.split(" ")[0].split("/"), date.split(" ")[1].split(":")]
    dateDT = datetime.datetime(int(date_convert[0][0]), int(date_convert[0][1]), int(date_convert[0][2]), \
                               int(date_convert[1][0])-3, int(date_convert[1][1]), int(date_convert[1][2]))
    return int(time.mktime(dateDT.timetuple()))*1000000000


###open file, iterate through each row, storing the stock prices for 4 stocks for each row/time sample
with open(csvname, 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        print (row)
        date = row[0]
        stocks = ["uso", "cad", "goog", "aapl"]
        for counter in range(len(stocks)):
            this_stock = counter
            json_body = [
                {
                    "measurement": measurement,
                    "tags": {
                        "ticker": stocks[counter]
                    },
                    "time": dateToUnixConverter(date),
                    "fields": {
                        "price": float(row[counter + 1]),
                         "VAR1": float(row[5]),
                         "VAR2": float(row[6]),
                         "VAR3": float(row[7])}
                }
            ]
            #save the json into influx, added flag for easy testing in environemnts where influx does not exist
            if True:       
                host='localhost'
                port=8086
                user = 'root'
                password = 'root'
                dbname = 'mydb'
                client = InfluxDBClient(host, port, user, password, dbname)
                print("Write points: {0}".format(json_body))
                client.write_points(json_body)
