from pyspark.sql import SparkSession
from faker import Faker
import pandas as pd

spark = (
    SparkSession.builder.appName("Spark PostgreSQL Integration")
    .config("spark.jars", "/opt/spark/jars/postgresql-42.2.23.jar")
    .getOrCreate()
)


fake = Faker()

data = [
    (
        fake.file_name(),
        fake.last_name(),
        fake.phone_number(),
        fake.address(),
        fake.ssn(),
        fake.date_of_birth(),
    )
    for _ in range(10000000)
]

df = pd.DataFrame(
    data=data,
    columns=[
        "first_name",
        "last_name",
        "phonenumber",
        "address",
        "national_id",
        "birthday",
    ],
)

spark_df = spark.createDataFrame(df)
jdbc_url = "jdbc:postgresql://postgres:5432/your_db"
properties = {
    "user": "your_username",
    "password": "your_password",
    "driver": "org.postgresql.Driver",
}

spark_df.write.jdbc(url=jdbc_url, table="user", mode="append", properties=properties)
