from kafka import KafkaProducer
import psycopg2
import json

conn = psycopg2.connect(
    dbname="postgres", user="username", password="1234", host="postgres", port="5433"
)

producer = KafkaProducer(bootstrap_servers="localhost:9092")

with conn.cursor() as cur:
    cur.execute("SELECT * FROM shahkar_user_apilog")
    rows = cur.fetchall()
    for row in rows:
        producer.send("api_log", json.dumps(row).encode("utf-8"))

producer.flush()
conn.close()
