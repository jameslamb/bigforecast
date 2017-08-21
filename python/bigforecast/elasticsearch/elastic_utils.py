import json
import pandas as pd
import requests


def doc_count(es_host, es_index, query=None, feature_name="doc_count",
              start_time="now-1w", end_time="now", window_size="15m"):
    """
    Hit an Elasticsearch index and return a Pandas Series \
    (with a DateTimeIndex) where each value is the count \
    of documents matching some date_histogram query \
    in the index for the preceding 15 minutes. If no query \
    is given, just returns counts of all docs. \n

    Args:
        es_host (str): A hostname for an Elasticsearch cluster \n
        es_index (str): Index in that Elasticsearch cluster to hit \n
        query (dict): A dictionary representing an ES query. \n
        feature_name (str): Name to give to the resulting count vector. \n
        start_time (str): Any valid date string to pass to \
            Elasticsearch. This param indicates the earliest date \
            to pull data from. \n
        end_time (str): Any valid date string to pass to \
            Elasticsearch. This param indicates the latest date \
            to pull data from. \n
        window_size (str): Any valid datemath string to be \
            passed to an Elasticsearch query. e.g. "1h" for \
            "1 hour", "10m" for "10 minutes", "1d" for \
            "1 day". \n
    Returns:
        Series: A pandas Series with counts of matching documents
    """

    # Check inputs
    assert isinstance(es_host, str)
    assert isinstance(es_index, str)
    assert isinstance(query, str)
    assert isinstance(start_time, str)
    assert isinstance(end_time, str)
    assert isinstance(window_size, str)

    # Create URL to hit
    query_url = _make_query_url(es_host, es_index)

    # Default query if none is given
    if query is None:
        query = {"size": 0,
                 "aggs": {
                    "time": {
                        "date_histogram": {
                        "field": "timestamp",
                        "min_doc_count": 0,
                        "interval": window_size
                      }
                    }
                  }
                }

    # Send query
    response = requests.get(url, data=json.dumps(query))

    # Parse date histogram response into a DataFrame
    aggs_json = json.loads(response.text)['aggregations']['time']['buckets']
    aggsDF = pd.DataFrame.from_records(aggs_json)[['key_as_string', 'doc_count']]

    # Create a time-series index from key_as_string
    aggsDF['time'] = pd.to_datetime(aggsDF['key_as_string'])
    aggsDF = aggsDF.set_index(aggsDF['key_as_string'])

    # Rename 'doc_count' to whatever feature name was requested
    aggsDF = aggsDF.rename(columns = {'doc_count': feature_name}, inplace=True)

    # Just return a series object
    return(aggsDF[feature_name])


def _make_query_url(es_host, es_index):
    """
    Construct URL for the Elasticsearch HTTP API.
    We should be using ONLY aggregations in this project,
    so the "size=0" trailing argument is hard-coded below.
    """

    return("{host}/{index}/_search?size=0".format(host=es_host, index=es_index))
