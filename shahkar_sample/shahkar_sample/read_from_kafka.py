from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, count
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    FloatType,
    IntegerType,
    TimestampType,
)

spark = SparkSession.builder.appName("Kafka to Spark").getOrCreate()

schema = StructType(
    [
        StructField("timestamp", TimestampType(), nullable=True),
        StructField("task_id", StringType(), nullable=True),
        StructField("analyzer_id", StringType(), nullable=True),
        StructField("phonenumber", StringType(), nullable=True),
        StructField("response_time", FloatType(), nullable=True),
        StructField("result_time", TimestampType(), nullable=True),
        StructField("status", StringType(), nullable=True),
        StructField("request_size", IntegerType(), nullable=True),
    ]
)

kafka_df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "api_log")
    .load()
)


api_log_df = kafka_df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

aggregated_df = api_log_df.groupBy("analyzer_id").agg(
    count("*").alias("total_requests")
)

query = aggregated_df.writeStream.outputMode("complete").format("console").start()
query.awaitTermination()
