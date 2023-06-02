"""Generates a stream to Kafka from a time series csv file.
"""

import argparse
import csv
import json
import sys
import time
import datetime
from dateutil.parser import parse
from confluent_kafka import Producer
import socket

TOPIC = "test2"

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg.value()), str(err)))
    else:
        print("Message produced: %s" % (str(msg.value())))


def main():
    conf = {'bootstrap.servers': "broker:9092",
            'client.id': socket.gethostname()}
    producer = Producer(conf)

    while True:
        timestamp = datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y %H:%M:%S:%f")
        temperature = 40
        location = "Hala Katowice"
        kafka_key = location

        result = {}
        result["event_time"] = timestamp
        result["temperature"] = temperature
        result["location"] = location
        jresult = json.dumps(result)
        
        producer.produce(TOPIC, key=kafka_key, value=jresult, callback=acked)
       
        producer.flush()

        time.sleep(4)

if __name__ == "__main__":
    main()