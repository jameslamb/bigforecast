# Python script for downloading and parsing GDELT data

#import pandas
import subprocess
import sys
import os


url = "http://data.gdeltproject.org/gdeltv2/20170718201500.export.CSV.zip"

def get_file(url):
    """Downloads the GDELT 2.0 file at the given URL"""
    subprocess.call(["wget", url])


if __name__ == "__main__":
    if "20170718201500.export.CSV.zip" not in os.listdir(os.getcwd()):
        get_file(url)
