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

#tvp = timevaluepair?
    for idx, tvp in enumerate(root.xpath('//gml:doubleOrNilReasonTupleList', namespaces=ns)):
        if not tvp.text:
            continue
        
        for row_of_raw_values in tvp.text.split('\n'):
            if not row_of_raw_values.strip():
                continue
            
            row_of_cleaned_values = row_of_raw_values.split()
            if len(row_of_cleaned_values) != len(column_names):
                continue
            raw_row_dict = dict(zip(column_names, row_of_cleaned_values))
            nan_keys = [k for k, v in raw_row_dict.items() if v == "NaN"]  # ['radiationnetsurfacelwaccumulation']
            for k in nan_keys:
                del raw_row_dict[k]

            if idx < len(time_stamps):
                raw_row_dict['timestamps'] = datetime.fromtimestamp(int(time_stamps[idx]))
            yield raw_row_dict
    logger.debug(f' these columns have nan values and were excluded from the db {nan_keys}')








