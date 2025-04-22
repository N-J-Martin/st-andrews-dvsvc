#import psycopg2
import pandas as pd
#from llm_setup import get_db_logger, connect, accessors

if __name__ == "__main__":
   # LOGGER = get_db_logger()
   # conn = connect.connect()
  
    #accessors.insert_charity(conn,  "www.test.com", "test", "test" )
    # need to clean up csv file - have to merge corrected with original, so all values are correct. corrected columns only contain corrections where necessary
    #df = pd.read_csv("extracted_data.csv", usecols=["url_corrected","charity_numbers_corrected","summary_corrected","phone_corrected","email_corrected","locations_corrected","name_corrected"])
    df = pd.read_csv("extracted_data.csv", usecols=["url", "charity_numbers", "summary", "phone", "email", "locations", "name", "url_corrected","charity_numbers_corrected","summary_corrected","phone_corrected","email_corrected","locations_corrected","name_corrected"] )
    df["url_corrected"].fillna(df["url"], inplace = True)
    df["charity_numbers_corrected"].fillna(df["charity_numbers"], inplace = True)
    df["summary_corrected"].fillna(df["summary"], inplace = True)
    df["phone_corrected"].fillna(df["phone"], inplace = True)
    df["email_corrected"].fillna(df["email"], inplace = True)
    df["locations_corrected"].fillna(df["locations"], inplace = True)
    df["name_corrected"].fillna(df["name"], inplace = True)
    
    df = df[["url_corrected","charity_numbers_corrected","summary_corrected","phone_corrected","email_corrected","locations_corrected","name_corrected"]]
    print(df)
    #conn.close()