from .data_queries import DELETE_ALL_TABLE_RECORDS, SAVE_DATA_FINAL_TP_VERIFIED
import requests
from decouple import config
from utils import logger
from datetime import date
'''
Steps for testing FTPVE, 
'''

TEST = 'FTPVE'
URL = 'srf/overallStatus'
BODY = {}
SUCCESS_RESPONSE = {"success": "Mail is sent successfully"}
current_date = str(date.today().strftime("%m/%d/%Y"))

def send_ftpve_email(url, headers, db):
    recreate_required_data(db)
    response = call_django_api(url, headers)
    if response.status_code == 200:
        logger.info(f"{TEST} Email sent successfully, {response.json()}")
        return True
    logger.info(f"{TEST} Email not sent:, { response.json()} ")
    return False

def recreate_required_data(db):
    # Delete all records for "eapple" and create them again
    db.execute_query(DELETE_ALL_TABLE_RECORDS)
    logger.info(f"Deleted all records for {TEST}")
    db.execute_query(SAVE_DATA_FINAL_TP_VERIFIED)


def call_django_api(url, headers):
    # API call for django -> MultiSampleRequest
    return requests.get(url + URL, headers=headers, data=BODY)
