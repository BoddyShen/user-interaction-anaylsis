from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'user_interactions',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='user-interactions-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    print(f"Partition: {message.partition}, Offset: {message.offset}, Key: {message.key}, Value: {message.value}")