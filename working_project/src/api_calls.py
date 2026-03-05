import requests 
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import logging
import yaml
from pathlib import Path


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

    script_dir = Path(__file__).parent

    with open(script_dir / 'config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        # text = file.read()
    # print(text)
    url = config['api']['base_url']
    params = {
        'service':config['services']['service1'],
        'version':config['versions']['version2'],
        'request':config['requests']['getfeature'],
        'storedquery_id':config['query_id']['forecast_id'],
        'place':config['location']['name'],
        # 'starttime': '',
        # 'endtime':'',
    }
    # not sure if there should be comments here as its self explanatory
    ##
    print(f'reached here which means that the config worked {url}')
    logger.info('calling api')
    resp = requests.get(url=url, params=params)
    resp.raise_for_status()
    # print(type(resp.content))  


    return resp.content 

call_fmi_api()
