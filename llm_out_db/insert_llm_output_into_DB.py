import psycopg2
import pandas as pd
import phonenumbers
import ast
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from llm_setup import get_db_logger, connect, accessors
FILE = "extracted_data.csv"
USER_AGENT = "DASAD/0.1"
DELAY = 1

# returns phone number in standardised E164 format
def standardise_phone_number(x):
   try:
      return phonenumbers.format_number(phonenumbers.parse(str(x), "GB"), phonenumbers.PhoneNumberFormat.E164)
   except:
      return "nan"

# merges corrections to replace incorrect llm values
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
    geolocator = Nominatim(user_agent=USER_AGENT)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=DELAY)
  
    # need to clean up csv file - have to merge corrected with original, so all values are correct. corrected columns only contain corrections where necessary
    df = merge(FILE)
    all_locs = []
   
    for row in df.itertuples():
      service_count = 0
      try:
         # insert charity
         with conn:
            accessors.insert_charity(conn, str(row.url_corrected).strip(), str(row.charity_name_corrected).strip(), str(row.summary_corrected).strip())
            
         
         # insert charity nums
         charity_nums = ast.literal_eval(row.charity_numbers_corrected)
         for c in charity_nums:
            if charity_nums[c] is not None and charity_nums[c] != "":
               try:
                  with conn:
                     accessors.insert_charity_number(conn, row.url_corrected.strip(), charity_nums[c].strip(), c.strip())
               except Exception as e:
                  print(f"Error: {e}")

         # insert service
         services = ast.literal_eval(row.services_corrected)
         for s in services:
            service_count += 1
            try:
               with conn:
                  accessors.insert_service(conn, row.url_corrected.strip(), service_count, s["description"])
               # insert phone numbers for service
               if 'phone' in s and s['phone']:
                  phone = s['phone'].split(",")
                  for p in phone:
                     try: 
                        with conn:
                           accessors.insert_phone_num(conn, row.url_corrected.strip(), service_count, standardise_phone_number(p))
                     except Exception as e:
                        print(f"Error: {e}")

               # insert emails for service
               if 'email' in s and s['email']:
                  email = s['email'].split(",")
                  for e in email:
                     try: 
                        with conn:
                           accessors.insert_email(conn, row.url_corrected.strip(), service_count, e.strip())
                     except Exception as e:
                        print(f"Error: {e}")

               # add locations of service, add to location table if not seen already
               if 'locations' in s and s['locations']:
                  try:
                     for l in s['locations']:
                        if l not in all_locs:
                           all_locs.append(l)
                           #converts string to latitude/longitude coordinations, with rate limiting
                           location = geocode(l)
                           print(location.latitude)
                           with conn:
                              accessors.insert_location(conn, len(all_locs) - 1,  str(l).strip(), location.latitude, location.longitude)

                        with conn:
                           accessors.insert_service_location(conn, str(row.url_corrected).strip(), service_count, all_locs.index(l))

                  except Exception as e:
                     print(f"Error: {e}")

            except Exception as e:
                  print(f"Error: {e}")

      except Exception as e:
         print(f"Error: {e}")

      

    conn.close()