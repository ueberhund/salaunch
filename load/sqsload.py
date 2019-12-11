#Generates load to a SQS queue
#
#run as follows:
#locust -f sqsload.py --no-web -c 1000 -r 100
#where -c is # of users to spawn; -r is the hatch rate (users to spawn/second)

from locust import HttpLocust, TaskSet, task, between

class UserBehavior(TaskSet):

    @task
    def load_page(self):
        self.client.post("/ezpass", {"Action":"SendMessage",
            "MessageBody":"{'Plate':'D215J','Toll':'1.20','Location':'120th South'}",
            "Expires":"2020-10-15T12%3A00%3A00Z",
            "Version":"2012-11-05"})
        
class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    host = "https://sqs.us-east-1.amazonaws.com/122554519915"
    wait_time = between(20, 600)
