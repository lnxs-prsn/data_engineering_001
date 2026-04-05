from working_project.src.data_cleaning import parse_xml_to_raw_row_dict
from working_project.src.utility import validate_data
from working_project.src.models import WeatherModel


from datetime import datetime


def test_parse_xml_to_raw_row_dict():
    with open('./working_project/tests/test_response_sample_fmi.xml', 'rb') as f:
        xml_bytes = f.read()

        dictionary_generator = parse_xml_to_raw_row_dict(xml_bytes)
        db_row_in_dict_format = next(dictionary_generator)

        assert len(db_row_in_dict_format) > 0
        assert 'timestamps' in db_row_in_dict_format.keys()
        assert 'temperature' in db_row_in_dict_format.keys()
        assert type(db_row_in_dict_format['timestamps']) == datetime


# test_parse_xml_to_raw_row_dict()


# def test_validate_data():
#     with open('./working_project/tests/test_response_sample_fmi.xml', 'rb') as f:
#         xml_bytes = f.read()

#     dictionary_generator = parse_xml_to_raw_row_dict(xml_bytes)
#     validated_model = WeatherModel(**next(dictionary_generator)) 

#     assert validated_model.timestamps == datetime(2026, 2, 21, 16, 0)
#     assert validated_model.timestamps.year == 2026


# test_validate_data()