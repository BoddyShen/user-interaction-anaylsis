
# Project Structure
![Screenshot 2024-07-23 at 10 30 30 PM](https://github.com/user-attachments/assets/1772f355-f706-4865-9df3-e1f3d10939c9)

## Overview
This project demonstrates a data pipeline using Kafka, Spark, and AWS S3. The primary goal is to practice setting up and using Kafka for streaming data, Spark for processing data, and Docker Compose for managing services. The project includes a Kafka producer that generates fake user interaction data, Kafka as the message broker, Spark for processing the data, and AWS S3 for storing the processed data.

## How to Run
1. Build image: ``docker build -t da-spark-image .``
2. Use ``make run`` to run the docker-compose.
3. Submit the job to Spark:
  `docker cp jobs/kafka_to_S3.py spark-master:/opt/spark/app/kafka_to_S3.py` \
  `docker exec spark-master spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    /opt/spark/app/kafka_to_S3.py`
4. Run producer: `python3 producer.py`

## Components
### Kafka
Kafka is a distributed streaming platform that is used to build real-time data pipelines and streaming applications. It is designed to handle high throughput, fault tolerance, and horizontal scalability. Kafka allows you to publish and subscribe to streams of records, store them in a fault-tolerant manner, and process them in real-time.

### Spark
Apache Spark is a unified analytics engine for large-scale data processing. It provides high-level APIs in Java, Scala, Python, and R, and an optimized engine that supports general execution graphs. Spark is designed to perform both batch and streaming data processing, making it suitable for a wide range of applications.

### Docker Compose
Docker Compose is a tool for defining and running multi-container Docker applications. With Docker Compose, you can define the services, networks, and volumes needed for your application in a single docker-compose.yml file. This makes it easy to manage and scale complex applications composed of multiple interdependent services.
The Docker Compose configuration sets up the following services:

Zookeeper: Manages and coordinates Kafka brokers.
- Kafka: Message broker that handles the streaming data.
- Spark Master: The master node for the Spark cluster.
- Spark Worker: Worker nodes that execute Spark tasks.
- Spark History Server: Allows you to view Spark job history and logs.
