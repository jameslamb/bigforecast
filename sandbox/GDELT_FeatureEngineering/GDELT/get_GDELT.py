# Python script for downloading and parsing GDELT data

#import pandas
import subprocess
import sys
import os

DATA_DIR = "/data/"
example_url = "http://data.gdeltproject.org/gdeltv2/20170718201500.export.CSV.zip"

def get_file(file_date, version, file_time=None):
    """
    Downloads the GDELT file at the given URL

    Expects Date as ISO 8601 Format: YYYY-MM-DD
    """

    if version == 1:
        print(file_date)

        #file_date = file_date.isoformat()
        file_date = str(file_date).replace("-", "")
        url = "http://data.gdeltproject.org/events/" + file_date + ".export.CSV.zip"
        dl_name = "data/" + file_date + ".CSV.zip"
        print(url)
    else:
        file_time = str(file_time).replace("-", "") # need to check time formats
        file_date = str(file_date).replace("-", "")

    if dl_name not in os.listdir(os.getcwd()):
        subprocess.call(["wget", "-O", dl_name, url])

    else:
        print("Already downloaded file")

# 1.0 example http://data.gdeltproject.org/events/20170718.export.CSV.zip
# 2.0 example http://data.gdeltproject.org/gdeltv2/20170718201500.export.CSV.zip
# 2.0 example is 2017-07-18 20:15:00 

if __name__ == "__main__":
    if "20170718201500.export.CSV.zip" not in os.listdir(os.getcwd()):
        get_file(file_date = "2017-07-18", version = 1)
