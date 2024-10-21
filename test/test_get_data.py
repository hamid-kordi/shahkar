from locust import HttpUser, TaskSet, task, between
import json
import random
import pandas as pd

HOST = "127.0.0.1:8000"
with open(file="files/analyzer_data.json", mode="r") as analyzer:
    analyzer_data = json.load(analyzer)


def get_analyzer_random():
    """
    get random analyzer id and name , read csv for request to API
    """

    index = random.randint(0, 1900)
    analyzer_id = analyzer_data[index]["analyzer_id"]
    analyzer_name = analyzer_data[index]["name"]
    return analyzer_id, analyzer_name


chunksize = 1000
sample_size = 200000
total_records = 1000000


def select_random_phone_number():
    """
    get random phonenumber, read csv for request to API
    """
    # index = 10
    index = random.randint(0, 9)
    csv_file = f"files/output_{index}.csv"
    random_indices = sorted(random.sample(range(total_records), sample_size))
    phone_numbers = []
    for i, chunk in enumerate(pd.read_csv(csv_file, chunksize=chunksize)):
        if i in random_indices:
            phone_number = chunk["phonenumber"].values[0]
            phone_numbers.append(phone_number)
        if len(phone_numbers) == sample_size:
            break
    return phone_numbers


def random_user_agent():
    """
    select random user agent
    """

    agent = ["Desktop", "Mobile"]
    return agent[random.randint(0, 1)]


class UserBehavior(TaskSet):
    """
    define user behavior for the test
    """

    phones = select_random_phone_number()
    task_id = ["ba4220dd-1bf2-4b64-88f7-690928031069"]  # for sample and start test

    @task
    def get_user_data1(self):
        headers = {"Cache-Control": "no-cache", "Pragma": "no-cache", "Expires": "0"}
        random_index = random.randint(0, len(self.phones) - 1)
        params = {
            "phone_number": self.phones[random_index],
            "analyzer_id": get_analyzer_random()[0],
            "user_agent": random_user_agent(),
            "source_ip": "192.168.1.1",
        }

        response = self.client.get("/user/my_view/", params=params, headers=headers)

        if response.status_code == 202:
            result = response.json()
            self.task_id.append(result["task_id"])
            print(f"Task ID: {result['task_id']}")
        else:
            print(f"Error: {response.status_code}")

    # TODO:add paending
    @task
    def get_result_task(self):
        headers = {"Cache-Control": "no-cache", "Pragma": "no-cache", "Expires": "0"}
        index = random.randint(0, len(self.task_id) - 1)
        params = {"task_id": self.task_id[index]}
        response = self.client.get("/user/task_result/", params=params, headers=headers)
        while response.status_code != 200:
            response = self.client.get(
                "/user/task_result/", params=params, headers=headers
            )
        print(f"status code: {response.status_code} - {response.text}")

    # @task
    # def reset_stats(self):
    #     # Reset stats during the test
    #     self.environment.events.reset_stats.fire()


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
