import requests 
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import logging

logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

# this file is responsible for calling the api and fetching data from it
@retry(stop=stop_after_attempt(3), wait=wait_fixed(4), retry=retry_if_exception_type(requests.RequestException), 
       before_sleep= lambda retry_status: logger.warning(f'retrying after error {retry_status}' ))
def call_fmi_api() -> bytes:
    """
    call_api_to_fmi
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
    logger.info('calling api')
    resp = requests.get(url=url, params=params)
    resp.raise_for_status()
    # print(type(resp.content))  


    return resp.content 

# call_fmi_api()
