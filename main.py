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

TEST_DIR = Path(__file__).parent
DATA_FILE = TEST_DIR / 'test_response_sample_fmi.xml'



def main():
    """
    calls api, 
    parses data, 
    validates data, 
    batches data, 
    inserts data to db  
    """
        
    resp = call_fmi_api()
    

    for dict_row in parse_xml_to_raw_row_dict(resp):
        validate_data(dict_row)
    with get_session() as session:
        if not inspector.has_table(WeatherTable.__tablename__):
            WeatherTable.metadata.create_all(bind=engine)
        for batch in batch_data(parse_xml_to_raw_row_dict(resp), 1000):
            if latest_timestamp:=latest_db_timestamp(session):
                batch[:] = [row for row in batch if row['timestamps'] > latest_timestamp ]
            insert_to_db(session, batch)

if __name__ == "__main__":
    main()