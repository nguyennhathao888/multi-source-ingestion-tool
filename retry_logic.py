import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def make_session():
    po_retry=Retry(
        total=3,
        status_forcelist=[500,502,503,504],
        backoff_factor=0.5
    )
    adapter = HTTPAdapter(max_retries=po_retry)
    session=requests.Session()
    session.mount("http://",adapter)
    session.mount("https://",adapter)
    return session


