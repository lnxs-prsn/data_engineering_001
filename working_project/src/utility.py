from working_project.src.models import WeatherModel, WeatherTable
from typing import Generator
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from sqlalchemy import select
import logging
from pydantic import ValidationError


logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


def validate_data(raw_row_dict: dict, return_validated_data: bool=False) -> WeatherModel | None:
    """
    Validate weather data and optionally return the validated model.

    Args:
        raw_row_dict: Dictionary containing raw weather data.
        return_validated_data: If True, return the validated WeatherModel instance.

    Returns:
        WeatherModel if validation succeeds and return_validated_data is True,
        otherwise None.
    """
    try:
        model = WeatherModel(**raw_row_dict)
        if return_validated_data:
            return model
    except (TypeError, ValueError, ValidationError) as e:
        logger.debug(f'Errors found: {e}')

        


    
    


def batch_data(parse_xml_to_raw_row_dict: Generator[dict, None, None], batch_size: int) -> Generator[list, None, None]:
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



def insert_to_db(db_session: Session, batch: list[dict],  ) -> None:
    """

    Inserts weather data into the database.

    if timestamp already exists in the database it wont be inserted to database
    
    """
    if not batch:
        return None
    
    stmt = insert(WeatherTable).values(batch)
    stmt = stmt.on_conflict_do_nothing(index_elements=['timestamps'])
    db_session.execute(stmt)
    db_session.commit()


def latest_db_timestamp(session: Session):
    query_latest_timestamp = select(WeatherTable.timestamps).order_by(WeatherTable.timestamps.desc()).limit(1)
    newest_db_timestamp = session.execute(query_latest_timestamp).scalar_one_or_none()
    return newest_db_timestamp