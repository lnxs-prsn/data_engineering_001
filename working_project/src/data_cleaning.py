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
    column_names.append('timestamps')

    raw_time_rows = root.xpath('//gmlcov:positions', namespaces=ns)
    raw_data_rows = root.xpath('//gml:doubleOrNilReasonTupleList', namespaces=ns)
    
    for raw_data_row, raw_time_row in zip(raw_data_rows, raw_time_rows):
        for data_line, time_line  in zip(raw_data_row.text.split('\n'), raw_time_row.text.split('\n')):
            if not data_line.strip() or not time_line.strip():
                continue
            data_row = data_line.strip().split(' ')
            time_row = time_line.strip().split(' ')
            if not time_row[-1].strip() or not data_row[-1]:
                continue
            data_row.append(datetime.fromtimestamp(int(time_row[-1])))

            ready_row = data_row
            ready_dict = dict(zip(column_names, ready_row))
            ready_dict.pop('radiationnetsurfacelwaccumulation')
            yield ready_dict

