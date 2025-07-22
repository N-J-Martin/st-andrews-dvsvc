import pandas as pd
import json
import ast

EXPECTED_FILE = "../resource/expected_output.csv"
IN_FILE = ""

correct = 0
# based on url - as none were corrected
phoneDict = {}
emailDict ={}


df = pd.read_csv(EXPECTED_FILE, usecols=["url_corrected", "charity_numbers_corrected","summary_corrected","services_corrected", "charity_name_corrected"] )

for i, d in df.iterrows():
    service_list = ast.literal_eval(d["services_corrected"])
    phones = set()
    emails = set()
    for s in service_list:
        if 'phone' in s and s['phone']:
            phone = s['phone'].split(",")
            phones.update(phone)
        
        if 'email' in s and s['email']:
            email = s['email'].split(",")
            emails.update(email)

    phoneDict[d["url_corrected"]] = phones.copy()
    emailDict[d["url_corrected"]] = emails.copy()

print(phoneDict)
print(emailDict)