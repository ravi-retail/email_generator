from .data_queries import SAVE_DATA_INTO_SRF, DELETE_ALL_RECORDS
import requests
from decouple import config 
from utils import logger
'''
Steps for testing Sample Request Form, 

'''
URL = '/style/factory/send_samples'
BODY = {
    'request_notes': 'Request is sent',
    'color_code': '100',
    'factory': 'dynamic',
    'season': 'S24',
    'request_no': '1',
    'size': 'L',
    'style': 'eapple',
    'brand': 'DICKI',
    'tpstatus': '0'
    }
ERROR_RESPONSE_001 = {"info":"Sample request not saved"}
SUCCESS_RESPONSE = {"info": "Sample request 1 sent for eapple - 100 ,L"}

def send_srf_email(url, headers, db):
    recreate_required_data(db)
    response = call_django_api(url, headers)
    if response.status_code == 200 and response.json() == SUCCESS_RESPONSE:
        logger.info("SRF Email sent successfully")
        return True
    logger.info(f"SRF Email not sent, tried to delete and save data { response.json()} ")
    return False

def recreate_required_data(db):
    # Delete all records for "eapple" and create them again
    logger.info("Deleted all records for SRF")
    db.execute_query(DELETE_ALL_RECORDS)
    # Create the records again
    logger.info("Created all records for SRF")
    db.execute_query(SAVE_DATA_INTO_SRF)
    # API call for django -> MultiSampleRequest

def call_django_api(url, headers):
    # API call for django -> MultiSampleRequest
    return  requests.post(url + URL,headers=headers, data=BODY)



    