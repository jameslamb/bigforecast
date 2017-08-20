import pandas as pd
import os


def extract_fields(row):
    """
    Takes the interesting things out of a row in a dataframe and returns
    a dictionary of them.
    """
    # Perhaps we'll want all the actor information, but this for now.
    cols_to_keep = ["GlobalEventID", "Day", "MonthYear",
                    "DATEADDED", "SOURCEURL", "NumMentions",
                    "NumSources", "NumArticles", "AvgTone",
                    "GoldsteinScale", "EventRootCode", "QuadClass",
                    "timestamp"]
    return dict(row[cols_to_keep])


# Global var with list of names in GDELT results
GDELT_COLS = [
    "GlobalEventID",
    "Day",
    "MonthYear",
    "Year",
    "FractionDate",
    "Actor1Code",
    "Actor1Name",
    "Actor1CountryCode",
    "Actor1KnownGroupCode",
    "Actor1EthnicCode",
    "Actor1Religion1Code",
    "Actor1Religion2Code",
    "Actor1Type1Code",
    "Actor1Type2Code",
    "Actor1Type3Code",
    "Actor2Code",
    "Actor2Name",
    "Actor2CountryCode",
    "Actor2KnownGroupCode",
    "Actor2EthnicCode",
    "Actor2Religion1Code",
    "Actor2Religion2Code",
    "Actor2Type1Code",
    "Actor2Type2Code",
    "Actor2Type3Code",
    "IsRootEvent",
    "EventCode",
    "EventBaseCode",
    "EventRootCode",
    "QuadClass",
    "GoldsteinScale",
    "NumMentions",
    "NumSources",
    "NumArticles",
    "AvgTone",
    "Actor1Geo_Type",
    "Actor1Geo_Fullname",
    "Actor1Geo_CountryCode",
    "Actor1Geo_ADM1Code",
    "Actor1Geo_ADM2Code",
    "Actor1Geo_Lat",
    "Actor1Geo_Long",
    "Actor1Geo_FeatureID",
    "Actor2Geo_Type",
    "Actor2Geo_Fullname",
    "Actor2Geo_CountryCode",
    "Actor2Geo_ADM1Code",
    "Actor2Geo_ADM2Code",
    "Actor2Geo_Lat",
    "Actor2Geo_Long",
    "Actor2Geo_FeatureID",
    "ActionGeo_Type",
    "ActionGeo_Fullname",
    "ActionGeo_CountryCode",
    "ActionGeo_ADM1Code",
    "ActionGeo_ADM2Code",
    "ActionGeo_Lat",
    "ActionGeo_Long",
    "ActionGeo_FeatureID",
    "DATEADDED",
    "SOURCEURL"
]

def split_v2_GDELT(update_file):
    """
    This function reads a GDELT CSV file and parses each row \
    and splits it up to be fed to the kafka topic one at a time. \n

    Args:
        update_file (str): a full path to a zipp CSV with GDELT data \n

    Returns:
        An iterable object with one event/article per item. \n
    """

    # Read in the CSV with GDELT events 2.0 data
    gdeltDF = pd.read_csv(update_file,
                          sep="\t",
                          header=None,
                          compression="zip",
                          names=GDELT_COLS)

    # Convert Dates to proper date strings
    gdeltDF['timestamp'] = gdeltDF['DATEADDED'].apply(_format_gdelt_date)

    # Return a list of rows (one per article)
    return list(gdeltDF.apply(extract_fields, 1))


def _format_gdelt_date(date_num):
    """
    Given dates from GDELT of the form "20170819204500", convert to
    proper timestamps of the form "2017-08-19 20:45:00".
    """

    # Check inputs
    assert isinstance(date_num, int) or isinstance(date_num, float)

    # Convert to character
    date_str = str(int(date_num))

    # Extract components. God I hope this doesn't break
    out_str = date_str[:4] + "-" + \
              date_str[4:6] + "-" + \
              date_str[6:8] + " " + \
              date_str[8:10] + ":" + \
              date_str[10:12] + ":" + \
              date_str[12:14]

    return(out_str)
