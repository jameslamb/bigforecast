"""
bigforecast GDELT ingestion topology
"""

from bigforecast.storm.bolts import ScraperBolt
from bigforecast.storm.bolts import AnalyzerBolt
from bigforecast.storm.bolts import ESLoaderBolt

from bigforecast.storm.spouts import KafkaArticleSpout
from bigforecast.storm.spouts import SampleArticleSpout
from bigforecast.storm.spouts import SampleGDELTSpout

# Other imports
from streamparse import Grouping, Topology


class gdeltTopology(Topology):
    article_spout = SampleGDELTSpout.spec(par=1, name="gdelt-spout")

    scraper_bolt = ScraperBolt.spec(inputs=[article_spout],
                                    par=1,
                                    name='web-scraper-bolt')

    analyzer_bolt = AnalyzerBolt.spec(inputs=[scraper_bolt],
                                    par=1,
                                    name='analyzer-bolt')

    loader_bolt = ESLoaderBolt.spec(inputs=[analyzer_bolt],
                                    par=1,
                                    name='loader-bolt')
