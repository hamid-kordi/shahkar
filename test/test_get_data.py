from locust import HttpUser, TaskSet, task, between
import json
import random


with open(file="analyzer_id.json", mode="r") as analyzer:
    analyzer_data = json.load(analyzer)


def get_analyzer_random():
    analyzer_id = analyzer_data[random.randint(0, 2000)]["analyzer_id"]
    analyzer_name = analyzer_data[random.randint(0, 2000)]["name"]
    return analyzer_id,analyzer_name

def get_random_phone_number():
    pass


class UserBehavior(TaskSet):
    @task
    def get_user_data(self):
        params = {
            "phone_number": "09123456789",
            "analyzer_id": "1234",
            "user_agent": "Mobile",
            "source_ip": "192.168.1.1",
            "request_id": "abcd-1234",
        }

        response = self.client.get("/user-data/", params=params)

        if response.status_code == 202:
            result = response.json()
            print(f"Task ID: {result['task_id']}")
        else:
            print(f"Error: {response.status_code}")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
