from unittest.mock import patch, Mock
from helsinki_weather_pipeline.src.api_calls import call_fmi_api


def test_call_fmi_api_returns_bytes():
    fake_response = Mock()
    fake_response.content = b"fake data"
    fake_response.raise_for_status = Mock()

    with patch(
        "working_project.src.api_calls.requests.get", return_value=fake_response
    ) as mock_get:
        result = call_fmi_api()
        assert isinstance(result, bytes)
        assert result == b"fake data"

        mock_get.assert_called_once()
