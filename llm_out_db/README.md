To run this database (in postgres container), run from this folder,
``` podman compose build```
```podman compose up ```

This runs table_setup.py (runs create table statements) and insert_llm_output_into_DB.py (actually sanitises, and inserts the data). Together, the scripts construct a POSTGRES database in the container, and inserts (corrected) information about Domestic Violence charities from our Ollama model (see llm folder).

Requires checked, "extracted_data.csv".
With data in format
  - url - 1 url per entry
  - charity_name - 1 name per entry
  - charity_numbers - {'england_wales': <number>, 'scotland': <number>, 'northern_ireland': <number>}
  - summary - single string
  - services - a JSON object containing 
      - description - single string
      - phone - either single number, or 'phone1, phone2, ...'
      - email - either single email, or 'email1, email2, ...'
      - locations - [location1, location2, ...]
  

  As well as corrected fields url_corrected, charity_numbers_corrected, summary_corrected, services_corrected and name_corrected (only used when corrections made).

  Uses Neomatim (https://nominatim.org/) via GeoPy (https://geopy.readthedocs.io/en/stable/) to find latitude/longitude coordimates of locations. 
  
