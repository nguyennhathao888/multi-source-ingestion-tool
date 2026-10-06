import requests
from ingest import fetch_api
from unittest.mock import MagicMock,patch
import pytest
def test_fetch_api_success():
    source = {"name": "test", "url": "https://fake-url.com", "response_key": "products"}
    with patch("ingest.make_session") as mock_make_session:
        mock_session=MagicMock()
        mock_session.get.return_value.json.return_value={"products":[{"id":1,"title":"Fake"}]}
        mock_session.get.return_value.raise_for_status.return_value=None
        mock_make_session.return_value=mock_session
        result=fetch_api(source)
        assert len(result)==1
        assert result[0]["title"]=="Fake"

def test_fetch_api_failed():
    source = {"name": "test", "url": "https://fake-url.com", "response_key": "products"}
    with patch("ingest.make_session") as mock_make_session:
      mock_session=MagicMock()
      mock_session.get.return_value.raise_for_status.side_effect=requests.exceptions.HTTPError("...")
      mock_make_session.return_value=mock_session
      with pytest.raises(requests.exceptions.HTTPError):
        result=fetch_api(source)

      

      