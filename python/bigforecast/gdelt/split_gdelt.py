
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
                    "GoldsteinScale", "EventRootCode", "QuadClass"]
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

    # Return a list of rows (one per article)
    return list(gdeltDF.apply(extract_fields, 1))
