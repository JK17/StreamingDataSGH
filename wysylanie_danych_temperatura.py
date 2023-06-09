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
import numpy as np

TOPIC = "test2"

def prepare_temperature():
    
    number_of_points = 100
    center = 60
    scale = 5

    heating_duration = 70  # Czas trwania fazy grzewczej w iteracjach
    cooling_duration = 100  # Czas trwania fazy chłodzenia w iteracjach
    x = np.linspace(0, number_of_points, number_of_points)
    y = [y for y in 40 * np.sin(x * (np.pi / heating_duration)) + center + np.random.normal(0, scale, number_of_points)]
    y = [temp if temp <= 95 else 94 + np.random.random() for temp in y]
    y = [temp if temp >= 25 else 25 + np.random.random() for temp in y]

 

    # Symulowanie fazy grzewczej i chłodzenia
    for i in range(1, len(y) - 1):
        if i % (heating_duration + cooling_duration) < heating_duration:
            y[i] += np.random.normal(0, 2)  # Dodatkowy wzrost temperatury w fazie grzewczej
            y[i] = max(y[i-1], y[i])  # Utrzymywanie wartości rosnącej
        else:
            cooling_factor = np.random.uniform(0.8, 1.0)  # Współczynnik chłodzenia
            y[i] = y[i-1] * cooling_factor  # Spadek temperatury w fazie chłodzenia

    return y

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg.value()), str(err)))
    else:
        print("Message produced: %s" % (str(msg.value())))


def main():
    conf = {'bootstrap.servers': "broker:9092",
            'client.id': socket.gethostname()}
    producer = Producer(conf)
    temperature_results = prepare_temperature()
    
    for temperature_ in temperature_results:
        timestamp = datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y %H:%M:%S:%f")
        temperature = temperature_
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