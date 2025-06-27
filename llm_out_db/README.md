To run this database (in postgres container), run from this folder,
``` podman compose build```
```podman compose up ```

This runs table_setup.py (runs create table statements) and insert_llm_output_into_DB.py (actually sanitises, and inserts the data). 

Also requires checked, "extracted_data.csv".
With data in format
  - url - 1 url per entry
  - charity_numbers - {'england_wales': <number>, 'scotland': <number>, 'northern_ireland': <number>}
  - summary - single string
  - phone - either single number, or 'phone1, phone2, ...'
  - email - either single email, or 'email1, email2, ...'
  - locations - [location1, location2, ...]
  - name - single string

  and as above for url_corrected, charity_numbers_corrected, summary_corrected, phone_corrected, email_corrected, locations_corrected and name_corrected is those fields are necessary (only used when corrections made).
  
