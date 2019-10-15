import json
import random

from locust import HttpLocust, TaskSet

def login(l):
    pass

def logout(l):
    pass

def index(l):
    '''用户信息'''
    userNumber = random.randint(300000, 500000)
    userAge = 18
    headers = {'charset': 'utf-8', 'content-type': 'application/json'}
    post_data = {'userNumber': userNumber, 'userAge': userAge}
    request_result = l.client.post("/app/api/api-demo", data= json.dumps(post_data), headers = headers)
    print(request_result.__dict__)

def profile(l):
    pass

class UserBehavior(TaskSet):
    threadnum = 10
    tasks = {index: threadnum}

    def on_start(self):
        pass

    def on_stop(self):
        pass

class WebsiteUser(HttpLocust):
    host = "https://api.domain.com"
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000