import pytest 
from unittest.mock import Mock, patch
from working_project.src.data_cleaning import clean_data



def test_clean_data_returns_object():
    with open('test_response_sample_fmi.xml', 'rb') as f:
        xml_bytes = f.read()

        df = clean_data(xml_bytes)

        assert not df.empty
        assert 'timestamps' in df.columns
        assert 'temperature' in df.columns