from .data_queries import DELETE_ALL_TABLE_RECORDS
import requests
from decouple import config
from utils import logger
from datetime import date
'''
Steps for testing ROA, 
'''

TEST = 'LPIE'
URL = '/style'
BODY = {}
current_date = str(date.today().strftime("%m/%d/%Y"))

def send_lpie_email(url, headers, db):
    recreate_required_data(db)
    response = call_django_api(url, headers)
    if response.status_code == 200:
        logger.info(f"{TEST} Email sent successfully, {response.json()}")
        return True
    logger.info(f"{TEST} Email not sent, tried to delete and save data { response.json()} ")
    return False

def recreate_required_data(db):
    # Delete all records for all tables to run style code
    db.execute_query(DELETE_ALL_TABLE_RECORDS)
    logger.info(f"Deleted all records for {TEST}")


def call_django_api(url, headers):
    # API call for django -> MultiSampleRequest
    return requests.get(url + URL, headers=headers, data=BODY)
