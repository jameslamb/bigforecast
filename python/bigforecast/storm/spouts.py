from __future__ import absolute_import, print_function, unicode_literals

from kafka import KafkaConsumer
import json
from streamparse.spout import Spout
import random
import subprocess
from bigforecast.gdelt.split_gdelt import split_v2_GDELT
import time

class KafkaArticleSpout(Spout):

    outputs = ['article']

    def initialize(self, stormconf, context):

        # Set up the consumer
        self.consumer = KafkaConsumer('GDELT_articles',
                         bootstrap_servers='kafka1:9092')

    def next_tuple(self):
        msg = next(self.consumer)
        self.log("Pulled msg off Kafka que: " + str(msg))
        msg_dict = json.loads(msg)
        out_tuple = []
        out_tuple.append(json.dumps(msg_dict))
        self.emit(out_tuple)


    def ack(self, tup_id):
        pass  # if a tuple is processed properly, do nothing

    def fail(self, tup_id):
        pass  # if a tuple fails to process, do nothing

class SampleArticleSpout(Spout):
    """This spout just gives a few different article URLs"""

    outputs = ['article']

    def initialize(self, stormconf, context):

        self.urls = ["http://bleacherreport.com/articles/2728061-daycare-owner-recounts-using-mma-to-thwart-attempted-child-abduction?utm_source=cnn.com&utm_campaign=editorial&utm_medium=referral",
                "http://www.cnn.com/2017/08/18/entertainment/taylor-swift-social-media-wipe/index.html",
                "http://money.cnn.com/2017/08/15/technology/amazon-instant-pickup/index.html?iid=ob_homepage_tech_pool"]

    def next_tuple(self):
        msg = self.urls[random.randint(0,2)]
        msg_dict = {"url": msg}
        out_tuple = []
        out_tuple.append(json.dumps(msg_dict))
        self.emit(out_tuple)

    def ack(self, tup_id):
        pass  # if a tuple is processed properly, do nothing

    def fail(self, tup_id):
        pass  # if a tuple fails to process, do nothing


class SampleGDELTSpout(Spout):
    """This is a step up from the SampleArticleSpout in which it reads GDELT file,
    and uses the same functions kafka will use to extract it."""
    outputs = ['article']

    def initialize(self, stormconf, context):
        dl_url = "http://data.gdeltproject.org/gdeltv2/20170819204500.export.CSV.zip"
        dl_name = "20170819204500.export.CSV.zip"
        subprocess.call(["wget", "-O", dl_name, dl_url])
        self.log("Spout completed getting the file")
        self.articles = iter(split_v2_GDELT(dl_name))
        self.log("Spout completed parsing hte file")

    def next_tuple(self):
        try:
            msg_dict = next(self.articles)
            out_tuple = []
            out_tuple.append(json.dumps(msg_dict))
            self.emit(out_tuple)
        except Exception as e:
            self.log(str(e))
            self.log("Completed emitting events.")
            time.sleep(10)

    def ack(self, tup_id):
        pass  # if a tuple is processed properly, do nothing

    def fail(self, tup_id):
        pass  # if a tuple fails to process, do nothing
