#Generates load to a SQS queue
#
#run as follows:
#locust -f sqsload.py --no-web -c 1000 -r 100
#where -c is # of users to spawn; -r is the hatch rate (users to spawn/second)

import random
import decimal
from locust import HttpLocust, TaskSet, task, between

def generate_licenseplate():
    return "D215J"
        
def generate_toll():
    return str(decimal.Decimal(random.randrange(100, 400))/100)
    

class UserBehavior(TaskSet):

    @task
    def load_page(self):
        plate = generate_licenseplate()
        toll = generate_toll()
        
        self.client.post("/ezpass", {"Action":"SendMessage",
            "MessageBody":"{'Plate':" + plate + ",'Toll':" + toll + ",'Location':'120th South'}",
            "Expires":"2020-10-15T12%3A00%3A00Z",
            "Version":"2012-11-05"})
    
class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    host = "queue url"
    wait_time = between(20, 600)
