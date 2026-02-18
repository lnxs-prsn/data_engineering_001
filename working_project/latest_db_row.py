from sqlalchemy import text, create_engine
from sqlalchemy.exc import ProgrammingError

def latest_timestamp(engine) -> object:
    """
    Docstring for latest_timestamp
    this function fetchest latest added row of the db table current_forecast
    
    :param engine: sqlalchemy engine
    :return: datetime object
    :rtype: object
    """


    with engine.connect() as conn:
        try:
            result = conn.execute(text('SELECT timestamps FROM current_forecast ORDER BY timestamps DESC LIMIT 1;'))
            # returns tuple (timestamp,)
            print(result)
            if result:
                latest = result.fetchone()
                return latest[0]
        except ProgrammingError as pe:
            print(f'error from {pe}')
            return False
        