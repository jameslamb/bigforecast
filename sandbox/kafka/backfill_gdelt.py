import subprocess
import os
import sys
import pandas as pd
from split_v2_outputfile import split_v2_GDELT

from kafka import KafkaProducer


sys.stdout.write('Starting package metadata producer...\n')
GDELT_producer = KafkaProducer(bootstrap_servers = "localhost:9092",
                                  value_serializer=lambda v: json.dumps(v).encode('utf-8'))

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
        item = l.split(" ")[-1]
        if "export" in item:
            all_files.append(item)
        if not l: break

print(len(all_files))
print(all_files[0:6])

i = 0
while True:
    print("\n\n\n")
    next_file = all_files.pop(0)
    dl_name = next_file.split("/")[-1]
    print("next_file:", next_file)
    print("dl_name:", dl_name)
    print("\n\n\n")

    subprocess.call(["wget", "-O", dl_name, next_file])
    events = split_v2_GDELT(dl_name)
    for event in events:
        send_msg = GDELT_producer.send("GDELT_articles", event)
        #print(send_msg.value)
        #print(send_msg.success())

    subprocess.call(["rm", dl_name])

    if i > files_to_load:
        break
"""
dir(send_msg) = ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_call_backs', '_callbacks', '_errbacks', '_produce_future', '_produce_success', 'add_both', 'add_callback', 'add_errback', 'args', 'chain', 'error_on_callbacks', 'exception', 'failed', 'failure', 'get', 'is_done', 'retriable', 'succeeded', 'success', 'value']
"""
