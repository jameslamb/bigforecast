from __future__ import absolute_import, print_function, unicode_literals

from kafka import KafkaConsumer
import json
from streamparse.spout import Spout
import random

class KafkaArticleSpout(Spout):

    outputs = ['article']

    def initialize(self, stormconf, context):

        # Set up the consumer
        self.consumer = KafkaConsumer('package_metadata',
                         bootstrap_servers='localhost:9092')

    def next_tuple(self):
        msg = next(self.consumer)
        msg_dict = json.loads(msg.value)
        out_tuple = (msg_dict['package'].encode('utf-8'), msg_dict['description'].encode('utf-8'))
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