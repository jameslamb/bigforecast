#!/usr/bin/env python

import json
from kafka import KafkaProducer
import sys
import time
import bigforecast as bgf
import uuid
import os
import subprocess

# TODO (jaylamb20@gmail.com):
# read in hostname(s) from environment instead of localhost
# Set up producer running on localhost:9092
sys.stdout.write('Starting package metadata producer...\n')
BOOTSTRAP_SERVERS = ['localhost:9092']
#GDELT_producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS,
#                               value_serializer=lambda v: json.dumps(v).encode('utf-8'))
sys.stdout.write('Producer running on localhost:9092\n')

while True:

    # Grab the GDELT master files list
    sys.stdout.write('Pulling GDELT master file list...')

    # Grab the master list of files
    gdelt_files = bgf.gdelt.get_master_file_list()

    # Put the IDs and file URLs on the topic
    for file_info in gdelt_files:

        try:
            # TODO (jaylamb20@gmail.com):
            # --- add some logic for checking if we've seen this file?
            # Log out current file
            msg = "We have not processed {} yet! Pulling it...\n"
            sys.stdout.write(msg.format(file_info['url']))

            # Pull down the CSV from GDELT
            out_name = os.path.join('/tmp/', str(uuid.uuid4()) + '.zip')
            subprocess.call(["wget", "-O", out_name, file_info['url']])

            # Parse through all the events in the file and put them onto
            # the "GDELT_articles" Kafka topic
            events = bgf.gdelt.split_v2_GDELT(json.dumps(out_name))
            for event in events:
                #GDELT_producer.send("GDELT_articles", event)
                sys.stdout.write(str(event))

            subprocess.call(["rm", out_name])

        except Exception as e:
            sys.stdout.write(str(e) + '\n')

    sys.stdout.write('done\n\n')

    # Sleep for a bit (we can turn this off later if we want)
    time.sleep(5)
