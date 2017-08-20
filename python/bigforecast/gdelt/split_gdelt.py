
import pandas as pd
import pkg_resources


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


def split_v2_GDELT(update_file):
    """
    This function reads a GDELT CSV file and parses each row \
    and splits it up to be fed to the kafka topic one at a time. \n

    Args:
        update_file (str): a full path to a zipp CSV with GDELT data \n

    Returns:
        An iterable object with one event/article per item. \n
    """

    # Get ordered list of column names
    with open(pkg_resources.resource_filename("bigforecast", "gdelt/feature_names.txt"), "r") as f:
        cols = f.readlines()
    cols = list(map(lambda s: s.replace("\n", ""), cols))

    # Read in the CSV with GDELT events 2.0 data
    gdeltDF = pd.read_csv(update_file,
                          sep="\t",
                          header=None,
                          compression="zip",
                          names=cols)

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
