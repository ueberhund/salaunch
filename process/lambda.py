
import sys
import logging
import boto3
import json
import os
import pymysql
from decimal import Decimal

def save_to_database(plate, toll, location):
    
    rds_host = os.environ['rds_host']
    rds_username = os.environ['rds_username']
    rds_password = os.environ['rds_password']
    rds_db_name = os.environ['db_name']

    item_count = 0
    conn = pymysql.connect(rds_host, user=rds_username, passwd=rds_password, db=rds_db_name, connect_timeout=5)
    with conn.cursor() as cur:
        cur.execute("""insert into transactions_toll (plaza, description, plate, toll) values( '%s', '%s', '%s', %d)""" % (location, 'INTRA AGENCY V-TOLL', plate, Decimal(toll)))
        conn.commit()
        cur.close()

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
    save_to_database(plate, toll, location)

if __name__ == '__main__':
    main()
