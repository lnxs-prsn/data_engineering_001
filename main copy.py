import pandas as pd 
import requests
from sqlalchemy import create_engine
from working_project.data_cleaning import clean_data
from working_project.create_db import create_tables
from working_project.api_calls import call_api
from working_project.latest_db_row import latest_timestamp


# 
def the_project():
    """
    this method stores data to the postgres tables 
    raw_forecast and current_forecast
    returns: boolean
    """

    path_to_db = 'postgresql://myuser:mypassword@localhost:5432/mydatabase'
    engine = create_engine(path_to_db)

    resp = call_api()
    if resp == None:
        raise TypeError('response of the api request is None expected xml')

    df = clean_data(resp)
    # fetches most recent timestamp from the db 
    if latest_time := latest_timestamp(engine): 
            df = df[df['timestamps'] > latest_time].reset_index(drop=True)
    print(len(df))
    print('here and all good')
    if create_tables(engine) and not df.empty:
        try:
            df.to_sql('raw_forecast', engine, if_exists='append', index=False, method='multi', chunksize=500)
            df.to_sql('current_forecast', engine, if_exists='append', index=False, method='multi', chunksize=500)
        except Exception as e:
            print('error is likely related to duplicate data in current_forecast table')
            print(f'there was error {e}')
    return True

def main():
    the_project()


if __name__ == "__main__":
    main()