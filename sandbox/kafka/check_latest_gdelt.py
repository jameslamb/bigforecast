import subprocess
import sys
#from kafka import KafkaProducer


sys.stdout.write('Starting package metadata producer...\n')
#GDELT_producer = KafkaProducer(bootstrap_servers = "localhost:9092",
                               #value_serializer = lambda v: json.dumps(v).encode("utf-8"))
sys.stdout.write('Producer running on localhost:9092\n')


check_latest_url = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"
last_ingested_file = "last_ingested.txt"
last_update_file = "lastupdate.txt"

subprocess.call(["wget","-O", last_update_file, check_latest_url])

def get_output_name(update_file):
    with open(update_file, 'r') as f:
        return f.readline().split(" ")[-1][:-1]

#while True: #uncomment this when hooking up to Kafka

if __name__ == "__main__":
    latest_update = get_output_name(last_update_file)
    try:
        latest_ingested = get_output_name(last_ingested_file)
    except IOError:
        latest_ingested = None

    if latest_update != latest_ingested:
        dl_name = latest_update.split("/")[-1]
        try:
            print("Getting file:", latest_update)
            subprocess.call(["wget", "-O", dl_name, latest_update])
            subprocess.call(["mv", last_update_file, last_ingested_file])
            new_file = True
        except:
            print("Unable to get latest file!")
    else:
        print("We already have the latest file!")

    # We downloaded the file, now parse and load to kafka.
    if new_file is True:

        events = split_v2_GDELT(dl_name)
        for event in event:
            #GDELT_producer.send("GDELT_article": event)
            pass
