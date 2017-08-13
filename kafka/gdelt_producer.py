#!/usr/bin/env python

import json
from kafka import KafkaProducer
import sys
import time
import bigforecast as bgf

# TODO (jaylamb20@gmail.com):
# read in hostname(s) from environment instead of localhost
# Set up producer running on localhost:9092
sys.stdout.write('Starting package metadata producer...\n')
BOOTSTRAP_SERVERS = ['localhost:9092']
metadata_producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS,
                                  value_serializer=lambda v: json.dumps(v).encode('utf-8'))
sys.stdout.write('Producer running on localhost:9092\n')

while True:

    # Grab the GDELT master files list
    sys.stdout.write('Pulling GDELT master file list...')

    # Grab the master list of files
    gdelt_files = bgf.gdelt.get_master_file_list()

    # Put the IDs and file URLs on the topic
    for file_info in gdelt_files:

        # Write out to Kafka
        try:
            metadata_producer.send('GDELT_articles',
                                   {'article_id': file_info['id'],
                                    'article_url': file_info['url']})
        except Exception as e:
            sys.stdout.write(str(e) + '\n')

    sys.stdout.write('done\n\n')

    # Sleep for a bit (we can turn this off later if we want)
    time.sleep(5)
