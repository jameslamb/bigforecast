import json
from streamparse.bolt import Bolt
from elasticsearch import Elasticsearch
from bigforecast.storm import newspaper_utils as npu

# Bolt 1: take in descriptions and write out a set of relationship tuples

# tuples definition
# 0: Storm tuple ID
# 1: json string of GDELT information
# 2: json string of article download information
# 3: json string of nlp performed by AnalyzerBolt

class ScraperBolt(Bolt):
    """
    Bolt which takes in the article from GDELT, then scrapes the web
    for the text and parses the keywords and passes it on to the loader bolt.
    """

    outputs = ['article', 'article_data']

    def initialize(self):
        pass

    def process(self, tup):
        article_data = json.loads(tup[1])
        article = npu.process_article(article_data["url"])
        tup.append(article)

        # emit package-dependency tuples
        self.log('Parsed deps: ' + article[""])
        self.emit(out_tup)


class AnalyzerBolt(Bolt):
    """This bolt performs some basic nlp on the text for sentiment analysis"""
    outputs = ["article", "article_data", "article_analysis"]

    def initialze(self):
        pass

    def process(self, tup):
        # Clearly needs more development, but I want to get this into the topology and test.
        nlp = {}
        article = json.loads(tup[2])
        nlp["oil_in_title"] =  "1" if "oil" in article["title"] else "0"
        nlp_string = json.dumps(nlp)

        tup.append(nlp_string)
        self.emit(tup)


# Bolt 2: Take in parsed tuples and update DB
class ESLoaderBolt(Bolt):
    """This bolt takes the information from a parsed article and loads it into elasticesearch."""

    outputs = ['none']

    def initialize(self, conf, ctx):
        self.es = Elasticsearch([{"host": "elasticsearch1", "port": 9200}])

    def process(self, tup):
        article = {**json.loads(tup[1]),
                   **json.loads(tup[2]),
                   **json.loads(tup[3])}

        npu.load_article(article)
