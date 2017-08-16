import csv  
import datetime
import time

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
    
dt = datetime.datetime.now(tz=EST5EDT())

while (dt.hour == 9 & dt.minute > 30) | (dt.hour >10 & dt.hour < 16):
    from yahoo_finance import Share
    oil = Share('uso')
    cad = Share('cad')
    goog = Share('goog')
    aapl = Share('aapl')
    
    print(oil.get_price())
    print(cad.get_price())
    print(goog.get_price())
    print(aapl.get_price())

    
    dt = datetime.datetime.now(tz=EST5EDT())
    year = str(dt.year)
    month = str(dt.month)
    day = str(dt.day)
    hour = str(dt.hour)
    minute = str(dt.minute)
    second = str(dt.second)

    row = [year+"/"+month+"/"+day+" "+hour+":"+minute+":"+second , \
        str(oil.get_price()) , str(cad.get_price()) , str(goog.get_price()) , str(aapl.get_price())]
    print(row)
    
     

    with open('stockdata.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)

    time.sleep(15*60) 