


def extract_value(row):
    """
    Takes the interesting things out of a row in a dataframe and returns
    a dictionary of them
    """

    # Check inputs
    

    # Perhaps we'll want all the actor information, but this for now.
    cols_to_keep = ["GlobalEventID", "Day", "MonthYear",
                    "DATEADDED", "SOURCEURL", "NumMentions",
                    "NumSources", "NumArticles", "AvgTone",
                    "GoldsteinScale", "EventRootCode", "QuadClass"]
    return dict(row[cols_to_keep])

def split_v2_GDELT(update_file):
    """
    This function reads a GDELT CSV file and parses each row and splits it up
    to be fed to the kafka topic one at a time.

    Input is a string of an output file_name
    Output is an iterable object which can be fed to kafka.
    """

    gdelt = pd.read_csv(update_file, sep = "\t", header = None, compression = "zip",
                        names = cols)