# from working_project.src
from working_project.src.models import WeatherModel, WeatherTable
from working_project.src.utility import validate_data, insert_to_db, batch_data
from working_project.src.api_calls import call_fmi_api
from working_project.src.data_cleaning import parse_xml_to_raw_row_dict
from sqlalchemy import create_engine
from decouple import config
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import inspect
from contextlib import contextmanager

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
    print('why not working ')

    resp = call_fmi_api()


    for dict_row in parse_xml_to_raw_row_dict(resp):
        validate_data(dict_row)
    with get_session() as session:
        if not inspector.has_table(WeatherTable.__tablename__):
            WeatherTable.metadata.create_all(bind=engine)
        for batch in batch_data(parse_xml_to_raw_row_dict(resp), 1000):
            insert_to_db(session, batch)

if __name__ == "__main__":
    main()