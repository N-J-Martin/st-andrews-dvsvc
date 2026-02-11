import pandas as pd
import ast
import phonenumbers
import argparse

EXPECTED_FILE = "../resource/expected_output.csv"
IN_FILE = "extracted_data.csv"

# reformats phone numbers into standard E164 format
def standardise_phone_number(x):
   try:
      return phonenumbers.format_number(phonenumbers.parse(str(x), "GB"), phonenumbers.PhoneNumberFormat.E164)
   except:
      return None

# Creates dictionaries linking charity urls to expected phone numbers, emails and charity numbers
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

# formats llm responses into dictionaries for phone numbers, emails and charity numbers, with the urls as keys
# essentially the same as get_expected_results
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
                        phones.add(p)

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




# compares of phone numbers, email addresses and charity numbers of the llm responses with their expected values.
def count_correct_responses(exp_phone_dict: dict, exp_email_dict: dict, exp_charity_dict: dict, new_phone_dict: dict, new_email_dict: dict, new_charity_dict: dict,  interactive: bool, log: bool ) -> float:
    correct = 0
    counted = 0
    LOGS = ""
    # new_phone_dict, new_email_dict and new_charity_dict should contain the same keys.
    for k in new_phone_dict.keys():
        # check key also in expected file before comparing
        if k in exp_phone_dict and k in exp_email_dict and k in exp_charity_dict and k in new_email_dict and k in new_charity_dict:
            counted += 1    
            passed = False
            new_phone_dict[k] = set(map(lambda x: standardise_phone_number(x), new_phone_dict[k]))
            if exp_phone_dict[k] != new_phone_dict[k]:
                LOGS = LOGS + f"Expected: {exp_phone_dict[k]}\n"
                LOGS = LOGS + f"Actual: {new_phone_dict[k]}\n\n"
            elif exp_email_dict[k] != new_email_dict[k]:
                LOGS = LOGS + f"Expected: {exp_email_dict[k]}\n"
                LOGS = LOGS + f"Actual: {new_email_dict[k]}\n\n"
            elif exp_charity_dict[k] != new_charity_dict[k]:
                LOGS = LOGS + f"Expected: {exp_charity_dict[k]}\n"
                LOGS = LOGS + f"Actual: {new_charity_dict[k]}\n\n"

            else:
                correct += 1
                passed = True

            # interactive provides option to manually mark responses as correct
            if not passed and interactive:
                print(LOGS)
                LOGS = ""
                override = input(f"Override {k}? (Y/N)")
                if override.upper()[0] == 'Y':
                    correct+=1
                print("============")

    if log:
        print(LOGS)
    # return percentage of correct responses at the end
    return (correct / counted)*100

# extracts the text used in the llm prompts, relate back to ur
def get_paragraph_text(file: str) -> dict:
    para_dict = {}
    response = pd.read_csv(file, usecols=["url", "paragraph_text"])
    for i, d in response.iterrows():
        para_dict[d["url"]] = d["paragraph_text"]
    return para_dict

# identifies whether all values in a list are featured in the paragraph text
def check_value_on_page(url:str, targets: list, paragraphs: str,interactive: bool,  log: bool) -> bool:
    for value in targets:
        if value is not None and value not in paragraphs:
            if log or interactive:
                print(f"Could not find '{value}' in {url}.\n")
                # interactive allows overriding of false negatives
                if interactive:
                    override = input(f"Override {url}? (Y/N)")
                    print("============")
                    if override.upper()[0] != 'Y':
                        return False
                   
            else:
                return False
    return True
    
# computes percentage of llm responses held values found in the text given in the prompt
def check_details_on_page(phone_dict: dict, email_dict: dict, charity_dict: dict, page_dict: dict, interactive: bool, log:bool) -> float:
    correct = 0
    count = 0 # 1 nan page
    for url, page in page_dict.items():
        if not pd.isnull(page):
            count += 1
            if check_value_on_page(url, phone_dict[url], page, interactive, log) and check_value_on_page(url, email_dict[url], page, interactive,  log) and check_value_on_page(url, charity_dict[url], page, interactive, log):
                correct += 1
    print(correct)
    return (correct/count)*100



def main():
    # flags for interactive (manually correct false negatives), the mode - comparing against expected, or comparing against page text, produce logs of mismatches 
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interactive", action='store_true', help="manually correct false negatives")
    parser.add_argument("-m", "--mode", required=True, choices=["expected", "inplace"], help="comparing against expected (expected), or comparing against page text (inplace)")
    parser.add_argument("-l", "--logs", action='store_true', help="outputs any mismatches")
    args = parser.parse_args()
    
    new_phone_dict, new_email_dict, new_charity_dict = get_response_details(IN_FILE)
    if args.mode == "expected":
        phone_dict, email_dict, charity_dict = get_expected_results(EXPECTED_FILE)
        result = count_correct_responses(phone_dict, email_dict, charity_dict, new_phone_dict, new_email_dict, new_charity_dict, args.interactive, args.logs)
        print(f"Percentage of responses correct (3 S.F): {result:.3}")

    else:
        result = check_details_on_page(new_phone_dict, new_email_dict, new_charity_dict, get_paragraph_text(IN_FILE), args.interactive, args.logs)
        print(result)
        print(f"Percentage of responses whose values can be found in input (3 S.F): {result:.3}")

if __name__ == "__main__":
    main()

