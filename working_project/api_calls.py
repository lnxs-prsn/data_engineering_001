import requests 

def call_api():
    url = 'https://opendata.fmi.fi/wfs'
    params = {
        'service':'WFS',
        'version':'2.0.0',
        'request':'getFeature',
        'storedquery_id':'fmi::forecast::harmonie::surface::point::multipointcoverage',
        'place':'helsinki',
        # 'starttime': '',
        # 'endtime':'',
    }

    resp = requests.get(url=url, params=params)
    resp.raise_for_status()
    return resp.content