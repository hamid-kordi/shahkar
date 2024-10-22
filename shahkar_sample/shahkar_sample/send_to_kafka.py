from kafka import KafkaProducer
import psycopg2
import json
from datetime import datetime
import time

def json_serial(obj):
    """Function to handle non-serializable types."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise


conn = psycopg2.connect(
    dbname="postgres", user="username", password="1234", host="postgres", port="5432"
)

producer = KafkaProducer(bootstrap_servers="kafka:9092")

coutn = 0
while True:
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM shahkar_user_apilog")
            rows = cur.fetchall()
            for row in rows:
                producer.send("api_log", json.dumps(row, default=json_serial).encode("utf-8"))
                coutn += 1
            print(f"{coutn} rows")
            producer.flush()
        time.sleep(60)
    except:
        conn.close()
        print("connection closed")

# from kafka import KafkaConsumer
# import json

# consumer = KafkaConsumer(
#     'api_log',
#     bootstrap_servers='kafka:9092',
#     auto_offset_reset='earliest',
#     enable_auto_commit=True,
#     group_id='my-group'
# )

# for message in consumer:
#     data = json.loads(message.value.decode('utf-8'))
#     print(data)  
