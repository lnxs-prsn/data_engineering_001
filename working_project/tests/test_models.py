from working_project.src.models import WeatherModel
from decimal import Decimal
import pytest
from pydantic import ValidationError
import datetime

data = {
    "pressure": "1020.0",
    "geopheight": "7.7",
    "temperature": "5.1",
    "dewpoint": "2.5",
    "humidity": "83.9",
    "winddirection": "348.0",
    "windspeedms": "5.4",
    "windums": "1.14",
    "windvms": "-5.28",
    "precipitationamount": "7.84",
    "totalcloudcover": "43.9",
    "lowcloudcover": "0.0",
    "mediumcloudcover": "21.4",
    "highcloudcover": "28.7",
    "radiationglobal": "1.3",
    "radiationglobalaccumulation": "12949259.0",
    "radiationnetsurfaceswaccumulation": "11809502.0",
    "radiationswaccumulation": "769211.0",
    "visibility": "26811.9",
    "windgust": "8.3",
    "timestamps": datetime.datetime(2026, 4, 5, 20, 0),
}


def test_WeatherModel_data_valid():

    validated_model = WeatherModel(**data)

    assert validated_model.temperature == Decimal("5.1")
    assert validated_model.pressure == Decimal("1020.0")
    assert validated_model.timestamps == datetime.datetime(2026, 4, 5, 20, 0)


def test_WeatherModel_type_invalid():
    invalid_data = {**data, "temperature": "not decimal"}

    with pytest.raises(ValidationError) as exec_error:
        WeatherModel(**invalid_data)

    errors = exec_error.value.errors()

    assert errors[0]["loc"] == ("temperature",)
