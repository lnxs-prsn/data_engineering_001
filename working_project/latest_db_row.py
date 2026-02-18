from sqlalchemy import text, create_engine
from sqlalchemy.exc import ProgrammingError

# import psycopg2



# def latest_timestamp() -> object:

#     conn = psycopg2.connect(host='localhost', port='5432', dbname='mydatabase', user='myuser', password='mypassword')
#     cur  = conn.cursor()

#     cur.execute('SELECT timestamps FROM current_forecast ORDER BY timestamps DESC LIMIT 1;')
#     # returns tuple (timestamp,)
#     latest = cur.fetchone()
#     latest, _ = latest
#     return latest[0]


def latest_timestamp(engine) -> object:
    """
    Docstring for latest_timestamp
    this function fetchest latest added row of the db
    
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
        
latest_timestamp(engine)