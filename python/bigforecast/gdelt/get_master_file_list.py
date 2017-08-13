import requests
import sys


def get_master_file_list():
    """
    Get the list of all GDELT files available.

    Returns:
        list: a list of dictionaries with keys "id" and "url"
            corresponding to GDELT v2.0 events data files
    """

    # Read in the file
    url = "http://data.gdeltproject.org/gdeltv2/masterfilelist.txt"
    filelist = requests.get(url).text.split('\n')

    # Parse into a list
    out_list = []
    for file_info in filelist:
        try:
            metadata = file_info.split(' ')
            out_list.append({'id': metadata[0], 'url': metadata[2]})
        except IndexError:
            sys.stdout.write('Could not parse line in GDELT masterfile: ' + file_info)

    # Return this in reverse so the newer articles get checked first
    return(reversed(out_list))
