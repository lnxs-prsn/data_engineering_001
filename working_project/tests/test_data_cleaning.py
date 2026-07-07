from working_project.src.data_cleaning import parse_xml_to_raw_row_dict
from working_project.src.utility import validate_data
from pathlib import Path

from datetime import datetime, timezone

TEST_DIR = Path(__file__).parent
DATA_FILE = TEST_DIR / 'test_response_sample_fmi.xml'



def load_first_parsed_row():
    with open(DATA_FILE, 'rb') as f:
        xml_bytes = f.read()
    
    dictionary_generator = parse_xml_to_raw_row_dict(xml_bytes)
    return dictionary_generator

def test_parse_xml_to_raw_row_dict():
    db_row_in_dict_format = load_first_parsed_row()

    assert len(next(db_row_in_dict_format)) > 0
    assert 'timestamps' in next(db_row_in_dict_format).keys()
    assert 'temperature' in next(db_row_in_dict_format).keys()
    assert isinstance(next(db_row_in_dict_format)['timestamps'], datetime) 



def test_data_cleaning():
    db_row_in_dict_format = load_first_parsed_row()
    assert 'radiationnetsurfacelwaccumulation' not in next(db_row_in_dict_format)
    assert 'temperature' in next(db_row_in_dict_format) 
    assert next(db_row_in_dict_format)['temperature'] != "NaN"

def test_validate_distinct_timestamps():
    db_row_in_dict_format = load_first_parsed_row()
    validated_model = validate_data(db_row_in_dict_format) 
    distinct_timestamps = []
    duplicate_timestamps =  []
    for row in validated_model:
        if row['timestamps'] not in row.items():
            distinct_timestamps.append(row['timestamps'])
        else:
            duplicate_timestamps.append(row['timestamps'])
    assert len(duplicate_timestamps) == 0
