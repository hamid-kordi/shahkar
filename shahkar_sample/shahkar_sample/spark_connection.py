from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = (
    SparkSession.builder.appName("Structured Streaming with PostgreSQL")
    .master("spark://spark-master:7077")
    .config("spark.jars", "/opt/spark/jars/postgresql-42.2.24.jar")
    .getOrCreate()
)

jdbc_url = "jdbc:postgresql://postgres:5433/postgres"
jdbc_properties = {
    "user": "username",
    "password": "1234",
    "driver": "org.postgresql.Driver",
}

logs_df = (
    spark.readStream.format("jdbc")
    .option("url", jdbc_url)
    .option("dbtable", "shahkar_user_apilog")
    .options(**jdbc_properties)
    .load()
)

processed_logs = logs_df.groupBy("analyzer_id").count()

query = processed_logs.writeStream.outputMode("complete").format("console").start()

query.awaitTermination()
