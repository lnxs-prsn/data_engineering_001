from helsinki_weather_pipeline.src.models import WeatherTable
from helsinki_weather_pipeline.src.utility import (
    validate_data,
    add_to_insert_que,
    batch_data,
    latest_db_timestamp,
)
from helsinki_weather_pipeline.src.api_calls import call_fmi_api
from helsinki_weather_pipeline.src.data_cleaning import parse_xml_to_raw_row_dict
from sqlalchemy import create_engine
from decouple import config
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import inspect
from contextlib import contextmanager
import logging
from helsinki_weather_pipeline.src.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

user = config("POSTGRES_USER")
passw = config("POSTGRES_PASSWORD")
db = config("POSTGRES_DB")
db_host = config("POSTGRES_HOST", default="localhost")

path_to_db = f"postgresql://{user}:{passw}@{db_host}:5432/{db}"

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
    resp = call_fmi_api()

    try:

        with get_session() as session:
            if not inspector.has_table(WeatherTable.__tablename__):
                WeatherTable.metadata.create_all(bind=engine)
            latest_timestamp = latest_db_timestamp(session)
            for batch in batch_data(validate_data(parse_xml_to_raw_row_dict(resp)), 1000):
                if latest_timestamp:
                    batch[:] = [row for row in batch if row["timestamps"] > latest_timestamp]
                add_to_insert_que(session, batch)
                session.commit()
    except Exception as e:
        logger.error(f"Error caught {e}")
        raise


if __name__ == "__main__":
    main()
