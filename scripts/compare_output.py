import pandas as pd
import ast

EXPECTED_FILE = "../resource/expected_output.csv"
IN_FILE = "../resource/extracted_data_service_context(in).csv"

correct = 0
# based on url - as none were corrected
phone_dict = {}
email_dict = {}
charity_dict = {}

# reads file of expected output.and sets up dictionaries linking url to emails, phone numbers and charity numbers
expected = pd.read_csv(EXPECTED_FILE, usecols=["url_corrected", "charity_numbers_corrected","summary_corrected","services_corrected", "charity_name_corrected"] )

for i, d in expected.iterrows():
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

    phone_dict[d["url_corrected"]] = phones.copy()
    email_dict[d["url_corrected"]] = emails.copy()

    
    expected_charity_nums = ast.literal_eval(d["charity_numbers_corrected"])
    expected_charity_nums = list(expected_charity_nums.values())
    charity_dict[d["url_corrected"]] = expected_charity_nums


# reads response file, collects et of phone numbers, email addresses and charity numbers to compare with expected.

response = pd.read_csv(IN_FILE, usecols=["url", "charity_numbers","summary","services", "charity_name"] )

for i, d in response.iterrows():
    service_list = ast.literal_eval(d["services"])
    phones = set()
    emails = set()

    for s in service_list:
        if 'phone' in s and s['phone']:
            phone = s['phone'].split(",")
            phones.update(phone)

        if 'email' in s and s['email']:
            email = s['email'].split(",")
            emails.update(email)

    charity_nums = ast.literal_eval(d["charity_numbers"])
    charity_nums = list(charity_nums.values())

    if phone_dict[d["url"]] == phones and email_dict[d["url"]] == emails and charity_dict[d["url"]] == charity_nums:
        correct += 1

# outputs percentage of correct responses (all of phones numbers, emails, and charity numbers match), to 3 significant figures
print(f"Percentage of responses correct (3 S.F): {(correct / len(phone_dict))*100:.3}")
