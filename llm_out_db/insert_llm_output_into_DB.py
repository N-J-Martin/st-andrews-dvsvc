import psycopg2
import pandas as pd
from llm_setup import get_db_logger, connect, accessors

if __name__ == "__main__":
    LOGGER = get_db_logger()
    conn = connect.connect()
  
    #accessors.insert_charity(conn,  "www.test.com", "test", "test" )
    df = pd.read_csv("extracted_data.csv", usecols=["url_corrected","charity_numbers_corrected","summary_corrected","phone_corrected","email_corrected","locations_corrected","name_corrected"])
    print(df)
    conn.close()