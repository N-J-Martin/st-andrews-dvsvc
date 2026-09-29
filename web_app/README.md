# DASHED Web App
This is the web front end for the automated domestic violence support database. 
It is built using Flask, and additionally uses Neomatim (https://nominatim.org/) via GeoPy (https://geopy.readthedocs.io/en/stable/), and the POSTGRESQL database managed by directory `llm_out_db`.

## Current Features
Enter postcode and a distance (between 0 and 1000km) to search for domestic violence support organisations that have a service within that area, ordered by distance of service. Organisations are repeated for each service. 

The search distance will expand until either a charity is found, or the distance exceeds 1000km.

If the location entered is not valid (geocoder does not return coordinates for the value), then all charities in the database are shown. This can also be accessed by /all/1.

Search results are paginated

Click on a service in the search results to navigate to a page about that organisation, displaying general information about the charity and a list of services they provide.

## Running Locally
This requires `llm_out_db_db_1` to be running. This can be set up as described in the README in `llm_out_db` directory. You can restart the podman/docker container with `podman/docker compose restart llm_out_db_db_1`.

Set up and activate a python virtual environment as described in the main README. Install the requirements for this directory, by navigating to this directory and running
`pip install -r requirements.txt`.

Then to host the web app locally, run `flask run`.
The site can be accessed at `localhost:5000`

## TODO
- Show both charities with location in search radius, and nationwide examples (e.g: location is UK, England, Scotland, Wales, None).
- Introduce a map to show locations
- Filter by keywords in descriptions, leading to adjusting database backend and queries to allow filtering by other user requirements (accsssibility, service type, who they support etc).
- Improve display of information


