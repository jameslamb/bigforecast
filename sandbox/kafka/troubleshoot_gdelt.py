#!/usr/bin/env python

import json
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

sys.stdout.write('Producer running on kafka cluster')
try:
    bgf.gdelt.create_log_DB()
    sys.stdout.write("Creating Log DB\n")
except:
    sys.stdout.write("Log DB Already Created\n")

while True:

    # Grab the GDELT master files list
    sys.stdout.write('Pulling GDELT master file list...\n')

    # Grab the master list of files
    gdelt_files = bgf.gdelt.get_master_file_list()
    gdelt_files = [name for name in gdelt_files if "export" in name['url']]

    # Put the IDs and file URLs on the topic
    for file_info in gdelt_files:
        print(file_info)
        try:
            # Check if file has been downloaded previously
            if bgf.check_file_downloaded(file_info['url']):
                msg = "We have already processed {}. \n\n\n"
                sys.stdout.write(msg.format(file_info['url']))
                continue

            msg = "We have not processed {} yet! Pulling it...\n"
            sys.stdout.write(msg.format(file_info['url']))

            # Pull down the CSV from GDELT
            out_name = os.path.join('/tmp/', str(uuid.uuid4()) + '.zip')
            subprocess.call(["wget", "-O", out_name, file_info['url']])

            # Parse through all the events in the file and put them onto
            # the "GDELT_articles" Kafka topic
            events = bgf.gdelt.split_v2_GDELT(out_name)

            subprocess.call(["rm", out_name])

            # Log that we've parsed this file.
            bgf.gdelt.log_file(file_info['url'])


        except Exception as e:
            sys.stdout.write(str(e) + '\n\n\n\n')

    sys.stdout.write('done\n\n')

    # Sleep for a bit (we can turn this off later if we want)
    time.sleep(5)
