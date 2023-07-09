import pyodbc
import time
from decouple import config
import traceback
from utils import logger

class DatabaseConnection:
    def __init__(self, max_retries=3, retry_delay=1):
        self.server = config('DATABASE_HOSTNAME')
        self.database = config('DATABASE_NAME', '')
        self.username = config('DATABASE_USERNAME')
        self.password = config('DATABASE_PASSWORD')
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            conn_str = f"DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
            self.connection = pyodbc.connect(conn_str)
            logger.info("Connected to the database successfully!")
        except pyodbc.Error as e:
            logger.error("Error connecting to the database:", e)

    def execute_query(self, query):
        self.connect()
        # Open the cursor, for every query we have to open and close
        self.cursor = self.connection.cursor()
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                self.cursor.execute(query)
                #commit the transaction
                self.cursor.commit()
                break
            except pyodbc.Error as e:
                logger.info(traceback.print_exc())
                self = DatabaseConnection()
                self.connect()
                logger.error("Error executing the query:", e)
                logger.error(f"Retrying in {self.retry_delay} seconds...")
                # time.sleep(self.retry_delay)
                retry_count += 1
        else:
            logger.error("Max retries exceeded. Failed to execute the query.")
        # Close the cursor when execution is done
        self.cursor = self.disconnect()
        return None

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("Disconnected from the database.")


# Initiate Database connection
# db = DatabaseConnection()
# db.connect()
# result = db.execute_query("SELECT * FROM mytable")
# print(result)
# db.disconnect()

# # Establish the connection
# conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

# # Create a cursor object
# cursor = conn.cursor()

# # Execute a query
# cursor.execute('SELECT * FROM [CTP_Royce2].[dbo].[status]')

# # Fetch and print the results
# for row in cursor.fetchall():
#     print(row)

# # Close the cursor and the connection
# cursor.close()
# conn.close()
# python -m main srf
