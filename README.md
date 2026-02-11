# st-andrews-dvsvc

A web crawler to discover UK-based domestic violence support services.

## Requirements

 * Charity Register, stored in `resource` folder, with path updated in the `__SCOT_CHARITIES_PATH` variable in `heuristics/dvdvsc_scorers.py`. Retrieved from the [OSCR](https://www.oscr.org.uk/about-charities/search-the-register/download-the-scottish-charity-register/).  © Crown Copyright and database right [2025]. Contains information from the Scottish Charity Register supplied by the Office of the Scottish Charity Regulator and licensed under the Open Government Licence v.3.0. (http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)

 * Python 3.10 or later
 * Docker-compose or equivalent container is up-to-date and connected (if using) 

## Use with Docker
 Set `.env`  with environment variables as per `example.env`. Note, you do not need to use 'DB_HOST' for this section.
 
After building the image with 

`docker compose build`

To ensure use of `schema_dump.sql` to initialise database, need to remove `db_data` volume using 

`docker volume rm st-andrews-dvsvc_db_data`

Then run: 

`docker compose up`

 to start four containers:

* `app` (the crawler)
* `db` (the PostgreSQL database server)
* `pgadmin`
* `ollama` (requires nvidia GPU, but other containers should run even if this doesn't)


`docker compose run db pgadmin` 

will only spin up the database and pgAdmin containers.

Access pgAdmin from a browser at port 5051, as specified in `compose.yaml`. The hostname of the database will be the container ID of db container (found by `docker compose ps`).

## Run just the crawler (without Docker)
First, create a virtual environment.

`python3.10 -m venv venv`

Then activate the environment.

(MacOS/Linux) `source venv/bin/activate`

(Windows - cmd) `venv\Scripts\activate.bat`


In the environment, install requirements.txt (on Lab PCs use psycopg2-binary instead of psycopg2 as PostgreSQL is not installed).

`pip install -r requirements.txt`

Ensure you have completed a `.env`(Linux/MacOS) or `env.bat`(Windows) as specified in `example.env`. Note, that if you want to output to a database as well as CSV, DB_HOST will need to be specified too (e.g. "127.0.0.1"). If you are not using a database, you will see error/warning messages reported as the application looks for one. Manual setup of a PostgreSQL database is out of scope for these instructions.

Specify 

`./simple-run.sh <output-file>` (Linux/MacOS)

 `simple-run.bat <output-file>`(Windows cmd) 
 
 for a crawl with plain CSV output. For particular features like job [persistence](https://docs.scrapy.org/en/latest/topics/jobs.html), run using `scrapy crawl dvsvc <args...>`. 

Note: CSV output is only viewable once the crawler has finished. To see in batches, add
`FEED_EXPORT_BATCH_ITEM_COUNT = N` to `dvsvc_crawl/settings.py`, 
and run with file name of format `%(batch_id)d-filename%(batch_time)s.csv`.

The web crawler will still try to write to a database (specified by DB_HOST in .env if you would like to connect one), so you may get errors, but a CSV output will still be outputted even so.

Finally, use 

`deactivate` 

to exit the environment after scraping is complete. 

## Use in the CS labs

`podman` should be a direct replacement for Docker. `podman-compose` should be installable using `pip`.

## Running LLM on P&N cluster

Follow instructions provided by ITS to access cluster, and set up an interactive job.
Set up python venv and install `scripts/requirements.txt`, again following as advised by ITS, or using the instructions given in the `Run Just the Crawler` section .

Ensuring `starting_links.txt` is in the `resource` folder, run 

`scripts/download_starting_page_texts.py` 

to download the page to `resource/starting_page_texts`.

Then run the ollama container in the background, using docker or equivalent, again described in the ITS instructions. Alternatively, you can use apptainer instead, using the instructions [here](https://wiki.cs.st-andrews.ac.uk/index.php?title=Apptainer#Nvidia_container_images), replacing the commands to run llama with the ones in `run_model.sh`.

Finally run 

`scripts/submit_pages_to_model.py`

 which will output the llm responses to `resource/llm_response`.

Export llm responses from cluster to local PC as required.
On the local PC, to convert JSON responses to a collective CSV file, set `directory` and `output_file` paths as appropriate in `scripts/database_reformat.py`, and run that script.

## Cleaned LLM output database
 See README in `llm_out_db` folder.

## Common Issues
### PostgreSQL Issues

We've experienced some issues installing `psycopg2`.

If the issue is the `OpenSSL` is not discovered, try specifying it's location with the `pip` command.

`whereis openssl`

will provide the OpenSSL path, then use it in 

`LDFLAGS="-I<openssl-path>/include -L<openssl-path>/lib pip install -r requirements.txt`

Otherwise, use the psycopg2 binary instead, by changing `psycopg2==2.9.9` to `pyscopg2-binary` in `requirements.txt`




