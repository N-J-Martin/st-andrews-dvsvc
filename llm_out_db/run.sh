#!/bin/bash
pg_ctl -D /var/lib/postgresql/data -l logfile start
python3 table_setup.py && python3 insert_llm_output_into_DB.py