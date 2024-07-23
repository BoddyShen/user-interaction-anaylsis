import pandas as pd
import s3fs
from dotenv import load_dotenv
import os
import time

load_dotenv(".env.spark")

aws_access_key = os.getenv('AWS_ACCESS_KEY')
aws_secret_key = os.getenv('AWS_SECRET_KEY')
s3_endpoint = os.getenv('S3_ENDPOINT')

bucket_name = 'customer-interactions-for-hudi'
parquet_path = 'user-interaction-data'  

s3 = s3fs.S3FileSystem(key=aws_access_key, secret=aws_secret_key)

# List all Parquet files in S3
parquet_files = s3.glob(f's3://{bucket_name}/{parquet_path}/*.parquet')
print(f"Found {len(parquet_files)} parquet files.")

# If no files are found, print the path and exit
if not parquet_files:
    print(f"No Parquet files found at s3://{bucket_name}/{parquet_path}")
    exit()

# Timer start
start_time = time.time()

# Read all Parquet files using Pandas and merge them
df_list = []
for parquet_file in parquet_files:
    print(f"Reading {parquet_file}")
    try:
        df = pd.read_parquet(parquet_file, filesystem=s3)
        df_list.append(df)
        print(f"Successfully read {parquet_file}")
    except Exception as e:
        print(f"Failed to read {parquet_file}: {e}")

# Combine all DataFrames
if df_list:
    combined_df = pd.concat(df_list, ignore_index=True)
    print(combined_df.head())
else:
    print("No DataFrames to concatenate")

if not df_list:
    print("No DataFrames were read. Exiting.")
    exit()

summary_df = combined_df.groupby(['user_id', 'interaction_type']).size().reset_index(name='count')

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")

print(summary_df)