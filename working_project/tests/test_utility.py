from working_project.src.utility import *
from working_project.src.models import WeatherTable
from pathlib import Path
from working_project.src.data_cleaning import parse_xml_to_raw_row_dict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import pytest


TEST_DIR = Path(__file__).parent
DATA_FILE = TEST_DIR / 'test_response_sample_fmi.xml'



def output_generator():
    with open(DATA_FILE, 'rb') as f:
        xml_bytes = f.read()
    
    dictionary_generator = parse_xml_to_raw_row_dict(xml_bytes)
    return dictionary_generator
def test_validate_data_outputs_dict():
    dict_generator = validate_data(output_generator())
    assert isinstance(next(dict_generator), dict)



def test_batch_output_size():
    list_total_4 = batch_data(output_generator(), 2)
    list_total_10 = batch_data(output_generator(), 5)

    total_4 = [x for x in list_total_4]
    total_10 = [x for x in list_total_10]

    assert len(total_10) == 10
    assert len(total_4) == 25


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    WeatherTable.metadata.create_all(engine)
    sess = Session(engine)
    yield sess

    sess.close()

def test_add_to_insert_que(session):
    
    
    total = 0
    for batch in batch_data(output_generator(), 1000):
        total += len(batch)
        add_to_insert_que(session, batch)
    result = session.execute(select(WeatherTable)).scalars().all()
    
    assert len(result) == total


def test_latest_timestamp(session):
    for batch in batch_data(output_generator(), 1000):
        add_to_insert_que(session, batch)
    
    latest_timestamp = latest_db_timestamp(session)
    query = select(WeatherTable.timestamps).order_by(WeatherTable.timestamps.desc()).limit(1)
    latest_manual_timestamp = session.execute(query).scalar_one_or_none()
    assert latest_timestamp == latest_manual_timestamp