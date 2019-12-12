
# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.


import logging
import boto3
import json
import os
from botocore.exceptions import ClientError


def main(event, context):
    """Exercise retrieve_sqs_messages()"""

    # Assign this value before running the program
    print(event)
    
    receiptHandle = event['Records'][0]['receiptHandle']
    print(receiptHandle)
    
    body = event['Records'][0]['body'].replace("\'", "\"")
    body = json.loads(body)
    
    plate = body['Plate']
    toll = body['Toll']
    location = body['Location']
    
    print("Plate: " + plate + "; toll: " + toll + "; location:" + location)
    #todo add to database
    
    #clear from the sqs queue
    queue_url = os.environ['queue_url']
    sqs_client = boto3.client('sqs')
    sqs_client.delete_message(QueueUrl=queue_url,
                              ReceiptHandle=receiptHandle)
    

if __name__ == '__main__':
    main()
