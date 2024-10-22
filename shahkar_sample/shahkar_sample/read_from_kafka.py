from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Kafka to Spark") \
    .getOrCreate()

kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "api_log") \
    .load()

processed_logs = kafka_df.selectExpr("CAST(value AS STRING)")

query = processed_logs.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
