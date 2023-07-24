from .data_queries import SAVE_DATA_DAILY_STATUS_REPORT_SAVE, SAVE_DATA_INTO_SRF, DELETE_ALL_RECORDS
import requests
from decouple import config
from utils import logger
from datetime import date

'''
Steps for testing Daily SRT, 
'''

TEST = 'DSRT'
URL = '/statusreport'
BODY = {}
SUCCESS_RESPONSE = {"success": "Mail is sent successfully"}
current_date = str(date.today().strftime("%m/%d/%Y"))

def send_dsrt_email(url, headers, db):
    recreate_required_data(db)
    response = call_django_api(url, headers)
    if response.status_code == 200:
        # logger.info(f"{TEST} Email sent successfully, {response.json()}")
        return True
    logger.info(f"{TEST} Email not sent, tried to delete and save data { response.json()} ")
    return False

def recreate_required_data(db):
    # Delete all records for "eapple" and create them again
    db.execute_query(DELETE_ALL_RECORDS)
    logger.info(f"Deleted all records for {TEST}")
    # Create the records for ROA
    db.execute_query(SAVE_DATA_DAILY_STATUS_REPORT_SAVE.format(current_date, current_date, current_date, current_date, current_date))
    logger.info(f"Created all records for {TEST}")
    # Update the records for ROA

def call_django_api(url, headers):
    # API call for django -> Daily Status Report
    return requests.get(url + URL, headers=headers, data=BODY)
