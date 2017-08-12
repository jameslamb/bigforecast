from kafka import KafkaConsumer
import json
import pickle
import sys
consumer = KafkaConsumer(bootstrap_servers='localhost:9092')
consumer.subscribe(["GDELT_articles"])

#for msg in consumer:
while True:
   msg = next(consumer)
   print(msg)
   #msg_dict = json.loads(msg.value)
   #print(msg_dict)
   #out_tuple = (msg_dict['package'], msg_dict['description'])
   #print(type(out_tuple))
   #print(out_tuple)
