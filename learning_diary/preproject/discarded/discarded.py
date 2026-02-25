# xmltodict
# data = xmltodict.parse(resp.content)
# print(data)

# members = data['wfs:FeatureCollection'].get('wfs:member')
# if not isinstance(members, list):
#     members = [members]

# observations = []







# # mix of failed approached 

# import requests as rq
# import pandas as pd
# import xml.etree.ElementTree as ET
# from lxml import etree

# # calling api
# resp = rq.get('http://opendata.fmi.fi/wfs/fin?service=WFS&version=2.0.0&request=GetFeature&storedquery_id=fmi::observations::weather::timevaluepair&fmisid=101520&')


# xml solution
# root = ET.fromstring(resp.text)
# rows = []

# ns = {
#     "wml2": "http://www.opengis.net/waterml/2.0"
# }

# for tvp in root.findall(".//wml2:MeasurementTVP", ns):
#     time = tvp.find('wml2:time', ns).text
#     value = tvp.find('wml2:value', ns).text
#     rows.append((time, value))

# print(rows[0])


# lxml solution
# 
# root = etree.fromstring(resp.text.encode())
# times = root.xpath('//wml2:time', namespaces=root.nsmap)
# value = root.xpath('//wml2:value', namespaces=root.nsmap)
# ns = root.nsmap
# 
# cleanin data 
# lxml_rows = []
# for tvp in root.xpath('//wml2:MeasurementTVP', namespaces=ns):
    # time = tvp.xpath('./wml2:time/text()', namespaces=ns)[0]
    # value = tvp.xpath('./wml2:value/text()', namespaces=ns)[0]
    # print(str(time))
    # lxml_rows.append({
        # 'time': time,
        # 'value': float(value),
    # })
# 
# converting to dataframe 
# df1 = pd.DataFrame(lxml_rows)
# df1.head()
# 
# 
# 