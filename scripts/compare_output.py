import pandas as pd
import ast
import re
import phonenumbers
import getopt, sys

EXPECTED_FILE = "../resource/expected_output.csv"
IN_FILE = "extracted_data.csv"

def standardise_phone_number(x):
   try:
      return phonenumbers.format_number(phonenumbers.parse(str(x), "GB"), phonenumbers.PhoneNumberFormat.E164)
   except:
      return None


def get_expected_results(file: str) -> tuple[dict, dict, dict]:
    # based on url - as none were corrected
    phone_dict = {}
    email_dict = {}
    charity_dict = {}

    # reads file of expected output.and sets up dictionaries linking url to emails, phone numbers and charity numbers
    expected = pd.read_csv(file, usecols=["url_corrected", "charity_numbers_corrected","summary_corrected","services_corrected", "charity_name_corrected"] )

    for i, d in expected.iterrows():
        service_list = ast.literal_eval(d["services_corrected"])
        phones = set()
        emails = set()
        for s in service_list:
            if 'phone' in s and s['phone']:
                phone = s['phone'].split(",")
                for p in phone:
                    phones.add(standardise_phone_number(p))
            
            if 'email' in s and s['email']:
                email = s['email'].split(",")
                for e in email:
                    emails.add(e.strip())

        phone_dict[d["url_corrected"]] = phones.copy()
        email_dict[d["url_corrected"]] = emails.copy()

        
        expected_charity_nums = ast.literal_eval(d["charity_numbers_corrected"])
        expected_charity_nums = list(expected_charity_nums.values())
        # remove None and "" values from list
        expected_charity_nums = list(filter(lambda x: x != None and x != "", expected_charity_nums))
        charity_dict[d["url_corrected"]] = expected_charity_nums

    return phone_dict, email_dict, charity_dict

def get_response_details(file: str) -> tuple[dict, dict, dict]:
    phone_dict = {}
    email_dict = {}
    charity_dict = {}
    response = pd.read_csv(file, usecols=["url", "charity_numbers","summary","services", "charity_name"] )

    for i, d in response.iterrows():
        
        
        phones = set()
        emails = set()
        charity_nums = []

    
        if not pd.isnull(d["services"]): 
            service_list = ast.literal_eval(d["services"])
            for s in service_list:
                if 'phone' in s and s['phone']:
                    if type(s['phone']) == list :
                        phone = s['phone']
                    else:
                        phone = s['phone'].split(",")
                    for p in phone:
                        phones.add(standardise_phone_number(p))

                if 'email' in s and s['email']:
                    if type(s['email']) == list :
                        email = s['email']
                    else:
                        email = s['email'].split(",")
                    for e in email:
                        if e:
                            emails.add(e.strip())

        if not pd.isnull(d["charity_numbers"]):
            charity_nums = ast.literal_eval(d["charity_numbers"])
            charity_nums = list(charity_nums.values())
            charity_nums = list(filter(lambda x: x != None and x != "", charity_nums))

        phone_dict[d["url"]] = phones.copy()
        email_dict[d["url"]] = emails.copy()
        charity_dict[d["url"]] = charity_nums.copy()

    return phone_dict, email_dict, charity_dict




# reads response file, collects et of phone numbers, email addresses and charity numbers to compare with expected.
def count_correct_responses(exp_phone_dict: dict, exp_email_dict: dict, exp_charity_dict: dict, new_phone_dict: dict, new_email_dict: dict, new_charity_dict: dict,  interactive: bool ) -> float:
    correct = 0
    counted = 0
    
    # new_phone_dict, new_email_dict and new_charity_dict should contain the same keys.
    for k in new_phone_dict.keys():
        # check key also in expected file before comparing
        if k in exp_phone_dict and k in exp_email_dict and k in exp_charity_dict and k in new_email_dict and k in new_charity_dict:
            counted += 1    
            passed = False
            if exp_phone_dict[k] != new_phone_dict[k]:
                print(f"Expected: {exp_phone_dict[k]}")
                print(f"Actual: {new_phone_dict[k]}")
                print()
            elif exp_email_dict[k] != new_email_dict[k]:
                print(f"Expected: {exp_email_dict[k]}")
                print(f"Actual: {new_email_dict[k]}")
                print()
            elif exp_charity_dict[k] != new_charity_dict[k]:
                print(f"Expected: {exp_charity_dict[k]}")
                print(f"Actual: {new_charity_dict[k]}")
                print()
            else:
                correct += 1
                passed = True

            # interactive provides option to manually mark responses as correct
            if not passed and interactive:
                override = input(f"Override {d["url"]}? (Y/N)")
                if override.upper()[0] == 'Y':
                    correct+=1
                print("============")

    # return percentage of correct responses at the end
    print(counted)
    return (correct / counted)*100

def get_paragraph_text(file: str) -> dict:
    para_dict = {}
    response = pd.read_csv(file, usecols=["url", "paragraph_text"])
    for i, d in response.iterrows():
        para_dict[d["url"]] = d["paragraph_text"]
    return para_dict

def check_value_on_page(url:str, targets: list, paragraphs: dict) -> bool:
    if url in paragraphs:
        page = paragraphs[url]
        for value in targets:
            if value in page:
                return False

        return True
    else:
        raise ValueError("No page provided")

def main():
    interactive = False
    argList  = sys.argv[1:]
    options = "i"
    long_options = "interactive"
    # use -i or --interactive as command line argument to use itneractive mode to manually correct responses that don't match.    
    try:
        args, vals = getopt.getopt(argList, options, long_options)
        for a, v in args:
            if a in ("-i", "--interactive"):
                interactive = True

    except getopt.error as err:
        print (str(err))
    
    phone_dict, email_dict, charity_dict = get_expected_results(EXPECTED_FILE)
    new_phone_dict, new_email_dict, new_charity_dict = get_response_details(IN_FILE)
    # outputs percentage of correct responses (all of phones numbers, emails, and charity numbers match), to 3 significant figures
    print(f"Percentage of responses correct (3 S.F): {count_correct_responses(phone_dict, email_dict, charity_dict, new_phone_dict, new_email_dict, new_charity_dict, interactive):.3}")

if __name__ == "__main__":
    """para = get_paragraph_text(IN_FILE)
    phone_dict, email_dict, charity_dict = get_expected_results(EXPECTED_FILE)
    for u, p in phone_dict.items():
        try:
            print(check_value_on_page(u, p, para))
        except:
            print("No page stored")

    """

    main()

