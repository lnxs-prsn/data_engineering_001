from lxml import etree
import requests
import pandas 
# from api_calls import call_fmi_api

# resp = call_fmi_api()


def parse_response(resp) -> dict:

    """parse_response   
function receives binary from the call_api and parses the data to usable format for cleaning and storing to postgres db
:return: dictionary with columns, rows and timestamps
:rtype: dict    
"""

    root = etree.fromstring(resp)
    ns = root.nsmap
    rows = []
    columns1 = []
    time_stamps = []



    # gets the columns of the data from the xml 
    alist = [x.get('name').lower() for x in root.xpath('//swe:field', namespaces=ns)]
    columns1 = alist
    # print(columns1)

    # gets rows of the data from the xml
    for num, tvp in enumerate(root.xpath('//gml:doubleOrNilReasonTupleList', namespaces=ns)):
        alist = tvp.text.split('\n')
        arow = [x.strip().replace(' ', ',') for x in alist if x != '']
        rows = arow
        # print(rows[49])
    rows.pop(50)

    # gets timestamps from the xml
    for tvp in root.xpath('//gmlcov:positions', namespaces=ns):
        alist = tvp.text.split('\n')
        time_stamps = [x.strip().replace(' ', ',').replace(',,', ',').replace('60.16952,24.93545,', '') for x in alist if x != '']
        # print(time_stamps)
    time_stamps.pop(50)

    # organizes data in df usable way
    ready_rows = []
    for x in rows:
        alist = x.split(',')
        ready_rows.append(alist)

    data = {'columns': columns1, 'rows': ready_rows, 'timestamps': time_stamps}
    return data



def clean_data(data) -> pandas.DataFrame:
    """
    clean_data
    function receives dictionary from parse_response and cleans the data so it can be stored to postgres db
    :return: python dataframe
    :rtype: object
    """
    

    # data from xml is getting stored to df
    df = pandas.DataFrame(data['rows'], columns=data['columns'], dtype=float)
    # timestamps column is added to dataframe
    df['timestamps'] = data['timestamps']
    # type conversion for timestamps column
    df['timestamps'] = pandas.to_datetime(df['timestamps'].astype(int), unit='s')
    # NaN data column is dropped
    df = df.drop(columns=['radiationnetsurfacelwaccumulation'])
    # duplicates are dropped
    df = df.drop_duplicates()
    return df


