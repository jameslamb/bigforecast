import time
from yahoo_finance import Share

oil = Share("CL=F")
def get_price():
     oil.refresh()
     return oil.get_price(), time.time()

