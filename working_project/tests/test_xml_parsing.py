import pytest 
from src.data_cleaning import parse_response



def test_parse_response():
    with open('tests/test_response_sample_fmi.xml', 'rb') as f:
        xml_bytes = f.read()

        columns_rows_dict = parse_response(xml_bytes)

        assert isinstance(columns_rows_dict, dict)
        assert 'columns' in columns_rows_dict
        assert 'rows' in columns_rows_dict
        assert 'timestamps' in columns_rows_dict
        assert 'timestamps' in columns_rows_dict['columns']
        assert 'temperature' in columns_rows_dict['columns']            