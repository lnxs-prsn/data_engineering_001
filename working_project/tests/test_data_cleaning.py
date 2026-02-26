import pytest 
from unittest.mock import Mock, patch
from src.data_cleaning import clean_data, parse_response
import pandas



def test_clean_data_returns_object():
    with open('tests/test_response_sample_fmi.xml', 'rb') as f:
        xml_bytes = f.read()

        columns_rows_timestamps = parse_response(xml_bytes)
        df = clean_data(columns_rows_timestamps)



        assert not df.empty
        assert 'timestamps' in df.columns
        assert 'temperature' in df.columns
        assert df['timestamps'].dtype == 'datetime64[s]'
        assert df['temperature'].dtype == 'float64'

test_clean_data_returns_object()