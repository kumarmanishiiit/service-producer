# consumer.py
from kafka import KafkaConsumer
import json
import os
import sqlite3
from datetime import datetime

DB_NAME = "monitoring.db"

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "192.168.1.21:9092")
TOPIC_NAME = os.getenv("TOPIC_NAME", "test-topic")

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def check_service_health(ip, health_check_url=None):
    return True
    # try:
    #     if health_check_url:
    #         url = f"http://{ip}{health_check_url}"
    #     else:
    #         url = f"http://{ip}/health"  # Default health check endpoint
        
    #     response = requests.get(url, timeout=5)
    #     return response.status_code == 200
    # except requests.RequestException:
    #     return False

# Register a new service or update existing
def register_service(name, ip, health_check_url=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute("SELECT * FROM services WHERE name = ?", (name,))
    existing_service = cursor.fetchone()
    
    # Check service health
    is_healthy = check_service_health(ip, health_check_url)
    status = 'UP' if is_healthy else 'DOWN'
    
    if existing_service:
        cursor.execute("UPDATE services SET ip = ?, status = ?, last_heartbeat = ?, health_check_url = ? WHERE name = ?", 
                      (ip, status, current_time, health_check_url, name))
    else:
        cursor.execute("INSERT INTO services (name, ip, status, last_heartbeat, health_check_url) VALUES (?, ?, ?, ?, ?)", 
                      (name, ip, status, current_time, health_check_url))
    
    conn.commit()
    conn.close()

def register(data):
    name = data.get('name')
    ip = data.get('ip')
    health_check_url = data.get('health_check_url')
    
    if not name or not ip:
        return jsonify({'error': 'Missing service name or IP'}), 400
    # print(data.value.get('name'))
    register_service(name, ip, health_check_url)
    # return jsonify({'message': f'Service {name} registered/updated'}), 200

for message in consumer:
    register(message.value)
    print(f"Received message: {message.value}")
