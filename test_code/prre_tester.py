from .data_queries import DELETE_ALL_TABLE_RECORDS, SAVE_DATA_PRODUCT_READY, SAVE_DATA_PRODUCT_READY_2
import requests
from decouple import config
from utils import logger
from datetime import date
'''
Steps for testing ProductReady , TP-Update Email for PD , QA and Design, 
'''

TEST = 'PRRE'
URL = '/srf/overallStatus'
BODY = {}
current_date = str(date.today().strftime("%m/%d/%Y"))
SUCCESS_RESPONSE = {"status": "Documents Check Successful"}

def send_prre_email(url, headers, db):
    recreate_required_data(db)
    response = call_django_api(url, headers)
    if response.status_code == 200 and response.json() == SUCCESS_RESPONSE:
        logger.info(f"{TEST} Email1 sent successfully, {response.json()}")
    # save data for reminder email product ready
    recreate_required_data_2(db)
    response = call_django_api(url, headers)
    if response.status_code == 200 and response.json() == SUCCESS_RESPONSE:
        logger.info(f"{TEST} Email1 sent successfully, {response.json()}")
        return True
    logger.info(f"{TEST} Email not sent, tried to delete and save data { response.json()} ")
    return False

def recreate_required_data(db):
    # Delete all records for all tables to run style code
    db.execute_query(DELETE_ALL_TABLE_RECORDS)
    logger.info(f"Deleted all records for {TEST}")
    #Create Rows for sending TP-Verify Email for QA, PD and Design
    db.execute_query(SAVE_DATA_PRODUCT_READY)
    logger.info(f"Created records for {TEST}")

def recreate_required_data_2(db):
    # Delete all records for all tables to run style code
    db.execute_query(DELETE_ALL_TABLE_RECORDS)
    logger.info(f"Deleted all records for {TEST}")
    #Create Rows for sending TP-Verify Email for QA, PD and Design
    db.execute_query(SAVE_DATA_PRODUCT_READY_2)
    logger.info(f"Created records for {TEST}")
    return

def call_django_api(url, headers):
    # API call for django -> MultiSampleRequest
    return requests.get(url + URL, headers=headers, data=BODY)
