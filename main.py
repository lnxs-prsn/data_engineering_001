import pandas
import requests
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from working_project.src.data_cleaning import clean_data, parse_response
from working_project.src.db_functions import create_tables, latest_timestamp
from working_project.src.api_calls import call_fmi_api
from decouple import config
import logging

logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")
# pipeline test
logger = logging.getLogger(__name__)
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
    user = config('POSTGRES_USER')
    passw = config('POSTGRES_PASSWORD')
    db = config('POSTGRES_DB')
    db_host = config('POSTGRES_HOST', default='localhost')

    path_to_db = f'postgresql://{user}:{passw}@{db_host}:5432/{db}'

    engine = create_engine(path_to_db)

    resp = call_fmi_api()
    if not resp:
        logger.error(f'API response is None {resp}')
        raise TypeError('response of the api request is None expected xml')

    df = clean_data(parse_response(resp))
    # fetches most recent timestamp from the db 
    if latest_time := latest_timestamp(engine): 
            logger.info(f'latest time stamp in the DB: {latest_time}')
            df = df[df['timestamps'] > latest_time].reset_index(drop=True)
            logger.info(f'new data to insert {len(df)} rows')
    else:
        logger.info('no existing data in the DB table empty or missing')
    
    if df.empty:
            logger.error(f'Data frame empty no new data to insert')
            return (False, f'dataframe is empty. lastest timestamp in db is {latest_time} ')
    try:
        # tables are created if they dont exits
        
        if not (tables:=create_tables(engine)):
            logger.error(f'Failed to create database tables')
            return (False, 'tables were not created')
        
        logger.info(f'inserting {len(df) }rows')
        df.to_sql('raw_forecast', engine, if_exists='append', index=False, method='multi', chunksize=500)
        df.to_sql('current_forecast', engine, if_exists='append', index=False, method='multi', chunksize=500)
        logger.info('Data was inserted successfully')
        return (True, 'database was updated')
    except SQLAlchemyError as e:
        logger.info(f'Database error: {e}', exc_info=True)
        return(False, f'an error occurred while saving data to the database')


def main():
    try:
        result = the_project()
        if isinstance(result, tuple):
            is_success, message = result
            if is_success:
                logger.info('database was updated')
            else:
                logger.warning(f'database update failed: {message}')
        else:
            logger.error('unexpected return value from the_project function')
    except Exception as e:
        logger.critical(f'Unhandled error in the main() {e}', exc_info=True)
        raise


if __name__ == "__main__":
    main()