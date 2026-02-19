import requests 
# change the name to fetch weather data
def call_api() -> bytes:
    """
    call_api
    function fetches data from wfs api from Finnish Meteorological Institute
    :return: content of the requests
    :rtype: bytes
    """
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
    # not sure if there should be comments here as its self explanatory
    ##
    resp = requests.get(url=url, params=params)
    resp.raise_for_status()
    # print(type(resp.content))  
    return resp.content 

# call_api()
