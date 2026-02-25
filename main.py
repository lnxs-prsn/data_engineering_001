import pandas
import requests
from sqlalchemy import create_engine
from working_project.src.data_cleaning import clean_data, parse_response
from working_project.src.db_functions import create_tables, latest_timestamp
from working_project.src.api_calls import call_fmi_api
from decouple import config



# 
def the_project() -> tuple[bool, str]:
    """
    this method stores data to postgres tables 
    raw_forecast and current_forecast
    returns: tuple[bool, str]
    :rtype: tuple[bool, str]
     - bool: indicates if the database was updated successfully
     - str: message providing additional information about the operation
     - "database was updated" if the operation was successful
     - "dataframe is empty" if there is no new data to insert
     - "tables were not created" if the database tables could not be created
     - error message if an exception occurred during the database update process
    """
    # decouple gets path from .env
    path_to_db = config('PATH_TO_DB')
    engine = create_engine(path_to_db)

    resp = call_fmi_api()
    if not resp:
        raise TypeError('response of the api request is None expected xml')

    df = clean_data(parse_response(resp))
    # fetches most recent timestamp from the db 
    if latest_time := latest_timestamp(engine): 
            df = df[df['timestamps'] > latest_time].reset_index(drop=True)
    
    try:
        # tables are created if they dont exits
        if not df.empty and (tables := create_tables(engine)):
            print(len(df), print(tables))
            df.to_sql('raw_forecast', engine, if_exists='append', index=False, method='multi', chunksize=500)
            df.to_sql('current_forecast', engine, if_exists='append', index=False, method='multi', chunksize=500)
            return (True, 'database was updated')
        elif df.empty:
            return (False, f'dataframe is empty. lastest timestamp in db is {latest_time} ')
        elif not tables:
            return (False, 'tables were not created')
    except Exception as e:
        return (False, f'an error occurred while saving data to the database: {e}')
    

def main():
    try:
        result = the_project()
        if isinstance(result, tuple):
            is_success, message = result
            if is_success:
                print('database was updated')
            else:
                print(f'database update failed: {message}')
        else:
            print('unexpected return value from the_project function')
    except Exception as e:
        print(e) 
        


if __name__ == "__main__":
    main()