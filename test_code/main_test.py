import sys
from pathlib import Path
sys.path.append(str(Path(sys.argv[0]).absolute().parent.parent))

from .db_helper import DatabaseConnection
from decouple import config
from .data_queries import DELETE_ALL_RECORDS
from .srf_tester import send_srf_email
from .roa_tester import send_roa_email
from .droa_tester import send_droa_email
from .dsrt_tester import send_dsrt_email
from .dsre_tester import send_dsre_email
from .lpee_tester import send_lpee_email
from .lpie_tester import send_lpie_email
from .prre_tester import send_prre_email
from .ftpve_tester import send_ftpve_email

import traceback
from utils import logger
# from roa_tester import 


ROA = 'roa'
DROA = 'droa'
DSRE = 'dsre'
DSRT = 'dsrt'
SRF = 'srf'
LPIE = 'lpie'
LPEE = 'lpee'
PRRE = 'prre'
FTPVE = 'ftpve'


URL = 'http://localhost:8000/api/v1'
HEADERS = {
    "Authorization": config('AUTHENTICATION_BEARER') + ' ' + config('AUTHENTICATION_TOKEN'),
    "Content_Type":"application/json",
    "Accept": "application/json",
    }

# All the test cases to execute
test_cases = [
    ROA,  # ROA Email
    DROA, # DROA Email
    DSRE, # DSRE Daily Status Report Email
    DSRT, # Daily SRT Report Email
    SRF,  # Sample Request Form
    LPIE, # Line Plan Initiation Email
    LPEE,  # Line Plan Execution Error Email
    PRRE,
    FTPVE 
    ]

# Read parameters to test based on user commands, else test all
test_cases = [test_case.lower() for test_case in sys.argv[1:]] if len(sys.argv) > 1 else test_cases 
logger.info(f"Testing following emails {test_cases} ")

def main():
    # Initiate Database connection
    db = DatabaseConnection()
    db.connect()

    for test_case in test_cases:
        try:
            test_func = empty_function
            if test_case == SRF:
                test_func = send_srf_email
            elif test_case == ROA:
                test_func = send_roa_email
            elif test_case == DROA:
                test_func = send_droa_email
            elif test_case == DSRT:
                test_func = send_dsrt_email
            elif test_case == DSRE:
                test_func = send_dsre_email
            elif test_case == LPIE:
                test_func = send_lpie_email
            elif test_case == PRRE:
                test_func = send_prre_email
            elif not (LPIE in test_cases) and LPEE == test_case:
                test_func = send_lpee_email
            elif test_case == FTPVE:
                test_func = send_ftpve_email
            else:
                logger.info("Test Function name not defined")
            try:
                logger.info(f"Testing: {test_case}")
                print(f"Testing: {test_case}")
                test_status = test_func(URL, HEADERS, db)
                print(f'Test Success :{test_case}' if test_status else f'Test Failed: {test_case}' )
                if test_case == LPIE:
                    print(f'Test Success :{LPEE}' if test_status else f'Test Failed: {LPEE}')
            except BaseException as e:
                logger.error(f"Error While testing : {traceback.format_exc()}")
        finally:
            # Delete all records for "eapple" and create them again
            db.execute_query(DELETE_ALL_RECORDS)
            logger.info("Deleted all records for style='eapple'")

def empty_function(**kwargs):
    return

if __name__ == '__main__':
    main()