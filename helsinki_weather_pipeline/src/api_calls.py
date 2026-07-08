import requests
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import logging
import yaml
from pathlib import Path


logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(4),
    retry=retry_if_exception_type(requests.RequestException),
    before_sleep=lambda retry_status: logger.warning(f"retrying after error {retry_status}"),
)
def call_fmi_api() -> bytes:
    """
    call_api_to_fmi
    function fetches data from wfs api from Finnish Meteorological Institute
    :return: content of the requests
    :rtype: bytes
    """

    script_dir = Path(__file__).parent

    with open(script_dir / "config.yaml", "r") as file:
        config = yaml.safe_load(file)
    url = config["api"]["base_url"]
    params = {
        "service": config["services"]["service1"],
        "version": config["versions"]["version2"],
        "request": config["requests"]["getfeature"],
        "storedquery_id": config["query_id"]["forecast_id"],
        "place": config["location"]["name"],
        # 'starttime': '',
        # 'endtime':'',
    }

    logger.info("calling api")
    resp = requests.get(url=url, params=params, timeout=(5, 20))
    resp.raise_for_status()

    return resp.content
