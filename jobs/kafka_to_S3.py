from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, IntegerType
import os

aws_access_key = os.getenv('AWS_ACCESS_KEY')
aws_secret_key = os.getenv('AWS_SECRET_KEY')
s3_endpoint = os.getenv('S3_ENDPOINT')
checkpoint_location = os.getenv('CHECKPOINT_LOCATION')
data_path = os.getenv('DATA_PATH')

spark = SparkSession.builder \
    .appName("KafkaToS3") \
    .config("spark.hadoop.fs.s3a.endpoint", s3_endpoint) \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("com.amazonaws.services.s3.enableV4", "true") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_key) \
    .config("fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .getOrCreate()

# Define schema for interaction data
schema = StructType([
    # StructField("interaction_id", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("interaction_type", StringType(), True),
    StructField("page_id", StringType(), True),
    StructField("referrer", StringType(), True),
    StructField("amount", IntegerType(), True)  # Only for purchases
])

# Read from Kafka
kafka_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9093") \
    .option("subscribe", "user_interactions") \
    .load()

# Deserialize JSON data
interaction_df = kafka_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Write to S3
query = interaction_df.writeStream \
    .format("parquet") \
    .option("path", data_path) \
    .option("checkpointLocation", checkpoint_location) \
    .start()

query.awaitTermination()