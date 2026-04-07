from working_project.src.models import WeatherModel, WeatherTable
from typing import Generator
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

def validate_data(raw_row_dict: dict, num: int=0) -> WeatherModel | bool:
    if num == 1:
        return WeatherModel(**raw_row_dict)
    if WeatherModel(**raw_row_dict):
        return True
    
    


def batch_data(parse_xml_to_raw_row_dict: Generator[dict, None, None], batch_size: int) -> Generator[dict, None, None]:
    """
    """
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
    this function silently ignores duplicate data insertion
    be aware if intenttion is to add data from multiple stations
    """
    if not batch:
        return 0
    
    stmt = insert(WeatherTable).values(batch)
    stmt = stmt.on_conflict_do_nothing(index_elements=['timestamps'])
    result = db_session.execute(stmt)
    db_session.commit()