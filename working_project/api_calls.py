import requests as rq

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

    resp = rq.get(url=url, params=params)
    if resp.ok:
        return resp
    return resp.raise_for_status()