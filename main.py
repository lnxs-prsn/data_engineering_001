import pandas as pd 
import requests
from sqlalchemy import create_engine
from working_project.data_cleaning import clean_data
from working_project.db_functions import create_tables, latest_timestamp
from working_project.api_calls import call_fmi_api
from decouple import config


# 
def the_project():
    """
    this method stores data to postgres tables 
    raw_forecast and current_forecast
    returns: bool
    :rtype: bool
    """
    # decouple gets path from .env
    path_to_db = config('PATH_TO_DB')
    engine = create_engine(path_to_db)

    resp = call_fmi_api()
    if not resp:
        raise TypeError('response of the api request is None expected xml')

    df = clean_data(resp)
    # fetches most recent timestamp from the db 
    if latest_time := latest_timestamp(engine): 
            df = df[df['timestamps'] > latest_time].reset_index(drop=True)
    # tables are created if they dont exits
    if not df.empty and create_tables(engine):
        try:
            df.to_sql('raw_forecast', engine, if_exists='append', index=False, method='multi', chunksize=500)
            df.to_sql('current_forecast', engine, if_exists='append', index=False, method='multi', chunksize=500)
        except Exception as e:
            print('error is likely related to duplicate data in current_forecast table')
            print(f'there was error {e}')
    return True

def main():
    if the_project():
        return 'database was updated'


if __name__ == "__main__":
    main()