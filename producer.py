import json
import time
from faker import Faker
from kafka import KafkaProducer
import uuid

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    linger_ms=10,  # Batch for 10 milliseconds
    batch_size=32 * 1024  # Batch size of 32 KB
)

def generate_interaction_data(max_messages=20):
    count = 0
    while count < max_messages:
        interaction_type = fake.random_element(elements=('click', 'view', 'purchase'))
        interaction_data = {
            'interaction_id': str(uuid.uuid4()),
            'user_id': fake.random_element(elements=(1, 2, 3, 4, 5)),
            'timestamp': fake.date_time_this_year().isoformat(),
            'interaction_type': interaction_type,
            'page_id': fake.random_element(elements=('home', 'search', 'product', 'checkout')),
            'referrer': fake.url(),
            'amount': fake.random_int(min=1, max=100) if interaction_type == 'purchase' else None
        }
        partition_key = {
            'click': 0,
            'view': 1,
            'purchase': 2
        }[interaction_type]
        
        try:
            producer.send('user_interactions', value=interaction_data, partition=partition_key)
            print(f"Sent: {interaction_data} to partition: {partition_key}")
            count += 1
        except Exception as e:
            print(f"Failed to send message: {e}")

        # time.sleep(1)

if __name__ == '__main__':
    generate_interaction_data()
