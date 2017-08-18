import json
from streamparse.bolt import Bolt
from elasticsearch import Elasticsearch
import newspaper_utils as npu

# Bolt 1: take in descriptions and write out a set of relationship tuples
# tuples

# 0: storm tuple ID
# 1: json string of GDELT information
# 2: json string of article download information
# 3: json string of nlp performed by AnalyzerBolt

class ScraperBolt(Bolt):
    """
    Bolt which takes in the article from GDELT, then scrapes the web
    for the text and parses the keywords and passes it on to the loader bolt.
    """

    outputs = ['article', 'article_data']

    def initialize(self, conf, ctx):
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
    outputs = ["article", "article_data"]

    def initialze(self):
        pass

    def process(self, tup):
        nlp = {}
        article = json.loads(tup[2])
        nlp["oil_in_title": "1" if "oil" in article["title"] else "0"]
        nlp_string = json.dumps(nlp)

        tup.append(nlp_string)
        self.emit(tup)


# Bolt 2: Take in parsed tuples and update DB
class ESLoaderBolt(Bolt):
    """This bolt takes the information from a parsed article and loads it into elasticesearch."""

    outputs = ['none']

    def initialize(self, conf, ctx):
        self.es = Elasticsearch([{"host": "", "port": 9200}])

    def process(self, tup):
        article = {**tup[1], **tup[2]} # cool syntax!
        npu.load_article(article)
