from helsinki_weather_pipeline.src.models import WeatherModel, WeatherTable
from typing import Generator
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from sqlalchemy import select
import logging
from pydantic import ValidationError
from logging.handlers import RotatingFileHandler
from datetime import datetime


handler = RotatingFileHandler("weather_app.log", maxBytes=1_000_000, backupCount=3)
handler.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def validate_data(dict_generator: Generator[dict, None, None]) -> Generator[dict, None, None]:
    """
    Validate weather data and optionally return the validated model.

    Args:
        dict_generator: Dictionary containing raw weather data.

    Returns:
        Generator[dict,None,None]
    """
    wrong_data = []
    total_rows = 0
    for raw_row_dict in dict_generator:
        total_rows += 1

        try:
            model = WeatherModel(**raw_row_dict)
            yield model.model_dump()
        except (TypeError, ValueError, ValidationError) as e:
            logger.info(f"Errors found: {e}")
            wrong_data.append(raw_row_dict)
    if wrong_data and len(wrong_data) / total_rows > 0.5:
        raise ValueError(
            f"more than 50 percent of the rows failed to validate. total failures: {wrong_data}"
        )
    elif wrong_data:
        logger.warning(f"{len(wrong_data)} rows failed validation, continuing with the rest")


def batch_data(
    parse_xml_to_raw_row_dict: Generator[dict, None, None], batch_size: int
) -> Generator[list, None, None]:
    """
    iterates rows from parser
    yields list which length <= batch_size

    args:
        parse_xml_to_raw_row_dict: Generator yielding row of dict
        batch_size: int

    returns:
        Generator/iterable list
        or
        none

    """
    if parse_xml_to_raw_row_dict:
        batch = []
        for row in parse_xml_to_raw_row_dict:
            batch.append(row)
            if len(batch) >= batch_size:
                yield batch
                batch = []
        if batch:
            yield batch


def add_to_insert_que(
    db_session: Session,
    batch: list[dict],
) -> None:
    """

    Inserts weather data into the database.

    if timestamp already exists in the database it wont be inserted to database

    """
    if not batch:
        return None

    stmt = insert(WeatherTable).values(batch)
    stmt = stmt.on_conflict_do_nothing(index_elements=["timestamps"])
    db_session.execute(stmt)


def latest_db_timestamp(session: Session) -> datetime | None:
    query_latest_timestamp = (
        select(WeatherTable.timestamps).order_by(WeatherTable.timestamps.desc()).limit(1)
    )
    newest_db_timestamp = session.execute(query_latest_timestamp).scalar_one_or_none()
    return newest_db_timestamp
