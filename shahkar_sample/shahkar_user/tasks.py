from celery import shared_task
from .models import UserProfile, ApiLog
from pyspark.sql import SparkSession
from django.core.exceptions import ObjectDoesNotExist
import time

# @shared_task
# def find_user_by_phone_spark(phone_number):

#     spark = SparkSession.builder.appName("User Finder").getOrCreate()
#     jdbc_url = "jdbc:postgresql://shahkar_postgres:5432/shahkar"
#     properties = {"user": "username", "password": "1234"}
#     df = spark.read.jdbc(url=jdbc_url, table="user", properties=properties)
#     df = df.repartition(100)
#     df.cache()
#     user = df.filter(df.phonenumber == phone_number).collect()
#     if user:
#         user = user[0]
#         return {
#             "national_id": user.natoinal_id,
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "birth_date": user.birthday.strftime("%Y-%m-%d"),
#             "address": user.address,
#             "message": "Success",
#         }
#     else:
#         return {"message": "User not found"}

#     spark.stop()


@shared_task
def find_user_by_phone(phone_number):
    user = UserProfile.objects.filter(phonenumber=phone_number).first()
    if user:
        return {
            "national_id": user.natoinal_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "birth_date": user.birthday.strftime("%Y-%m-%d"),
            "address": user.address,
            "message": "Success",
        }
    else:
        return {"message": "User not found"}


@shared_task
def log_into_db(task_id, state, tm):
    api_log = ApiLog.objects.filter(task_id=task_id).first()
    if api_log:
        api_log.status = state
        api_log.result_time = tm
        api_log.save()
