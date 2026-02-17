import pandas as pd 
import requests
from sqlalchemy import create_engine
from api_calls import call_api
from data_cleaning import clean_data
from working_project.create_db import create_tables

def working_project():
    path_to_db = 'postgresql://myuser:mypassword@localhost:5432/mydatabase'
    engine = create_engine(path_to_db)

    resp = call_api()
    df = clean_data(resp)
    print('here and all good')
    if create_tables() == 'success':
        print('all ready to go')
        df.to_sql('raw_forecast', engine, if_exists='append', index=False, method='multi', chunksize=500)
    return 'all done api call was made, response was parsed, cleaned and added to database'