import psycopg2
import pandas as pd
import phonenumbers
import ast

from llm_setup import get_db_logger, connect, accessors
FILE = "extracted_data.csv"

def standardise_phone_number(x):
   try:
      return phonenumbers.format_number(phonenumbers.parse(str(x), "GB"), phonenumbers.PhoneNumberFormat.E164)
   except:
      return "nan"
   
def merge(file: str):
    df = pd.read_csv(file, usecols=["url", "charity_numbers", "summary", "charity_name", "services", "charity_numbers_corrected","summary_corrected","services_corrected", "charity_name_corrected", "url_corrected"] )
    df["url_corrected"] = df["url_corrected"].fillna(df["url"])
    df["charity_numbers_corrected"] = df["charity_numbers_corrected"].fillna(df["charity_numbers"])
    df["summary_corrected"] = df["summary_corrected"].fillna(df["summary"])
    df["services_corrected"] = df["services_corrected"].fillna(df["services"])
    df["charity_name_corrected"] = df["charity_name_corrected"].fillna(df["charity_name"])
    df = df[["charity_numbers_corrected","summary_corrected","services_corrected", "charity_name_corrected", "url_corrected"]]

    return df

if __name__ == "__main__":
    LOGGER = get_db_logger()
    conn = connect.connect()
  
    # need to clean up csv file - have to merge corrected with original, so all values are correct. corrected columns only contain corrections where necessary
    """df = pd.read_csv("extracted_data.csv", usecols=["url", "charity_numbers", "summary", "phone", "email", "locations", "name", "url_corrected","charity_numbers_corrected","summary_corrected","phone_corrected","email_corrected","locations_corrected","name_corrected"] )
    df["url_corrected"] = df["url_corrected"].fillna(df["url"])
    df["charity_numbers_corrected"] = df["charity_numbers_corrected"].fillna(df["charity_numbers"])
    df["summary_corrected"] = df["summary_corrected"].fillna(df["summary"])
    df["phone_corrected"] = df["phone_corrected"].fillna(df["phone"])
    df["email_corrected"] = df["email_corrected"].fillna(df["email"])
    df["locations_corrected"] = df["locations_corrected"].fillna(df["locations"])
    df["name_corrected"] = df["name_corrected"].fillna(df["name"])

   #standardise telephone using https://pypi.org/project/phonenumbers/
    df["phone_corrected"] = df["phone_corrected"].map(lambda x: standardise_phone_number(x) )
   
    df = df[["url_corrected","charity_numbers_corrected","summary_corrected","phone_corrected","email_corrected","locations_corrected","name_corrected"]]
   """
    df = merge(FILE)
    all_locs = []
    service = 1
    for row in df.itertuples():
      try:
         with conn:
            accessors.insert_charity(conn, str(row.url_corrected).strip(), str(row.charity_name_corrected).strip(), str(row.summary_corrected).strip())
            charity_nums = ast.literal_eval(row.charity_numbers_corrected)

      
         for c in charity_nums:
            if charity_nums[c] is not None and charity_nums[c] != "":
               try:
                  with conn:
                     accessors.insert_charity_number(conn, row.url_corrected, charity_nums[c], c)
               except Exception as e:
                  print(f"Error: {e}")

            """phones = str(row.phone_corrected).split(",")
            for p in phones:
               if p != "nan":
                  accessors.insert_phone_num(conn, str(row.url_corrected).strip(), str(p).strip())
         
            emails = str(row.email_corrected).split(",")
            for e in emails:
               if e != "nan":
                  accessors.insert_email(conn, str(row.url_corrected).strip(), str(e).strip())
            
            locations = ast.literal_eval(row.locations_corrected)
            for l in locations:
               if l not in all_locs:
                  all_locs.append(l)
                  accessors.insert_location(conn, len(all_locs) - 1,  str(l).strip())

               accessors.insert_charity_location(conn, str(row.url_corrected).strip(), all_locs.index(l))
            """
      except Exception as e:
         print(f"Error: {e}")

      

    conn.close()