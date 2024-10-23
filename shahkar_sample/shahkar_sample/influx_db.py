from influxdb import InfluxDBClient
import json
from read_from_kafka import api_log_df
client = InfluxDBClient(host='influxdb', port=8086, username='root', password='12345678', database='mydb')

def write_to_influxdb(batch_df, batch_id):
    records = batch_df.collect()
    
    json_body = []
    for row in records:
        json_body.append({
            "measurement": "api_requests",
            "tags": {
                "analyzer_id": row.analyzer_id,
            },
            "fields": {
                "total_requests": row.total_requests,
                "response_time": row.response_time,
            },
            "time": row.timestamp
        })
    
    if json_body:
        client.write_points(json_body)

query = api_log_df.writeStream \
    .foreachBatch(write_to_influxdb) \
    .start()

query.awaitTermination()
