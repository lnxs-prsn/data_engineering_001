Helsinki weather forecast data pipeline

Simple data pipeline that fetches weather forecast data from FMI wfs endpoint for Helsinki area, parses and cleans the data, and stores it in a PostgreSQL database. 

DATA IS STORED IN 2 TABLES
* raw_forecast and current_forecast
  1. current_forecast does not allow duplicate data and raw_forecast allows duplicate data
     1. reason for this arrangement is to be able to recover from human or api errors 





TECH STACK
1. python
2. pandas
3. sqlalchemy
4. requests
5. decouple
6. postgresql
7. docker
8. pytest

PIPELINE FLOW
1. call_fmi_api() in api_calls.py is responsible for calling the api and fetching data from it
1. parse_response() in data_cleaning.py is responsible for parsing the data
2. clean_data() in data_cleaning.py is responsible for cleaning the data and creating dataframe
3. save_to_db() in db_functionspy is responsible for saving the data to the database
4. last_timestamp() in db_functions.py is responsible for getting the latest timestamp from the database is compared to the timestamps in the dataframe to filter out already existing data
5. main() in main.py is responsible for orchestrating the whole pipeline