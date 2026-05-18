from working_project.src.data_cleaning import parse_xml_to_raw_row_dict
from working_project.src.models import WeatherModel
from pathlib import Path

from datetime import datetime

TEST_DIR = Path(__file__).parent
DATA_FILE = TEST_DIR / 'test_response_sample_fmi.xml'



def load_first_parsed_row():
    with open(DATA_FILE, 'rb') as f:
        xml_bytes = f.read()
    
    dictionary_generator = parse_xml_to_raw_row_dict(xml_bytes)
    return next(dictionary_generator)

def test_parse_xml_to_raw_row_dict():
    db_row_in_dict_format = load_first_parsed_row()

    assert len(db_row_in_dict_format) > 0
    assert 'timestamps' in db_row_in_dict_format.keys()
    assert 'temperature' in db_row_in_dict_format.keys()
    assert isinstance(db_row_in_dict_format['timestamps'], datetime) 



def test_data_cleaning():
    db_row_in_dict_format = load_first_parsed_row()
    assert 'radiationnetsurfacelwaccumulation' not in db_row_in_dict_format
    assert 'temperature' in db_row_in_dict_format 
    assert db_row_in_dict_format['temperature'] != "NaN"

def test_validate_timestamps():
    db_row_in_dict_format = load_first_parsed_row()
    validated_model = WeatherModel(**db_row_in_dict_format) 

    assert validated_model.timestamps == datetime(2026, 2, 21, 16, 0)
    assert validated_model.timestamps.year == 2026


# test_validate_data()