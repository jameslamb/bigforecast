from __future__ import absolute_import, print_function, unicode_literals

from kafka import KafkaConsumer
import json
from streamparse.spout import Spout

class KafkaArticleSpout(Spout):

    outputs = ['package', 'description']

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
