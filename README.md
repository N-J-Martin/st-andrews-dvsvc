# st-andrews-dvsvc

A web crawler to discover UK-based domestic violence support services.

## Use with Docker

After building the image with `docker compose build`, run `docker compose up` to start four containers:

* `app` (the crawler)
* `db` (the PostgreSQL database server)
* `pgadmin`
* `ollama` (requires nvidia GPU)

This automatically loads environment variables from `.env` in the project directory. Set one up as per `example.env`.

To ensure use of `schema_dump.sql` to initialise database, need to remove `db_data` volume using `docker volume rm st-andrews-dvsvc_db_data` before using `up` command.

`docker compose run db pgadmin` will only spin up the database and pgAdmin containers. Access pgAdmin from a browser at port 5051, as specified in `compose.yaml`. The hostname of the database will be the container ID of db container.

## Run just the crawler (without Docker)
First, set up an virtual environment, with requirements.txt installed (on Lab PCs use psycopg2-binary instead of psycopg2).
Also ensure environement variables in .env are loaded, including DB_HOST (as seen [here](https://stackoverflow.com/questions/9554087/setting-an-environment-variable-in-virtualenv)).

Specify `./simple-run.sh <output-file>` for a crawl with plain CSV output. For particular features like job [persistence](https://docs.scrapy.org/en/latest/topics/jobs.html), run using `scrapy crawl dvsvc <args...>`. 

Note: CSV output only viewable once the crawler has finished. To see in batches, add
`FEED_EXPORT_BATCH_ITEM_COUNT = N` to `dvsvc_crawl/settings.py`, 
and run with file name of format `%(batch_id)d-filename%(batch_time)s.csv`.

## Use in the CS labs

`podman` should be a direct replacement for Docker. `podman-compose` should be installable using `pip`.
