from lxml import etree
import requests
from typing import Generator
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)



def parse_xml_to_raw_row_dict(resp: requests.Response) -> Generator[dict, None, None]:
    
    """
    function receives binary from the call_api and parses the data to usable format for cleaning and storing to postgres db
    :return: Generator which yields dictionary
    :rtype: Generator[dict, None, None]   
    
    """
    root = etree.fromstring(resp)
    ns = root.nsmap
    time_stamps = []



    # gets the columns of the data from the xml 
    column_names = [x.get('name').lower() for x in root.xpath('//swe:field', namespaces=ns)]

    # gets timestamps from the xml
    for tvp in root.xpath('//gmlcov:positions', namespaces=ns):
        if not tvp.text:
            continue
        for line in tvp.text.split('\n'):
            if line.strip():
                time_stamps.append(line.split()[-1])


    for idx, tvp in enumerate(root.xpath('//gml:doubleOrNilReasonTupleList', namespaces=ns)):
        if not tvp.text:
            continue
        
        for line in tvp.text.split('\n'):
            if not line.strip():
                continue
            
            row_values = line.split()
            if len(row_values) != len(column_names):
                continue
            raw_row_dict = dict(zip(column_names, row_values))
            nan_keys = [k for k, v in raw_row_dict.items() if v == "NaN"]  # ['radiationnetsurfacelwaccumulation']
            for k in nan_keys:
                del raw_row_dict[k]

            if idx < len(time_stamps):
                raw_row_dict['timestamps'] = datetime.fromtimestamp(int(time_stamps[idx]))
            yield raw_row_dict
    logger.info(f' these columns have nan values and were excluded from the db {nan_keys}')





# def clean_data(columns_rows_timestamps: dict) -> pandas.DataFrame:
#     """
#     clean_data
#     function receives dictionary from parse_response and cleans the data so it can be stored to postgres db
#     :return: python dataframe
#     :rtype: object
#     """
#     data = columns_rows_timestamps

#     # data from xml is getting stored to df
#     df = pandas.DataFrame(data['rows'], columns=data['columns'], dtype=float)
#     # timestamps column is added to dataframe
#     df['timestamps'] = data['timestamps']
#     # type conversion for timestamps column
#     df['timestamps'] = pandas.to_datetime(df['timestamps'].astype(int), unit='s')
#     # NaN data column is dropped
#     df = df.drop(columns=['radiationnetsurfacelwaccumulation'])
#     # duplicates are dropped
#     df = df.drop_duplicates()
#     return df





