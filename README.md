## Helsinki weather forecast data pipeline

Simple data pipeline that fetches weather forecast data from FMI wfs endpoint for Helsinki area, parses and cleans the data, and stores it in a PostgreSQL database. 

## DATA IS STORED IN 2 TABLES
* raw_forecast and current_forecast
  1. current_forecast does not allow duplicate data and raw_forecast allows duplicate data
     1. reason for this arrangement is to be able to recover from human or api errors 





## TECH STACK
1. python 3.11
2. pydantic
3. sqlalchemy
4. requests
5. decouple
6. postgresql
7. docker
8. pytest

## PIPELINE FLOW
1. call_fmi_api() in api_calls.py is responsible for calling the api and fetching data from it
1. parse_xml_to_raw_row_dict() in data_cleaning.py is responsible for parsing the data and removing NaN values
3. insert_to_db() in utility.py is responsible for inserting rows to database
4. latest_db_timestamp() in utility.py is responsible for getting the latest timestamp row from the database 
5. main() in main.py is responsible for orchestrating the whole pipeline


## HOW TO RUN
1.  clone repo 
2.  copy .env.example to your own .env file and set values you want
3. if you don't have uv astral install it <!-- https://docs.astral.sh/uv/getting-started/installation/        #there might have been changes after adding link here -->
4. if you have python 3.11 run uv sync else run uv python install 3.11 and run uv sync
5. start virtual enviroment if on linux source .venv/bin/activate and if on windows .venv/Scripts/activate
6. run docker-compose  up -d if you want to run it in the background.
7. run python main.py in the data_engineering_001 directory 



## TESTING
  - run pytest in the working_project/tests
  - pytest 
  - expected result
  - collected 6 items 
  - passed 6 items
