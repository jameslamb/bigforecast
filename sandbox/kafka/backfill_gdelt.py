import subprocess
import os
import sys
import pandas as pd
from split_v2_outputfile import split_v2_GDELT

#from kafka import KafkaProducer


sys.stdout.write('Starting package metadata producer...\n')
#GDELT_producer = KafkaProducer(bootstrap_servers = "localhost:9092",
                               #value_serializer = lambda v: json.dumps(v).encode("utf-8"))
sys.stdout.write('Producer running on localhost:9092\n')


files_to_load = 100000 #258022 total as of writing this
master_list_url = "http://data.gdeltproject.org/gdeltv2/masterfilelist.txt"
master_list = "masterfilelist.txt"

if master_list not in os.listdir(os.getcwd()):
    subprocess.call(["wget", "-O", master_list, master_list_url])

all_files = []

with open(master_list, 'r') as f:
    while True:
        l = f.readline()
        l = l.rstrip()
        all_files.append(l.split(" ")[-1])
        if not l: break

print(len(all_files))
print(all_files[0:6])

i = 0
while True:
    next_file = all_files.pop()
    dl_name = next_file.split("/")[-1]

    events = split_v2_GDELT(dl_name)
    for event in event:
        # GDELT_producer.send("GDELT_article": event)
        pass
    if i > files_to_load:
        break
