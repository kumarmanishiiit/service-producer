from kafka import KafkaProducer
import json
import os
import sqlite3

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "192.168.1.21:9092")
TOPIC_NAME = os.getenv("TOPIC_NAME", "delete-entry")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_event(data):
    print(TOPIC_NAME)
    producer.send(TOPIC_NAME, value=data)
    producer.flush()

    name = data.get('name')
    ip = data.get('ip')
    health_check_url = data.get('health_check_url')

send_event({"name": "Manish", "ip": "192.168.1.23", "health_check_url": "http://192.168.1.22:5000/health"})
