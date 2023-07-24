from .data_queries import SAVE_DATA_DROA_STATUS, SAVE_DATA_INTO_SRF, DELETE_ALL_RECORDS
import requests
from decouple import config
from utils import logger
from datetime import date

'''
Steps for testing ROA, 
'''

TEST = 'DROA'
URL = '/droamail'
BODY = {}
SUCCESS_RESPONSE = {"success":"Droa Mail sent successfully"}
current_date = str(date.today().strftime("%m/%d/%Y"))

def send_droa_email(url, headers, db):
    recreate_required_data(db)
    response = call_django_api(url, headers)
    if response.status_code == 200 and response.json() == SUCCESS_RESPONSE:
        logger.info(f"{TEST} Email sent successfully, {response.json()}")
        return True
    logger.info(f"{TEST} Email not sent, tried to delete and save data { response.json()} ")
    return False

def recreate_required_data(db):
    # Delete all records for "eapple" and create them again
    db.execute_query(DELETE_ALL_RECORDS)
    logger.info(f"Deleted all records for {TEST}")
    # Create the records for DROA
    db.execute_query(SAVE_DATA_DROA_STATUS.format(current_date, current_date, current_date, current_date, current_date))
    logger.info(f"Created all records for {TEST}")
    # Update the records for DROA

def call_django_api(url, headers):
    # API call for django -> MultiSampleRequest
    for i in range(10):
        resp = requests.get(url + URL, headers=headers, data=BODY)
    return resp
