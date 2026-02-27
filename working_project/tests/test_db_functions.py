import pytest 
import unittest
import datetime
from working_project.src.db_functions import create_tables, latest_timestamp
from sqlalchemy.exc import ProgrammingError 
from sqlalchemy import text, create_engine  
from unittest.mock import MagicMock, patch, Mock

latest_timestamp1 = '2026-02-27 19:00:00'






def test_latest_timestamp_with_mocks():
    # Create a mock engine and connection
    mock_engine = MagicMock()
    mock_connection = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_connection

    # Mock the result of the SQL query
    mock_result = MagicMock()
    mock_result.fetchone.return_value = (latest_timestamp1,)
    mock_connection.execute.return_value = mock_result

    # Call the function with the mocked engine
    result = latest_timestamp(mock_engine)

    # Assert that the function returns the expected timestamp
    assert result == latest_timestamp1


# class TestDBFunctions(unittest.TestCase):
#     """TestDBFunctions
#     this class is for testing db_functions.py functions
    
#     """
    
#     def test_create_tables(self):
#         pass    
#     def test_latest_timestamp_with_mocks( self):
#         pass