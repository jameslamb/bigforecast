import json
from streamparse.bolt import Bolt
from elasticsearch import Elasticsearch
from bigforecast.storm import newspaper_utils as npu

# Bolt 1: take in descriptions and write out a set of relationship tuples

# tuples.values definitions
# 0: json string of GDELT information
# 1: json string of article download information
# 2: json string of nlp performed by AnalyzerBolt

class ScraperBolt(Bolt):
    """
    Bolt which takes in the article from GDELT, then scrapes the web
    for the text and parses the keywords and passes it on to the loader bolt.
    """

    outputs = ['article', 'article_data']

    def initialize(self, conf, ctx):
        pass

    def process(self, tup):
        article_data = json.loads(tup.values[0])
        self.log("Recieved tuple: " + str(article_data["SOURCEURL"]))
        # If we can't download or parse the article, ignore it.
        try:
            article = npu.process_article(article_data["SOURCEURL"])
            out_tup = (tup.values[0], json.dumps(article))
            self.emit(out_tup)
            self.log("Emitted tuple: " + str(article_data["SOURCEURL"]))
        except Exception as e:
            self.log("Failed parsing article: " +  article_data["SOURCEURL"] + str(e))


class AnalyzerBolt(Bolt):
    """This bolt performs some basic nlp on the text for sentiment analysis"""

    outputs = ["article", "article_data", "article_analysis"]

    def initialize(self, conf, ctx):
        pass

    def process(self, tup):
        # Clearly needs more development, but I want to get this into the topology and test.
        nlp = {}
        try:
            article = json.loads(tup.values[1])
            nlp["oil_in_title"] = "oil" in article["title"]
            nlp_string = json.dumps(nlp)
        except Exception as e:
            print(e)

        out_tup = (tup.values[0], tup.values[1], nlp_string)
        self.emit(out_tup)


# Bolt 2: Take in parsed tuples and update DB
class ESLoaderBolt(Bolt):
    """This bolt takes the information from a parsed article and loads it into elasticesearch."""

    outputs = ['none']

    def initialize(self, conf, ctx):
        self.es = Elasticsearch([{"host": "elasticsearch1", "port": 9200}])

    def process(self, tup):
        article = {**json.loads(tup.values[0]),
                   **json.loads(tup.values[1]),
                   **json.loads(tup.values[2])}

        try:
            npu.load_article(article, self.es, article["GlobalEventID"], index = "test")
            #self.log("Loaded Article: " + str(article["GlobalEventID"]) + ": " +  article["title"])
        except Exception as e:
            self.log(str(e))
            #self.log("Failed to load article into ES:", article["title"])
