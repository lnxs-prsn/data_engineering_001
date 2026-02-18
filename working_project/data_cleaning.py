from lxml import etree
import requests
import pandas as pd
# from api_calls import call_api

# resp = call_api()
def clean_data(resp):
    root = etree.fromstring(resp)
    ns = root.nsmap
    rows = []
    columns1 = []
    time_stamps = []



    # columns
    alist = [x.get('name').lower() for x in root.xpath('//swe:field', namespaces=ns)]
    columns1 = alist
    # print(columns1)

    for num, tvp in enumerate(root.xpath('//gml:doubleOrNilReasonTupleList', namespaces=ns)):
        alist = tvp.text.split('\n')
        arow = [x.strip().replace(' ', ',') for x in alist if x != '']
        rows = arow
        # print(rows[49])
    rows.pop(50)

    # timestamps
    for tvp in root.xpath('//gmlcov:positions', namespaces=ns):
        alist = tvp.text.split('\n')
        time_stamps = [x.strip().replace(' ', ',').replace(',,', ',').replace('60.16952,24.93545,', '') for x in alist if x != '']
        # print(time_stamps)
    time_stamps.pop(50)


    ready_rows = []
    for x in rows:
        alist = x.split(',')
        ready_rows.append(alist)



    df = pd.DataFrame(ready_rows, columns=columns1, dtype=float)

    df['timestamps'] = time_stamps

    df['timestamps'] = pd.to_datetime(df['timestamps'].astype(int), unit='s')

    # NaN data
    df = df.drop(columns=['radiationnetsurfacelwaccumulation'])

    df = df.drop_duplicates()
    return df
# clean_data(resp)