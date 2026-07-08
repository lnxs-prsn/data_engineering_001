## Helsinki weather forecast data pipeline

Simple data pipeline that fetches weather forecast data from FMI wfs endpoint for Helsinki area, parses and cleans the data, and stores it in a PostgreSQL database. 

## DATA IS STORED IN 1 TABLE
* weather_table





## TECH STACK
1. python 3.11
2. pydantic
3. sqlalchemy
4. requests
5. decouple
6. postgresql
7. docker
8. pytest
9. uv
10. tenacity



## HOW TO RUN
1.  clone repo 
2.  copy env.example to your own .env file and set values you want
3. if you don't have uv made by astral install it  https://docs.astral.sh/uv/getting-started/installation/        # uv docs for latest install instructions 
4. if you dont have python 3.11 type uv python install 3.11 click enter 
5. then type uv sync click enter
6. start virtual environment 
   1. if on linux source .venv/bin/activate 
   2. if on windows .venv/Scripts/activate
7. type docker compose up -d click enter if you want to run it in the background.
8.  run python main.py in the data_engineering_001 directory 


## PIPELINE FLOW
1. call_fmi_api() in api_calls.py is responsible for calling the api and fetching data from it
2. parse_xml_to_raw_row_dict() in data_cleaning.py is responsible for parsing the data and removing NaN values
3. add_to_insert_que() in utility.py is responsible for inserting rows to database
4. latest_db_timestamp() in utility.py is responsible for getting the latest timestamp row from the database 
5. main() in main.py is responsible for orchestrating the whole pipeline


## PROJECT STRUCTURE
```
├── docker-compose.yml
├── env.example
├── helsinki_weather_pipeline
│   ├── __init__.py
│   ├── src
│   │   ├── api_calls.py
│   │   ├── config.yaml
│   │   ├── data_cleaning.py
│   │   ├── __init__.py
│   │   ├── logging_config.py
│   │   ├── models.py
│   │   └── utility.py
│   └── tests
│       ├── __init__.py
│       ├── test_api_calls.py
│       ├── test_data_cleaning.py
│       ├── test_models.py
│       ├── test_response_sample_fmi.xml
│       ├── test_utility.py
│       └── weather_app.log
├── main.py
├── pyproject.toml
├── README.md
├── uv.lock
└── weather_app.log
```


## TESTING
  - at project root
   - type pytest click enter
   - expected result
   - collected 10 items 
   - passed 10 items
