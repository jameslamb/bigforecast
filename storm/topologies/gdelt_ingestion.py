"""
bigforecast GDELT ingestion topology
"""

from bigforecast.storm.bolts import ScraperBolt
from bigforecast.storm.bolts import AnalyzerBolt
from bigforecast.storm.bolts import ESLoaderBolt

from bigforecast.storm.spouts import KafkaArticleSpout

# Other imports
from streamparse import Grouping, Topology


class gdeltTopology(Topology):
    article_spout = KafkaArticleSpout.spec(par=1, name="gdelt-spout")

    scraper_bolt = ScraperBolt.spec(inputs=[article_spout],
                                    par=8,
                                    name='web-scraper-bolt')

    analyzer_bolt = AnalyzerBolt.spec(inputs=[scraper_bolt],
                                    par=8,
                                    name='analyzer-bolt')

    loader_bolt = ESLoaderBolt.spec(inputs=[analyzer_bolt],
                                    par=8,
                                    name='loader-bolt')
