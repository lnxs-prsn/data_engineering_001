# from working_project.src
from working_project.src.models import WeatherTable
from working_project.src.utility import validate_data, insert_to_db, batch_data, latest_db_timestamp
from working_project.src.api_calls import call_fmi_api
from working_project.src.data_cleaning import parse_xml_to_raw_row_dict
from sqlalchemy import create_engine
from decouple import config
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import inspect
from contextlib import contextmanager
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)
print('hello')

user = config('POSTGRES_USER')
passw = config('POSTGRES_PASSWORD')
db = config('POSTGRES_DB')
db_host = config('POSTGRES_HOST', default='localhost')

path_to_db = f'postgresql://{user}:{passw}@{db_host}:5432/{db}'

engine = create_engine(path_to_db)

SessionLocal = sessionmaker(bind=engine)
inspector = inspect(engine)

@contextmanager
def get_session():
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()




def main():
    """
    calls api, 
    parses data, 
    validates data, 
    batches data, 
    inserts data to db  
    """
    print('hellou')

    # resp = call_fmi_api()
    with open('working_project/src/test_response_sample_fmi.xml', 'rb') as resp:
        resp = resp.read()
    
        try:
            print('hello1')
            
            with get_session() as session:
                print('hello2')
                if not inspector.has_table(WeatherTable.__tablename__):
                    WeatherTable.metadata.create_all(bind=engine)
                    
                for batch in batch_data(validate_data(parse_xml_to_raw_row_dict(resp)), 1000):
                    print('helo')
                    if latest_timestamp:=latest_db_timestamp(session):
                        batch[:] = [row for row in batch if row['timestamps'] > latest_timestamp ]
                    insert_to_db(session, batch)
        except Exception as e:
            logging.info(f'Error caught {e}')
if __name__ == "__main__":
    main()