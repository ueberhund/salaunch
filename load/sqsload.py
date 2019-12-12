#Generates load to a SQS queue
#
#run as follows:
#locust -f sqsload.py --no-web -c 1000 -r 100
#where -c is # of users to spawn; -r is the hatch rate (users to spawn/second)
#
#master: locust -f sqsload.py --no-web --master --expect-slaves=4 -c 5000 -r 100 --run-time=60s
#slave: locust -f sqsload.py --no-web --slave --master-host=HOSTIP
#

import random
import decimal
from locust import HttpLocust, TaskSet, task, between

def generate_licenseplate():
    return character_range(3) + " " + number_range(3)
        
def generate_toll():
    return str(decimal.Decimal(random.randrange(100, 400))/100)
    
def character_range(num):
    platechars = ""
    for x in range(num):
        platechars += str(chr(random.randrange(97, 123)))
    
    return platechars.upper()
        
def number_range(num):
    nums = ""
    for x in range(num):
        nums += str(random.randrange(0,9))
        
    return nums
    
def generate_loc():
    val = random.randrange(0,9)
    return "EZPass Location " + str(val)
    

class UserBehavior(TaskSet):

    @task
    def load_page(self):
        plate = generate_licenseplate()
        toll = generate_toll()
        location = generate_loc()
        
        self.client.post("/ezpass", {"Action":"SendMessage",
            "MessageBody":"{'Plate':'" + plate + "','Toll':'" + toll + "','Location':'" + location + "'}",
            "Expires":"2020-10-15T12%3A00%3A00Z",
            "Version":"2012-11-05"})
    
class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    host = "sql url"
    wait_time = between(20, 600)
