#!/bin/bash

SPARK_WORKLOAD=$1

echo "SPARK_WORKLOAD: $SPARK_WORKLOAD"

case $SPARK_WORKLOAD in
  master)
    echo "Starting Spark master..."
    start-master.sh
    ;;
  worker)
    echo "Starting Spark worker..."
    start-worker.sh spark://spark-master:7077
    ;;
  history)
    echo "Starting Spark history server..."
    start-history-server.sh
    ;;
  *)
    echo "Unknown SPARK_WORKLOAD: $SPARK_WORKLOAD"
    exit 1
    ;;
esac