# This repo is to send emails for testing Emails and Email content only

## To execute, prepare virtual environment and install dependencies
    ```
    pip install virtualenv
    python -m venv env
    pip install -r requirements.txt
    ```

## Prepare `.env` file with following variables
    ```
    DATABASE_NAME =
    DATABASE_USERNAME =
    DATABASE_PASSWORD =
    DATABASE_HOSTNAME =
    AUTHENTICATION_BEARER =
    AUTHENTICATION_TOKEN = 
    ```

## To run send each email separately, execute the following command
    ```
    python -m main <test_case_1> <test_case_2>
    ```

## To send all emails at once, execute following command
    ```
    python -m main
    ```