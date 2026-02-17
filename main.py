import pandas as pd 
import requests
from sqlalchemy import create_engine
from working_project.data_cleaning import clean_data
from working_project.create_db import create_tables
from working_project.api_calls import call_api

# 
def the_project():
    """
    this method uses stores data to the postgres tables 
    raw_forecast and current_forecast
    """

    path_to_db = 'postgresql://myuser:mypassword@localhost:5432/mydatabase'
    engine = create_engine(path_to_db)

    resp = call_api()
    df = clean_data(resp)
    print('here and all good')
    if create_tables() == 'success':
        try:
            df.to_sql('raw_forecast', engine, if_exists='append', index=False, method='multi', chunksize=500)
            df.to_sql('current_forecast', engine, if_exists='append', index=False, method='multi', chunksize=500)
        except Exception as e:
            print('error is likely related to duplicate data in current_forecast table')
            print(f'there was error {e}')
    return 'all done api call was made, response was parsed, cleaned and added to database'

def main():
    the_project()


if __name__ == "__main__":
    main()