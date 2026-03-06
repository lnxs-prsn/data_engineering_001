from working_project.src.data_cleaning import parse_response



def test_parse_response():
    with open('./test_response_sample_fmi.xml', 'rb') as f:
        xml_bytes = f.read()

        columns_rows_dict = parse_response(xml_bytes)


        print(columns_rows_dict['timestamps'][0])

        assert isinstance(columns_rows_dict, dict)
        assert 'columns' in columns_rows_dict
        assert 'rows' in columns_rows_dict
        assert 'timestamps' in columns_rows_dict
        assert isinstance(columns_rows_dict['columns'][0], str)
        assert isinstance(columns_rows_dict['timestamps'][0], str)